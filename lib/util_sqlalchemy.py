import datetime
import decimal
import json
from abc import ABC, abstractmethod
from enum import Enum

import pytz
from dateutil import parser
from flask_sqlalchemy import pagination
from sqlalchemy import DateTime, String
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TEXT, TypeDecorator

from lib.util_datetime import tzware_datetime
from scrapegod.extensions import db
from lib.util_json import convert_decimals_to_floats


class JSONEncodedType(TypeDecorator):
    """Stores and retrieves JSON as TEXT for SQLite compatibility, with support for datetime and date."""

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        value = convert_decimals_to_floats(value)
        value = self._convert_to_serializable(value)
        return json.dumps(value) if isinstance(value, (dict, list, str)) else value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return self._convert_from_string(json.loads(value))
            except json.JSONDecodeError:
                return value
        return None

    def _convert_to_serializable(self, value):
        """Converts non-serializable types to serializable form."""
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        elif isinstance(value, decimal.Decimal):
            return float(value)
        elif isinstance(value, (dict, list)):
            if isinstance(value, dict):
                return {k: self._convert_to_serializable(v) for k, v in value.items()}
            return [self._convert_to_serializable(v) for v in value]
        return value

    def _convert_from_string(self, value):
        """Converts values from string back to their appropriate types."""
        if isinstance(value, dict):
            return {
                k: self._convert_to_numeric_or_datetime(v) for k, v in value.items()
            }
        elif isinstance(value, list):
            return [self._convert_to_numeric_or_datetime(v) for v in value]

        return self._convert_to_numeric_or_datetime(value)

    def _convert_to_numeric_or_datetime(self, value):
        """Helper method to convert strings to numeric or datetime types."""
        if isinstance(value, str):
            # Attempt to convert to a numeric type
            if value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                pass
            # Attempt to convert to a datetime or date type
            try:
                return parser.parse(value)
            except (ValueError, TypeError):
                pass
        return value


class BaseEnum(Enum):
    @classmethod
    def member_values(cls):
        """It returns a list of the values of the members of an enum class

        Parameters
        ----------
        cls
            The class that you want to get the member values from.

        Returns
        -------
            A list of the values of the members of the class.

        """
        member_values = []
        for member in cls.__members__:
            member_values.append(getattr(cls, member).value)
        return member_values


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class MutableList(Mutable, list):
    # I believe self must be added in arguments when calling insert
    def append(self, value):
        """Append value to mutable list"""
        list.append(self, value)
        self.changed()

    def insert(self, value):
        """Insert value to mutable list"""
        list.insert(self, 0, value)
        self.changed()

    def pop(self, index=0):
        """Delete and return value of mutable list base index"""
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """

    cache_ok = True
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError("{!r} must be TZ-aware".format(value))
        return value

    def __repr__(self):
        return "AwareDateTime()"


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_on = db.Column(AwareDateTime(), default=tzware_datetime)
    updated_on = db.Column(
        AwareDateTime(), default=tzware_datetime, onupdate=tzware_datetime
    )

    @staticmethod
    def set_tzaware(start_date: datetime):
        """If the datetime object is naive, then make it timezone aware by adding 12 hours to it

        Parameters
        ----------
        start_date : datetime
            datetime

        Returns
        -------
            A datetime object with a timezone.

        """
        if start_date.tzinfo is None:
            tz = pytz.timezone("Australia/Melbourne")
            start_date = tz.localize(start_date) + datetime.timedelta(hours=12)
        return start_date

    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.

        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        if field not in cls.__table__.columns:
            field = "created_on"

        if direction not in ("asc", "desc"):
            direction = "asc"

        return field, direction

    @classmethod
    def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=""):
        """
        Determine which IDs are to be modified.

        :param scope: Affect all or only a subset of items
        :type scope: str
        :param ids: List of ids to be modified
        :type ids: list
        :param omit_ids: Remove 1 or more IDs from the list
        :type omit_ids: list
        :param query: Search query (if applicable)
        :type query: str
        :return: list
        """
        omit_ids = map(str, omit_ids)

        if scope == "all_search_results":
            # Change the scope to go from selected ids to all search results.
            ids = cls.query.with_entities(cls.id).filter(cls.search(query))

            # SQLAlchemy returns back a list of tuples, we want a list of strs.
            ids = [str(item[0]) for item in ids]

        # Remove 1 or more items from the list, this could be useful in spots
        # where you may want to protect the current user from deleting themself
        # when bulk deleting user accounts.
        if omit_ids:
            ids = [id for id in ids if id not in omit_ids]

        return ids

    @classmethod
    def bulk_delete(cls, ids):
        """
        Delete 1 or more model instances.

        :param ids: List of ids to be deleted
        :type ids: list
        :return: Number of deleted instances
        """
        delete_count = cls.query.filter(cls.id.in_(ids)).delete(
            synchronize_session=False
        )
        db.session.commit()

        return delete_count

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    # New Method add to update values in table
    def update(self):
        """
        update a model instance.

        :return: Model instance
        """
        return db.session.commit()

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ", ".join("{}={!r}".format(n, getattr(self, n)) for n in columns)
        return "<{} {}({})>".format(obj_id, self.__class__.__name__, values)


def paginate(data, page, per_page):
    """It takes a list of items, a page number, and a number of items per page, and returns a
    SQLAlchemy's Pagination object

    Parameters
    ----------
    data
        The list of items to paginate
    page
        The current page number
    per_page
        The number of items to display per page

    Returns
    -------
        A Pagination object

    """
    # Based on page and per_page info, calculate start and end index of items to keep
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Get the paginated list of items
    items = data[start_index:end_index]

    # Create Pagination object
    return pagination(None, page, per_page, len(data), items)


class QueryPagination(ABC):
    @property
    @abstractmethod
    def data(self):
        """Method that should be defined in subclass"""
        pass

    def data_page(self, page, per_page=15):
        """It takes a list of data, a page number, and a number of items per page, and returns a list of
        data for the given page

        Parameters
        ----------
        page
            The page number to return
        per_page, optional
            The number of items to display per page.

        Returns
        -------
            A list of dictionaries.

        """
        return paginate(self.data, page, per_page)


class EnumString(TypeDecorator):
    impl = String

    def __init__(self, *args, **kwargs):
        self.valid_values = kwargs.pop("valid_values", None)
        super(EnumString, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if self.valid_values and value not in self.valid_values:
            raise ValueError(
                f"Invalid value '{value}'. Must be one of {self.valid_values}."
            )
        return value

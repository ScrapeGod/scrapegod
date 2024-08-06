import ast
import json
import logging
from decimal import Decimal
from typing import Iterable, List

from flask_sqlalchemy.model import Model
from sqlalchemy import String, cast, inspect, text
from sqlalchemy.ext.declarative import declarative_base

from lib.api.jsonapi_formatter import convert_to_jsonapi_format

logger = logging.getLogger("root")


Base = declarative_base()


class HasNoRelation(Exception):
    pass


class ScrapegodModelBaseClass(Model):
    @classmethod
    def my_columns(cls) -> List[str]:
        """Return a list of the names of the columns in the table associated with the given class

        Parameters
        ----------
        cls
            The class that we are decorating.

        Returns
        -------
            A list of the names of the columns in the table.

        """
        return [col.name for col in cls.__table__.columns]

    @classmethod
    def is_my_column(cls, column: str) -> bool:
        """> If the class has the attribute and the attribute is in the list of columns, then return True

        Parameters
        ----------
        cls
            The class that is being decorated.
        column : str
            The name of the column to check.

        """
        return hasattr(cls, column) and column in cls.my_columns()

    @classmethod
    def filter_kwargs(cls, **kwargs):
        """It takes a class and a dictionary of keyword arguments, and returns a new dictionary of keyword
        arguments that only contains the keys that are columns of the class

        Parameters
        ----------
        cls
            The class that is being instantiated.

        Returns
        -------
            A dictionary with the keys and values of the kwargs that are in the class.

        """
        new_kwargs = {}
        for key, value in kwargs.items():
            if cls.is_my_column(key):
                new_kwargs[key] = value
        return new_kwargs

    @classmethod
    def search_filter(cls, query, columns):
        """It takes a class, a query, and a list of columns, and returns a SQLAlchemy filter that can be
        used to filter the class by the query

        Parameters
        ----------
        cls
            The class that you're searching on.
        query
            The search query
        columns
            a list of columns to search

        Returns
        -------
            A generator object

        """
        if query == "" or query.text == "":
            return text("")
        search_query = "%{}%".format(query)
        search_chain = (
            cast(getattr(cls, col), String).ilike(search_query) for col in columns
        )
        return search_chain

    def obj_to_dict(
        self,
        jsonify=False,
        additional_properties=[],
        exclude=[],
        jsonapi_format=False,
        relations=[],
        primary_key="id",
        **kwargs,
    ) -> dict:
        """It creates a dictionary from a SQLAlchemy object.
        Returns
        -------
            A dictionary of the attributes of the object.
        """
        data = {
            c: getattr(self, c)
            for c in list(self.my_columns()) + additional_properties
            if c not in exclude
        }
        if jsonify:
            data = json.loads(json.dumps(data, default=str))

        relationships = None
        if relations:
            relationships = self.get_relations(relations)

        if jsonapi_format:
            return convert_to_jsonapi_format(
                self.__class__.__tablename__,
                data,
                relationships,
                primary_key=primary_key,
            )
        else:
            if relationships:
                data = {**data, **relationships}
            return data

    def get_relations(self, relations=[]):
        relationships = {}
        for relation in relations:
            relation_obj = getattr(self, relation)
            if relation_obj and not isinstance(relation_obj, str):
                if isinstance(relation_obj, Iterable):
                    if len(relation_obj) > 0 and not isinstance(relation_obj[0], dict):
                        relationships[relation] = [
                            rel.obj_to_dict(jsonify=True, jsonapi_format=True)
                            for rel in relation_obj
                        ]
                    else:
                        relationships[relation] = relation_obj
                else:
                    if isinstance(relation_obj, Model):
                        relationships[relation] = relation_obj.obj_to_dict(
                            jsonify=True, jsonapi_format=True
                        )
                    else:
                        relationships[relation] = relation_obj
            else:
                if relation_obj is not None:
                    relationships[relation] = relation_obj

        return relationships

    @classmethod
    def create(cls, filter=True, **kwargs):
        """It creates an object of the class passed to it, and if the filter parameter is set to True, it
        filters the kwargs passed to it

        Parameters
        ----------
        cls
            The class that the method is being called on.
        filter, optional
            If True, the kwargs will be filtered using the filter_kwargs method.

        Returns
        -------
            The object is being returned.

        """
        logger.debug("ThreadletModelBaseClass::create here")
        if filter == True:
            kwargs = cls.filter_kwargs(**kwargs)
        obj = cls(**kwargs)
        return obj

    @classmethod
    def get_or_create(cls, get_single=False, **kwargs):
        """It takes a class and a set of keyword arguments, and returns a tuple of the object and a boolean
        indicating whether the object was created

        Parameters
        ----------
        cls
            The class of the object you want to create.
        get_single, optional
            If True, returns a single object. If False, returns a list of objects.

        Returns
        -------
            A tuple of the object and a boolean.

        """
        is_created = False
        filter_kwargs = cls.filter_kwargs(**kwargs)
        q = cls.query
        for key, value in filter_kwargs.items():
            q = q.filter(getattr(cls, key) == value)

        if get_single:
            obj = q.first()
        else:
            obj = q.all()

        if not obj:
            is_created = True
            obj = cls(**kwargs)
        return obj, is_created

    @staticmethod
    def str_into_list_decimal(field):
        """Convert a string of space-separated values into a list of decimal values

        Parameters
        ----------
        field
            The field to be converted.

        Returns
        -------
            a list of the values in the field.

        """
        if field and type(field) == str:
            field = field.replace(" ", "")
            field = ast.literal_eval(field)
            field = [round(Decimal(float(x)), 6) for x in field]
        return field

    @staticmethod
    def str_into_list_float(field):
        """Convert a string of space-separated values into a list of decimal values

        Parameters
        ----------
        field
            The field to be converted.

        Returns
        -------
            a list of the values in the field.

        """
        if field and type(field) == str:
            field = field.replace(" ", "")
            field = ast.literal_eval(field)
            field = [round(float(x), 6) for x in field]
        return field

    @classmethod
    def is_elec_entity(cls):
        class_name = cls.__name__
        if "elec" in class_name.lower():
            return True
        elif "gas" in class_name.lower():
            return False
        else:
            return None

    def update_filter_kwargs(self, **kwargs):
        """It takes a dictionary of keyword arguments and sets the attributes of the object to the values
        of the keyword arguments

        """
        filter_kwargs = self.filter_kwargs(**kwargs)
        for key, value in filter_kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def clean_null_steps(charge_dict: dict) -> dict:
        """Given a dictionary of charges, remove any steps that are null.

        Parameters
        ----------
        charge_dict: dict
            a dictionary of tariff_name:charge_value pairs

        Returns
        -------
            A dictionary of the charges that are not null.

        """
        from prosebit.bill_flow.constants import BillFlowConstants

        charge_dict_copy = charge_dict.copy()
        for tariff in list(charge_dict_copy.keys()):
            if tariff == "demand":
                continue

            if isinstance(charge_dict_copy[tariff], Iterable) and not isinstance(
                charge_dict_copy[tariff], str
            ):
                charge_dict_copy[tariff] = [
                    step
                    for step in charge_dict_copy[tariff]
                    if step not in BillFlowConstants.NONE_VAL
                ]

        return charge_dict_copy

    @classmethod
    def is_my_relation(cls, relation: str):
        custom_relations = getattr(cls, "custom_relations", [])
        if custom_relations:
            custom_relations = custom_relations()
            if relation in custom_relations:
                return True

        relation_name = [rel["relation"] for rel in cls.my_relations()]
        return relation in relation_name

    @classmethod
    def my_relations(cls):
        """
        This function inspects a SQLAlchemy model to determine its relationships.
        It returns a list of relationship names and their types (one-to-one, one-to-many, many-to-one, many-to-many).

        Parameters:
            model: The SQLAlchemy model to be inspected.

        Returns:
            A list of dictionaries. Each dictionary represents a relationship and contains the relationship name (key 'relation')
            and its type (key 'type', 'one', 'many', 'many_to_one' or 'many_to_many').
        """
        inspector = inspect(cls)
        relationships = []

        for rel in inspector.mapper.relationships:
            direction = rel.direction.name.lower()
            if direction == "onetomany":
                relationships.append(
                    {
                        "relation": rel.key,
                        "type": "one_to_many",
                        "model": rel.entity.class_,
                    }
                )
            elif direction == "manytoone":
                relationships.append(
                    {
                        "relation": rel.key,
                        "type": "many_to_one",
                        "model": rel.entity.class_,
                    }
                )
            elif direction == "manytomany":
                relationships.append(
                    {
                        "relation": rel.key,
                        "type": "many_to_many",
                        "model": rel.entity.class_,
                    }
                )
        return relationships

    @classmethod
    def relation_class(cls, relation: str):
        """It returns the class of the relation of a given class.

        Parameters
        ----------
        cls
            The class that the method is being called on.
        relation : str
            str

        Returns
        -------
            The class of the relation.

        """

        if not hasattr(cls, relation) or not cls.is_my_relation(relation):
            raise HasNoRelation(
                f"{cls.__tablename__} table has no relation to {relation}"
            )

        return getattr(cls, relation).property.mapper.class_

    @classmethod
    def is_array_column(cls, column_name):
        from sqlalchemy.dialects.postgresql import ARRAY
        from sqlalchemy.sql.sqltypes import ARRAY as PostgresArray

        column_type = getattr(cls, column_name).type
        return isinstance(column_type, ARRAY) or isinstance(column_type, PostgresArray)

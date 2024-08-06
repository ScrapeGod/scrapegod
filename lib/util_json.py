import decimal
import json

from flask import jsonify


def render_json(status, *args, **kwargs):
    """
    Return a JSON response.

    Example usage:
      render_json(404, {'error': 'Discount code not found.'})
      render_json(200, {'data': coupon.to_json()})

    :param status: HTTP status code
    :type status: int
    :param args:
    :param kwargs:
    :return: Flask response
    """
    response = jsonify(*args, **kwargs)
    response.status_code = status

    return response


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.default(v) for v in obj]
        else:
            return super().default(obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime, date
from decimal import Decimal

from xero_python.api_client.serializer import serialize


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, (uuid.UUID, Decimal)):
            return str(o)
        return super(JSONEncoder, self).default(o)


def parse_json(data):
    return json.loads(data, parse_float=Decimal)


def serialize_model(model):
    return jsonify(serialize(model))


def jsonify(data):
    return json.dumps(data, sort_keys=True, indent=4, cls=JSONEncoder)


def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def convert_decimals_to_floats(value):
    """
    Recursively converts all decimal.Decimal values to floats in the given data.
    """
    if isinstance(value, decimal.Decimal):
        # Convert decimal.Decimal to float
        return float(value)
    elif isinstance(value, dict):
        # Recursively apply to dictionary values
        return {k: convert_decimals_to_floats(v) for k, v in value.items()}
    elif isinstance(value, list):
        # Recursively apply to elements in list
        return [convert_decimals_to_floats(elem) for elem in value]
    else:
        # Return other values unchanged
        return value

def convert_to_jsonapi_format(
    type: str, instance_data: dict, relations_data: dict, primary_key: str = None
):
    primary_key_value = instance_data.pop(primary_key, None)
    data_formatted = {
        "type": type,
        "id": primary_key_value,
        "attributes": instance_data,
    }
    if relations_data:
        data_formatted["relationships"] = relations_data

    return data_formatted

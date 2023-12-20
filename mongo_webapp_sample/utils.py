import uuid


def filter_keys(dict_obj, allowed_keys):
    return {key: dict_obj[key]
            for key in allowed_keys
            if key in dict_obj}


def ensure_id(dict_obj):
    # This helper ensures that the specified dict object has an "_id"
    # field. We'll generate our own UUIDs instead of relying on the default
    # MongoDB IDs.
    if not dict_obj.get('_id'):
        dict_obj['_id'] = str(uuid.uuid4())


def ensure_location_type(dict_obj):
    # ensure that the proper location type is set.
    if dict_obj.get("location"):
        dict_obj['location']['type'] = 'Point'

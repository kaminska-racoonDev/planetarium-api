def params_to_ints(qs):
    """Converts a list of string IDs to a list of integers"""
    return [int(str_id) for str_id in qs.split(",")]

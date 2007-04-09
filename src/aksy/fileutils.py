def is_file_type_supported(supported_file_types, filename):
    for type in supported_file_types:
        if filename.lower().endswith(type):
            return True
    return False
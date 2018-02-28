import unit_dictionary


# DIGITAL STORAGE CONVERSION
def check_digital_storage(value, units_from, units_to, decimal_places):
    dictionary = unit_dictionary.Dictionary()  # Dictionary object
    digital_storage_dict = dictionary.digital_storage_dict()  # Universal Metric unit dictionary

    # Digital storage conversions
    if units_from in digital_storage_dict and units_to in digital_storage_dict:
        from_base = digital_storage_dict.get(units_from, None)
        to_base = digital_storage_dict.get(units_to, None)

        value = value * from_base / to_base
        return str(round(value, decimal_places)) + units_to
    return False


def check_digital_storage_without_unit(value, units_from, units_to, decimal_places=1):
    dictionary = unit_dictionary.Dictionary()  # Dictionary object
    digital_storage_dict = dictionary.digital_storage_dict()  # Universal Metric unit dictionary

    # Digital storage conversions
    if units_from in digital_storage_dict and units_to in digital_storage_dict:
        from_base = digital_storage_dict.get(units_from, None)
        to_base = digital_storage_dict.get(units_to, None)

        value = value * from_base / to_base
        return float(round(value, decimal_places))


def unit_converter(value, units_from):
    dictionary = unit_dictionary.Dictionary()  # Dictionary object
    digital_storage_dict = dictionary.digital_storage_dict()  # Universal Metric unit dictionary
    if units_from in digital_storage_dict:
        value_bit = value * digital_storage_dict.get(units_from, None)
        for unit in digital_storage_dict:
            if value_bit >= 10 * digital_storage_dict.get(unit, None):
                return unit


if __name__ == '__main__':
    unit_to = unit_converter(1024, 'byte')
    print unit_to









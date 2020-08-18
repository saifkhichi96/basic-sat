def remove_whitespaces(string: str) -> str:
    """Removes all whitespaces from a string.

    :param string: The string to remove whitespaces from.
    :return: A new string with no whitespaces.
    """
    return ''.join(string.split())

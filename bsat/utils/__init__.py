"""Defines helper functions to perform common tasks."""


def remove_whitespaces(string: str) -> str:
    """Removes all whitespaces from a string.

    Args:
        string: The string to remove whitespaces from.

    Returns:
        A new string with no whitespaces.
    """
    return ''.join(string.split())

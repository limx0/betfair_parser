class IntStr(int):
    """Class for marking mis-formatted integer JSON fields, e.g. "123" instead of 123."""

    # TODO: Still no good solution for "'null'" found


class FloatStr(float):
    """Class for marking mis-formatted float JSON fields, e.g. "-5.5" instead of -5.5."""

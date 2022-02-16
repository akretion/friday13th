# -*- coding: utf-8 -*-


class Friday13thError(Exception):
    """Exception base class"""


class FieldValueError(Friday13thError):
    """Attempting to set a wrong value"""

    def __init__(self, field, value):
        self.field = field
        self.value = value
        super(FieldValueError, self).__init__(self)

    def __str__(self):
        return "field:{0} type:{1} decimais:{2} length:{3} - value:{4}".format(
            self.field.name,
            self.field.type,
            self.field.decimais,
            self.field.length,
            repr(self.value),
        )


class OverSizeError(FieldValueError):
    """Attempt to assigning a value larger than field size."""


class TypeError(FieldValueError):
    """Attempted assignment type not supported by field."""


class WrongDecimaisError(FieldValueError):
    """Attempt to assigning a wrong decimal value."""


class WrongDateFormatError(FieldValueError):
    """Attempt to assigning a wrong decimal value."""


class ArgsMissingError(Friday13thError):
    """Missing arguments in the method call."""

    def __init__(self, args_missing):
        self.args_missing = args_missing
        super(ArgsMissingError, self).__init__(self)

    def __str__(self):
        return ("Missing arguments: {0}").format(", ".join(self.args_missing))


class EmptyFileError(Friday13thError):
    """Attempting to write empty file."""


class NoRecordError(Friday13thError):
    """Attempting to write file without records. """


class RequiredFieldError(Friday13thError):
    """Required field not filled."""

# -*- coding: utf-8 -*-

from decimal import Decimal, InvalidOperation
from datetime import datetime, date

from . import errors


class BaseField(object):
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.type == "text":
            if value:
                if not isinstance(value, str):
                    raise errors.TypeError(self, value)
                if len(value) > self.length:
                    raise errors.OverSizeError(self, value)

        elif self.decimais:
            if not isinstance(value, Decimal):
                raise errors.TypeError(self, value)

            #FIXME - Get decimal from json layout
            PLACES = Decimal(10) ** (self.decimais * -1)
            value = value.quantize(PLACES)
            num_decimais = value.as_tuple().exponent * -1
            if num_decimais != self.decimais:
                raise errors.WrongDecimaisError(self, value)

            if len(str(value).replace('.', '')) > self.length:
                raise errors.OverSizeError(self, value)

        elif self.type == 'date':
            if value:
                if not isinstance(value, (date, datetime)):
                    raise errors.TypeError(self, value)
                if not self.format:
                    raise errors.WrongDateFormat(self, value)

                date_value = value.strftime(self.format)

                if len(str(date_value).replace("-", "")) > self.length:
                    raise errors.OverSizeError(self, date_value)

        else:
            if not isinstance(value, (int,)):
                raise errors.TypeError(self, value)
            if len(str(value)) > self.length:
                raise errors.OverSizeError(self, value)

        self._value = value

    def __str__(self):
        if self.value is None:
            if self.default is not None:
                if self.decimais:
                    self.value = Decimal("{0:0.{1}f}".format(
                        self.default, self.decimais))
                else:
                    self.value = self.default
            else:
                raise errors.RequiredFieldError(self.name)

        if self.type == "text" or self.decimais:
            if self.decimais:
                value = str(self.value)
                chars_faltantes = self.length - len(value)
                return ("0" * chars_faltantes) + value
            else:
                chars_faltantes = self.length - len(self.value)
                return self.value + (" " * chars_faltantes)

        if self.type == "date" and self.value:

            return self.value.strftime(self.format)

        if self.type == "integer":
            return "{0:0{1}d}".format(self.value, self.length)

        return "{0:{1}}".format(self.value, self.length)

    def __repr__(self):
        return str(self)

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

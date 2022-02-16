# -*- coding: utf-8 -*-

import os
import json

from decimal import Decimal, InvalidOperation
try:
    from collections import OrderedDict
except ImportError:
    # Fallback for python 2.6
    from ordereddict import OrderedDict

from .field import BaseField
from . import errors


class BaseRecord(object):

    def __new__(cls, **kwargs):
        fields = OrderedDict()
        attrs = {"_fields": fields}

        for Field in list(cls._fields_cls.values()):
            field = Field()
            fields.update({field.name: field})
            attrs.update({field.name: field})

        new_cls = type(cls.__name__, (cls, ), attrs)
        return super(BaseRecord, cls).__new__(new_cls, **kwargs)

    def __init__(self, **kwargs):
        self.fromdict(kwargs)

    def todict(self):
        data_dict = dict()
        for field in list(self._fields.values()):
            if field.value is not None:
                data_dict[field.name] = field.value
        return data_dict

    def fromdict(self, data_dict):
        for key, value in list(data_dict.items()):
            if hasattr(self, key):
                setattr(self, key, value)

    def carregar(self, registro_str):
        for campo in self._campos.values():
            valor = registro_str[campo.inicio:campo.fim].strip()
            if campo.decimais:
                exponente = campo.decimais * -1
                dec = valor[:exponente] + "." + valor[exponente:]
                try:
                    campo.valor = Decimal(dec)
                except InvalidOperation:
                    raise # raise custom?

            elif campo.formato == "num":
                try:
                    campo.valor = int(valor)
                except ValueError:
                    raise errors.TypeError(campo, valor)
            else:
                campo.valor = valor

    def __str__(self):
        return "".join(
            [str(field) for field in list(self._fields.values())])


class Records(object):

    def __init__(self, specs):

        spec_file = open(specs)
        spec = json.load(spec_file)
        spec_file.close()

        sessions_specs = spec.get("sessions", {})
        for key in sorted(sessions_specs.keys()):
            setattr(self, sessions_specs[key].get("name"),
                self._load_spec(sessions_specs[key]))

    #TODO
    def print_doc(self, spec):
        spec_file = open(spec)
        spec = json.load(spec_file, object_pairs_hook=OrderedDict)
        spec_file.close()

        sessions_specs = spec.get("sessions", {})
        for key in sorted(sessions_specs.keys()):
            for field in sessions_specs[key].get("fields"):
                field_name = sessions_specs[key].get("fields")[field].get("name")
                field_start = sessions_specs[key].get("fields")[field].get("start")
                field_end = sessions_specs[key].get("fields")[field].get("end")
                size = sessions_specs[key].get("fields")[field].get("end") - (sessions_specs[key].get("fields")[field].get("start") - 1)

    def _load_spec(self, spec):
        fields = OrderedDict()
        attrs = {"_fields_cls": fields}
        cls_name = spec.get("name")
        field_specs = spec.get("fields", {})
        for key in sorted(field_specs.keys()):

            field_spec = field_specs[key]

            name = field_spec.get("name")
            start = field_spec.get("start") - 1
            end = field_spec.get("end")

            field_attrs = {
                "name": name,
                "start": start,
                "end": end,
                "length": end - start,
                "type": field_spec.get("type", "text"),
                "decimais": field_spec.get("decimais", 0),
                "default": field_spec.get("default"),
                "format": field_spec.get("format", "%Y-%m-%d"),
            }
            Field = type(name, (BaseField,), field_attrs)
            entry = {Field.name: Field}

            fields.update(entry)

        return type(cls_name, (BaseRecord, ), attrs)

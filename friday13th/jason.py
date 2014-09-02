# -*- coding: utf-8 -*-

import json
from collections import OrderedDict


class File(object):
    """File"""
                #TODO
    def __init__(self, spec):

        self._name = None
        self._format = None
        self._version = None
        self._separetor = None
        self._records = []

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def format(self):
        return self._format

    @property
    def separator(self):
        return self._separator

    def add_record(self, record):
        self._records.append(record)

    def __unicode__(self):
        return u'\r\n'.join(unicode(record) for record in self._records)

    def __len__(self):
        return len(self._records)


class Fiday13thError(Exception):
    """Base Exception"""
    #TODO
    pass

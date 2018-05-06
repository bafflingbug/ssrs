#!/usr/bin/env python
# -*- coding: utf-8 -*-


def safe_value(value, default, allow_null=True, in_list=None, type_check=True):
    if in_list and default not in in_list:
        raise ValueError('defaule value not in in_list')
    if in_list:
        if value in in_list:
            return value
        return default
    if not allow_null and type(default) == str:
        if value == '':
            return default
        return value
    if value:
        if type_check and type(value) != type(default):
            return default
        else:
            return value
    return default


def safe_get(d, key):
    if type(d) is dict and key in d:
        return d[key]
    return None

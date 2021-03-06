#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dict_to_namedtuple.py

from collections import namedtuple, OrderedDict
from converter.converter_utilities import *


def to_namedtuple(d: dict, name: str = None, keep_dicts: bool = False, **kwargs) -> namedtuple:
    """
    namedtuple:
        https://docs.python.org/3/library/collections.html#collections.namedtuple

    This function will converts a dictionary to a namedtuple
    namedtuples are inmutable and can be iterated over normally
    tuples can be unpacked

    Caution !!!  non-deterministic behavior  !!!
    this conversion doesn't respect the keys of the given dictionary
    invalid names will be converted to usable variable names
    this can result in non-deterministic behaviors!

    behaviors:
        spaces in keywords will (by default) replaced with `_`
        invalid characters in keywords will (by default) replaced with `_`
        tuple keywords prioritizes string in the tuple else the 1st position
        keywords starting with a `_` will be stripped of the underscore
        keywords that are keywords receive a trailing `_` (underscore)
        keywords that are a single invalid character will be converted to an integer representing the Unicode code
            this will than be treated as an all number keyword.
        invalid characters trailing a valid start wil (by default) replaced by a `_` (underscore)
        keywords that start with or are all numbers will get (by default) a leading `d`
    after all the name conversion can lead to duplicate variables!
    this will raise a ValueError

    for deterministic behavior:
        make sure the keywords given are words that can be used as a variable name
        to check this use the following code:
    >>> import keyword
    >>> dict_keyword = 'keyword_in_dict'
    >>> if str(dict_keyword).isidentifier() and not keyword.iskeyword(str(dict_keyword)):
    >>>     print("%s is a good keyword" % dict_keyword)

    :param d: dict          dictionary to convert
    :param name: str        name of the namedtuple, if None 'namedtuple' is the name
    :param keep_dicts: bool if True nested dicts won't be converted to namedtuple
    :param kwargs:          keywords directly passed through to `condition_identifier`
    accepted keywords:      leading_digit_char: str must be valid start variable character
                            space_replace_char: str must be valid continue variable character
                            invalid_replace_char: str must be valid start & continue variable character
    :raises ValueError:     if given dictionary contains duplicate keyword after conversion (see return section)
    :return namedtuple:     the namedtuple created from the given dictionary
    """
    if not isinstance(d, dict):
        raise ValueError("expected d to be of type(dict), '%s'" % type(d))

    seen = set()  # create a set to fill with unique keywords
    new_dict = OrderedDict()
    name = condition_identifier(identifier=str(name), **kwargs) if bool(name) else 'namedtuple'

    for _key, _val in d.items():
        _key = condition_identifier(identifier=_key, **kwargs)  # raw key, don't use str(key)
        if _key in seen:  # if _key is already available in the set
            raise ValueError("After conditioning a key is not unique anymore: %s" % _key)
        seen.add(_key)  # add the _key in the set

        # if there is a nested dictionary, and keep_dicts is false
        # create a recursive namedtuple for nested use
        if (type(_val) is dict or isinstance(_val, dict)) and not bool(keep_dicts):
            _val = to_namedtuple(d=_val, name=name, keep_dicts=keep_dicts)
        new_dict.update({_key: _val})  # add the key and value to the dictionary

    # namedtuple one-liner
    return namedtuple(name, new_dict.keys())(*new_dict.values())  # -> namedtuple


if __name__ == '__main__':
    # print(to_namedtuple.__doc__)
    d = {"a": 1, "@b": 2, "_c": 3, "1": 4, "d": {"d2": 5}}
    converted_dict = to_namedtuple(d)
    print(type(converted_dict))
    for key, value in zip(converted_dict._fields, converted_dict):
        print(f"{key}\t= {value}")

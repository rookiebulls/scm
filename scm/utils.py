# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import re
import json
import shlex
from copy import deepcopy

import six
from prompt_toolkit.completion import Completion


def get_params(words, start_str='--path-param.'):
    """Gets the param option dict."""
    origin_dicts = []
    for idx, word in enumerate(words):
        if word.startswith(start_str):
            param, value = re.split('\s*=\s*', word)
            origin_dicts.append(_param_chain_to_dict(param, value))
    return _all_params_dict(origin_dicts)


def _param_chain_to_dict(param, value=None):
    """Turn option into dict.
    For example:
    --path-param.id=1 to {'id': 1}
    --path-param.name.values=test to {'name': {'values': 'test'}}
    """
    param_list = param.split('.')[1:]
    current_node = {param_list.pop(): value}
    while param_list:
        key = param_list.pop()
        d = dict()
        d[key] = current_node
        current_node = deepcopy(d)
    return current_node


def merged_dict(a, b):
    """Recursely merge two dict into a new one."""
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
            result[k] = merged_dict(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def _all_params_dict(origin_dicts):
    """Merge all the params dict into one."""
    result = {}
    fixed_result = {}
    if len(origin_dicts) == 0:
        pass
    elif len(origin_dicts) == 1:
        result = origin_dicts[0]
    else:
        first, second = origin_dicts[0], origin_dicts[1]
        result = a = merged_dict(first, second)
        for b in origin_dicts[2:]:
            result = merged_dict(a, b)
            a = result
    for key, value in result.items():
        if isinstance(value, dict):
            fixed_result[key] = json.dumps(value)
        else:
            fixed_result[key] = value
    return fixed_result


class TextUtils(object):
    """Utilities for parsing and matching text."""

    META_LOOKUP = {}

    def __init__(self, display_meta=False):
        self.display_meta = display_meta

    def find_matches(self, word, collection):
        """Find all matches in collection for word.
        :param word: The word before the cursor.
        :param collection: A collection of words to match.
        """
        word = self._last_token(word).lower()
        for suggestion in self._find_collection_matches(
                word, collection):
            yield suggestion

    def get_tokens(self, text):
        """Parse out all tokens.
        :param text: A string to be split into tokens.
        """
        if text is not None:
            text = text.strip()
            words = self._safe_split(text)
            return words
        return []

    def _last_token(self, text):
        """Find the last word in text.
        :param text: A string to parse and obtain the last word.
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = self._safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    def _fuzzy_finder(self, text, collection):
        """Customized fuzzy finder with optional case-insensitive matching.
        :param text: Input string entered by user.
        :param collection: collection of strings which will be filtered based
            on the input `text`.
        """
        suggestions = []
        pat = '.*?'.join(map(re.escape, text.lower()))
        regex = re.compile(pat)
        for item in collection:
            r = regex.search(item.lower())
            if r:
                suggestions.append((len(r.group()), r.start(), item))
        return (z for _, _, z in sorted(suggestions))

    def _find_collection_matches(self, word, collection):
        """Yield all matching names in list.
        :param word: The word before the cursor.
        :param collection: A collection of words to match.
        """
        word = word.lower()
        for suggestion in self._fuzzy_finder(word, collection):
            if self.display_meta:
                yield Completion(suggestion,
                                 -len(word),
                                 display_meta=self.META_LOOKUP.
                                 get(suggestion, 'No description'))
            else:
                yield Completion(suggestion, -len(word))

    def _shlex_split(self, text):
        """Wrapper for shlex, because it does not seem to handle unicode in 2.6.
        :param text: A string to split.
        """
        if six.PY2:
            text = text.encode('utf-8')
        return shlex.split(text)

    def _safe_split(self, text):
        """Safely splits the input text.
        :param text: A string to split.
        """
        try:
            words = self._shlex_split(text)
            return words
        except Exception:
            return text

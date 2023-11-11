"""Routines for evaluating the quality of the data."""

import re


# Suspicious symbols and tokens
RE_SYMBOLS = re.compile(r'[&#<>{}\[\]\\]')  # r'[^A-Za-z0-9\s]+'
RE_TOKENS = re.compile(r'^[^a-zA-Z]+|[^a-zA-Z]+$')  # r'^\W+|\W+$'


def calc_degree_impurity(text):
    """Calculate the degree of impurity in a text."""
    return len(RE_SYMBOLS.findall(text)/len(text))


def is_token_suspicious(token):
    """Check whether token is suspicious."""
    return RE_TOKENS.search(token) is not None

"""Remove certain characters from text."""

import re
import html
import textacy.preprocessing as tp
# from functools import partial
from bs4 import BeautifulSoup, Comment


def clean_html(text):
    """Clean HTML text."""
    text = html.unescape(text)  # convert html escape to characters

    # parse HTML
    soup = BeautifulSoup(text, 'lxml')

    # remove certain tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # remove comments
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()    # comment doesn't have decompose() method

    # get untagged text
    text = soup.get_text()

    return text


normalize_text = tp.make_pipeline(
    tp.normalize.bullet_points,
    tp.normalize.hyphenated_words,  # reattach separated by line breaks
    tp.normalize.quotation_marks,
    tp.normalize.unicode)


replace_from_text = tp.make_pipeline(
    tp.replace.urls,
    tp.replace.emails,
    tp.replace.numbers,
    tp.replace.currency_symbols,
    tp.replace.phone_numbers)


remove_from_text = tp.make_pipeline(
    tp.remove.accents,
    tp.remove.punctuation)


def clean_text(text, is_html=False):
    """Clean text."""
    if is_html:
        text = clean_html(text)
    text = normalize_text(text)
    text = replace_from_text(text)
    text = remove_from_text(text)
    text = tp.normalize.whitespace(text)
    return text


# # remove special characters
# text = re.sub(r'[^A-Za-z0-9\s]+', '', text)


# Section
# -------
# Calculate the degree of "impurity" in a text

RE_SUSPICIOUS = re.compile(r'[&#<>{}\[\]\\]')


def calc_degree_impurity(text):
    """Calculate the degree of impurity in a text."""
    return len(RE_SUSPICIOUS.findall(text)/len(text))

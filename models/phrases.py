"""Extract key words and phrases from a given text."""

import spacy
import pytextrank               # noqa
from keybert import KeyBERT

# Load spaCy model
nlp = spacy.load('en_core_web_trf')
nlp.add_pipe("textrank")

# Load KeyBERT model
kw_model = KeyBERT(model='all-MiniLM-L6-v2')


def extract_key_phrases(text, num_phrases=5):
    """Extract key phrases from the given text."""
    doc = nlp(text)
    words = [(p.text, p.rank) for p in doc._.phrases]
    words = sorted(words, key=lambda x: x[1], reverse=True)
    return [word[0] for word in words[:num_phrases]]

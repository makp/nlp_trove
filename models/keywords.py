"""Extract keywords from a text."""

import spacy
from keybert import KeyBERT
from textacy import extract


class KeywordExtractor:
    """Extract keywords from a text."""

    def __init__(self, spacy_model: str = "en_core_web_trf"):
        """Initialize the KeywordExtractor class."""
        self.nlp = spacy.load(spacy_model)
        self.kw_model = KeyBERT(model='all-MiniLM-L6-v2')

    def extract_keywords_textacy(self, doc,
                                 algorithm: str = "sgrank",
                                 top_n: int = 5) -> [str]:
        """Extract keywords from the given text using textacy."""
        if isinstance(doc, spacy.tokens.Doc):
            spacy_doc = doc
        else:
            spacy_doc = self.nlp(doc)

        extraction_functions = {
            'sgrank': extract.keyterms.sgrank,
            'textrank': extract.keyterms.textrank,
            'yake': extract.keyterms.yake,
            'scake': extract.keyterms.scake
        }

        if algorithm not in extraction_functions:
            raise ValueError("Unsupported algorithm selected.")

        keywords = extraction_functions[algorithm](spacy_doc,
                                                   normalize='lemma',
                                                   topn=top_n)

        keywords = [keyword for keyword, weight in keywords]
        return keywords

    def extract_keywords_keybert(self, doc, top_n: int = 5) -> [str]:
        """Extract keywords from the given text using KeyBERT."""
        if isinstance(doc, spacy.tokens.Doc):
            text = doc.text
        else:
            text = doc

        # Extract keywords using the KeyBERT model
        keywords = self.kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 1),
            stop_words='english',
            use_mmr=True,
            diversity=0.7,
            top_n=top_n)

        # Extract just the keywords
        keywords = [keyword for keyword, score in keywords]
        return keywords


# def convert_to_spacy_doc(self, tokenized_doc):
#     """Convert a list of tokens to a spaCy Doc."""
#     disabled_components = ['ner', 'lemmatizer']
#     doc = spacy.tokens.Doc(self.nlp.vocab, words=tokenized_doc)
#     for name, proc in self.nlp.pipeline:
#         if name not in disabled_components:
#             doc = proc(doc)
#     return doc

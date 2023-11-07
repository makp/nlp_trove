"""Functions for topic modeling."""

from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel


def map_tokens_to_integer_ids(tokenized_docs,
                              min_doc_freq=25,
                              max_doc_frac=0.9):
    """
    Build a dictionary from tokenized documents.

    When building a dictionary, filter out frequent and infrequent
    tokens. A dictionary is a mapping between words and their integer
    ids.
    """
    # Create a dictionary
    id2word = Dictionary(tokenized_docs)

    # Filter out certain tokens
    id2word.filter_extremes(no_below=min_doc_freq,
                            no_above=max_doc_frac)

    return id2word


def compute_coherence(lda_model, tokenized_docs, dictionary):
    """
    Compute and return the coherence of an LDA model.

    Coherence measures the degree of similarity between high scoring
    words. The higher the coherence score, the better.
    """
    coherence_model = CoherenceModel(model=lda_model,
                                     texts=tokenized_docs,
                                     dictionary=dictionary,
                                     coherence='c_v')

    return coherence_model.get_coherence()


def list_topics_for_bow_sorted(lda_model, bow):
    """
    Return the list of topics for a bow vector.

    The list is sorted by the probability of each topic.
    """
    topic_dist = lda_model.get_document_topics(bow,
                                               minimum_probability=None)
    return sorted(topic_dist, key=lambda x: x[1], reverse=True)


def get_top_n_docs_for_topic(series_bow,
                             lda_model,
                             topic_id,
                             num_docs=1):
    """Get the indexes of the top `num_docs` documents for a given topic."""
    lst = []
    for idx, bow in series_bow.items():
        topic_dist = dict(lda_model.get_document_topics(bow))
        prob = topic_dist.get(topic_id, 0)
        lst.append((idx, prob))
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst[:num_docs]


# def compute_perplexity(lda_model, test_corpus):
#     """
#     Compute and return the perplexity of a LDA model for a holdout
#     corpus.
#     Perplexity measures how well a probability model predicts a
#     sample. The lower the score, the better.
#     """
#     num_docs = len(test_corpus)
#     unnormalized_log_perplexity = 0
#     for doc_bow in test_corpus:
#         doc_topics = lda_model.get_document_topics(doc_bow,
#                                                    minimum_probability=0)
#         doc_probs = [prob for (_, prob) in doc_topics]
#         doc_perplexity = -np.dot(np.log(doc_probs), doc_probs)
#         unnormalized_log_perplexity += doc_perplexity
#     normalized_log_perplexity = unnormalized_log_perplexity / num_docs
#     perplexity = np.exp(normalized_log_perplexity)

#     return perplexity

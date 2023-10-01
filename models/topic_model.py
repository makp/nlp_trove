import os
from gensim.corpora import Dictionary
from gensim.models import LdaModel, CoherenceModel
# import numpy as np


def transform_tokenized_docs_to_bow_vectors(tokenized_docs,
                                            min_doc_freq=5,
                                            max_doc_fraction=0.9):
    """
    Transform tokenized documents into BoW vectors.
    """
    # Create a dictionary
    # Dictionaries map tokens to unique integer ids.
    id2word = Dictionary(tokenized_docs)

    # Filter out certain tokens
    id2word.filter_extremes(no_below=min_doc_freq,
                            no_above=max_doc_fraction)

    # Create a corpus of bow vectors
    # Each BoW vector is a list of (token_id, token_count) tuples
    bow_corpus = [id2word.doc2bow(tokens) for tokens in tokenized_docs]

    return id2word, bow_corpus


def compute_coherence(lda_model, tokenized_docs, dictionary):
    """
    Compute and return the coherence of an LDA model.
    Coherence measures the degree of similarity between high scoring
    words. The higher the coherence score, the better.
    """
    coherence_model = CoherenceModel(model=lda_model, texts=tokenized_docs,
                                     dictionary=dictionary, coherence='c_v')
    return coherence_model.get_coherence()


def compare_lda_models_with_multiple_k(tokenized_docs,
                                       bow_corpus,
                                       id2word,
                                       set_num_topics,
                                       dir_output='.',
                                       filename='lda_output.csv'):
    """
    Generate LDA models with different number of topics and compare
    them based on their coherence score. Write output to a file.
    """
    # Clear the file and add columns
    with open(filename, 'w') as f:
        f.write('')
        f.write('num_topic,coherence\n')

    for num_topics in set_num_topics:
        # Build an LDA model and calculate its coherence
        lda_model = LdaModel(corpus=bow_corpus,
                             id2word=id2word,
                             num_topics=num_topics)
        coherence = compute_coherence(lda_model, tokenized_docs, id2word)

        # Append output to csv file
        fullpath = os.path.join(dir_output, filename)
        with open(fullpath, 'a') as f:
            f.write(f'{num_topics},{coherence}\n')

    print('Mission accomplished')


def get_topic_distribution_for_bow(lda_model, bow):
    """
    Get the topic distribution for a given bow vector.
    """
    # Get the topic distribution as a list of (topic_id, prob) tuples
    topic_distribution = lda_model.get_document_topics(bow)

    # Sort the topic distribution in descending order of probability
    topic_distribution.sort(key=lambda x: x[1], reverse=True)

    return topic_distribution


def list_topics_for_bow_sorted(lda_model, bow):
    """
    Return the list of topics for a bow vector sorted in descending
    order of probability.
    """
    topic_dist = lda_model.get_document_topics(bow)
    return sorted(topic_dist, key=lambda x: x[1], reverse=True)


def get_top_n_docs_for_topic(lda_model, corpus, topic_id, num_docs=1):
    """
    Get the top `num_docs` documents in the corpus for a given topic.
    """
    lst = []
    for doc_id, bow in enumerate(corpus):
        topic_dist = dict(list_topics_for_bow_sorted(lda_model, bow))
        prob = topic_dist.get(topic_id, 0)
        lst.append((doc_id, prob))
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst[:num_docs]


# def compute_perplexity(lda_model, test_corpus):
#     """
#     Compute and return the perplexity of a LDA model on a held-out
#     test set.
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

from gensim import corpora, models
from gensim.models import CoherenceModel


def create_dictionary_and_corpus(docs, min_num=5, max_frac=0.9):
    """
    Create a dictionary and corpus from a list of documents, where
    each document is represented as a list of tokens.

    Dictionaries map tokens to unique integer ids.
    Corpora are collections of documents represented as bow vectors.
    Bow vectors are list of (token_id, token_count) tuples
    """
    # Create a dictionary
    dictionary = corpora.Dictionary(docs)

    # Filter out certain tokens
    # Drop tokens that appear in less than `min_num` of documents
    # Drop tokens that appear in more than `max_frac` of documents
    dictionary.filter_extremes(no_below=min_num, no_above=max_frac)

    # Create a corpus of bow vectors
    corpus = [dictionary.doc2bow(tokens) for tokens in docs]

    return dictionary, corpus


def run_lda(dictionary, corpus, num_topics=15):
    "Build a LDA model."

    # Run the LDA model
    lda_model = models.LdaModel(corpus=corpus,
                                num_topics=num_topics,
                                id2word=dictionary)

    topics = lda_model.print_topics(num_words=7)

    for topic in topics:
        print(topic)

    return lda_model


def compute_coherence(lda_model, docs, dictionary):
    """
    Compute and return the coherence of a LDA model.
    Coherence measures the degree of similarity between high scoring
    words. The higher the coherence score, the better.
    """
    coherence_model = CoherenceModel(model=lda_model, texts=docs,
                                     dictionary=dictionary, coherence='c_v')
    return coherence_model.get_coherence()


def compute_perplexity(lda_model, corpus):
    """
    Compute and return the perplexity of a LDA model.
    Perplexity measures how well a probability model predicts a
    sample. The lower the score, the better.
    """
    return lda_model.log_perplexity(corpus)


def compare_lda_models_multiple_k(docs,
                                  dictionary,
                                  corpus,
                                  set_num_topics,
                                  filename='lda_output.csv'):
    """
    Run LDA models with different number of topics and compare them.
    Write output to a file.
    """
    # Clear the file and add columns
    with open(filename, 'w') as f:
        f.write('')
        f.write('num_topic,coherence,perplexity\n')

    for num_topics in set_num_topics:
        # Build LDA model and calculate its coherence and perplexity
        lda_model = run_lda(dictionary, corpus, num_topics=num_topics)
        coherence = compute_coherence(lda_model, docs, dictionary)
        perplexity = compute_perplexity(lda_model, corpus)

        # Append output to csv file
        with open(filename, 'a') as f:
            f.write(f'{num_topics},{coherence},{perplexity}\n')

    print('Mission accomplished')


def get_topic_distribution_for_doc(lda_model, bow):
    """
    Get the topic distribution for a given document represented as a
    bow vector.
    """
    # Get the topic distribution as a list of (topic_id, prob) tuples
    topic_distribution = lda_model.get_document_topics(bow)

    # Sort the topic distribution in descending order of probability
    topic_distribution = sorted(topic_distribution,
                                key=lambda x: x[1], reverse=True)

    return topic_distribution


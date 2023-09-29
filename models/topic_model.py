from gensim import corpora, models


def run_lda(docs, num_topics=15, max_df=0.5, min_df=25):
    "Run LDA model on tokens"

    # Create a mapping between words and their integer ids
    dictionary = corpora.Dictionary(docs)

    # Filter out tokens
    dictionary.filter_extremes(no_below=min_df, no_above=max_df)

    # Create a corpus from documents
    corpus = [dictionary.doc2bow(tokens) for tokens in docs]

    # Run the LDA model
    lda_model = models.LdaModel(corpus=corpus,
                                num_topics=num_topics,
                                id2word=dictionary)

    topics = lda_model.print_topics(num_words=7)

    for topic in topics:
        print(topic)

    return lda_model


def get_topic_distribution(lda_model, tokens):

    # convert the abstract to bag-of-words format
    bag = lda_model.id2word.doc2bow(tokens)

    # get the topic distribution
    topic_distribution = lda_model.get_document_topics(bag, minimum_probability=0.1)

    # Sort the topic distribution in descending order of probability
    topic_distribution = sorted(topic_distribution,
                                key=lambda x: x[1], reverse=True)

    return topic_distribution

import pandas as pd

from preprocessing.process_text_to_spacy_docs import SeriesToDocs

# Create a Series for testing
data = {
    "10.1000/xyz123": "This is the text of the first article.",
    "10.1000/xyz124": "This is the text of the second article.",
    "10.1000/xyz125": "This is the text of the third article.",
    "10.1000/xyz126": "This is the text of the fourth article.",
}
series_test = pd.Series(data)

#
# Test `SeriesToDocs` class
#

# Create the converters to spaCy Doc objects
conv = SeriesToDocs(batch_size=2)

# Convert to spaCy Doc objects
idx, docbin = conv.convert_series_to_docs(series_test)

# Serialize the Doc objects
conv.convert_series_to_docs_and_serialize(
    series_test, "idx_test.pkl", "docbin_test.spacy"
)

# Deserialize the Doc objects
series_deserialized = conv.deserialize_docbin_as_series(
    "idx_test.pkl", "docbin_test.spacy"
)

type(series_deserialized.iloc[0])


#
# Test `SeriesToDocsWithAttributes` class
#

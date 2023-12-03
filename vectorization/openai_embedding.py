"""Routines for interacting with OpenAI's ADA2 embeddings."""

import os
from openai import OpenAI
import tiktoken
from helper_funcs.vectors import cosine_similarity

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CODING = 'cl100k_base'


def calc_num_tokens(string):
    """Calculate the number of tokens."""
    enc = tiktoken.get_encoding(EMBEDDING_CODING)
    num_tokens = len(enc.encode(string))
    return num_tokens


def create_embedding_openai(text, model=EMBEDDING_MODEL):
    """Create text embedding using OpenAI's ADA2 model."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[text],
        model=model)
    return response.data[0].embedding


def query_with_openai_embedding(query, ser_embs,
                                model=EMBEDDING_MODEL):
    """Query with OpenAI's ADA2 model."""
    query_emb = create_embedding_openai(query, model=model)
    scores = ser_embs.apply(lambda x:
                            cosine_similarity(x, query_emb))
    return scores.sort_values(ascending=False)

import pandas as pd
import json

from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PagedPDFSplitter

from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
import re
import time
import numpy as np
import json
import concurrent.futures

import os
import openai
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import datetime
from dateutil import parser
import re
from langchain.agents import initialize_agent,Tool
from langchain.llms import OpenAI
import concurrent.futures
import tiktoken

AI_LEARNED_DOCS_DIR = 'AI_learned_docs'
GPT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"

def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def rules_prompt(
    searchTerm: str,
    searchFiles: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from the JSON."""
    documents = search_among_documents(searchTerm, searchFiles)
    introduction = 'Use the below rules to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer\n\n"'
    message = introduction
    for document in documents:
        if (
            num_tokens(message + document['chunk'], model=EMBEDDING_MODEL)
            > token_budget
        ):
            break
        else:
            message += document['chunk']
    final_string = message
    return final_string

def search_among_documents(searchTerm,
    searchfiles=None,
    top_n: int = 100):

    search_term_vector = get_embedding(searchTerm, engine="text-embedding-ada-002")
    
    with open(searchfiles, 'r') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            item['embeddings'] = np.array(item['embeddings'])

        for item in data:
            item['similarities'] = cosine_similarity(item['embeddings'], search_term_vector)

        sorted_data = sorted(data, key=lambda x: x['similarities'], reverse=True)

    return sorted_data   

def getAnswerFromGPT(searchQuery,
    searchFiles: str,
    prev_history='',
    token_budget=2000):

    context = rules_prompt(searchTerm=searchQuery, searchFiles=searchFiles, token_budget=token_budget)
    
    myMessages = []

    myMessages.append({"role": "system", "content": "You are assistant and will answer user's query according to the rules provided."})
    myMessages.append({"role": "user", "content": context})
    myMessages.append({"role": "user", "content": "Please pay attention to the numbered lists. Please elaborate and list the relevant rules."})
    myMessages.append({"role": "user", "content": f'Question: {searchQuery}'})

    for i in prev_history:
        myMessages.append({"role": "user", "content": i['user']})
        myMessages.append({"role": "assistant", "content": i['AI']})
    myMessages.append({"role": "user", "content": searchQuery})
    
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=myMessages,
        temperature=0,
        max_tokens= 400
    )
    print(f'Final number of tokens: {response["usage"]["total_tokens"]}')
    print(f'This cost: ${response["usage"]["total_tokens"] * 0.002 / 1000}')

    return response['choices'][0]['message']['content']
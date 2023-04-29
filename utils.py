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
# openai.api_key = "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"
# openai.api_key = "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"
openai.api_key = "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"
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import datetime
from dateutil import parser
import re
from langchain.agents import initialize_agent,Tool
from langchain.llms import OpenAI
import concurrent.futures
from langdetect import detect


def search_among_documents(searchTerm,searchfiles=None,docsDir='AI_learned_docs'):

    search_term_vector = get_embedding(searchTerm, engine="text-embedding-ada-002")
    

    with open(searchfiles, 'r') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            item['embeddings'] = np.array(item['embeddings'])

        for item in data:
            item['similarities'] = cosine_similarity(item['embeddings'], search_term_vector)

        sorted_data = sorted(data, key=lambda x: x['similarities'], reverse=True)
        top_5_similarities = [{"similarityValue":item['similarities'],"chunk":item['chunk'].replace('...','')} for item in sorted_data[:7] if item['similarities']>0.68]
        if len(top_5_similarities) == 0:
            top_5_similarities = [{"similarityValue":item['similarities'],"chunk":item['chunk'].replace('...','')} for item in sorted_data[:3]]
        return top_5_similarities
    


def getAnswerFromGPT(context,searchQuery,prev_history=''):
    
    myMessages = []
    myMessages.append({"role": "system", "content": "You are assistant and will answer user's query according to information provided."})
    myMessages.append({"role": "user", "content": "Data: ( {} )\n\nI will ask you question and you will answer me according to the provided Data. If you do not know the answer just say I dont know. Do not come up with your own answers.".format(context)})
    myMessages.append({"role": "assistant", "content": "Okay sure!"})

    for i in prev_history:
        myMessages.append({"role": "user", "content": i['user']})
        myMessages.append({"role": "assistant", "content": i['AI']})
    myMessages.append({"role": "user", "content": searchQuery})
    
  

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=myMessages,
    max_tokens= 400,
    )
    return response['choices'][0]['message']['content']
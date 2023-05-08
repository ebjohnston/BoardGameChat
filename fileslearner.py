import os
import pandas as pd
from doc_learner import *
import time
def get_file_type(file_path):
    return os.path.splitext(file_path)[1][1:].lower()

filesToLearn = os.listdir('Files')
filesAlreadyLearned = os.listdir('AI_learned_docs')


for i in filesToLearn:
    filepath = 'Files/'+i
    fileType = get_file_type(i)
    print("learning ",i)



    ## Check if alreayd learned or not
    tolearnFileNameForCheckingOnly = os.path.splitext(os.path.basename(i))[0]+'.json'
    if tolearnFileNameForCheckingOnly in filesAlreadyLearned:
        print("file {} is already learned. [skipping]".format(i))
        print()
        continue
    
    if fileType == 'pdf':
            print("executing: pdf",flush=True)
            learn = pdf_reader_and_embeddings_generator(filepath)
            print("file {} learned successfully...".format(i))
            
    elif fileType == 'docx':
        print("executing: pdf",flush=True)
        learn = docx_reader_and_embeddings_generator(filepath)
        print("file {} learned successfully...".format(i))
        
    
    elif fileType == 'xlsx':
        learn = excel_reader_and_embeddings_generator(filepath)
        print("file {} learned successfully...".format(i))
    
    elif fileType == 'csv':
        learn = csv_reader_and_embeddings_generator(filepath)
        print("file {} learned successfully...".format(i))
    
    elif fileType == 'txt':
        learn = txt_reader_and_embeddings_generator(filepath)
        print("file {} learned successfully...".format(i))
    else:
         print("file format not supported, only pdf,txt,docx,xlsx,csv are allowed")


    print()
    time.sleep(2)
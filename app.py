from dotenv import load_dotenv
import os
import argparse
from docx import Document
import pdfplumber
from textwrap import wrap
import json
import re
import requests
import pinecone
import openai
import numpy as np

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone.init(api_key=pinecone_api_key, environment="us-east1-gcp")


def create_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def read_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_doc(file_path):
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def main():
    parser = argparse.ArgumentParser(description='Read text from different file formats')
    parser.add_argument('file', help='Path to the file to read text from')
    args = parser.parse_args()

    input_folder = "working"
    file_path = os.path.join(input_folder, args.file)
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == '.txt':
        text = read_txt(file_path)
    elif file_ext == '.doc' or file_ext == '.docx':
        text = read_doc(file_path)
    elif file_ext == '.pdf':
        text = read_pdf(file_path)
    else:
        print(f"Error: The file format {file_ext} is not supported.")
        return

    chunks = wrap(text, 2000)
    embeddings = []
    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    index_name = "document-chunks"
    pinecone.init(api_key=pinecone_api_key, environment="us-east1-gcp")
    if index_name not in pinecone.list_indexes():
        embeddings = np.array(embeddings)
        dimension = embeddings[0].shape[0]
        pinecone.create_index(index_name, metric="cosine", dimension=dimension)

    index = pinecone.Index('document-chunks')

    upserts = [(f"chunk-{i}", embedding) for i, embedding in enumerate(embeddings)]
    index.upsert(vectors=upserts)

       # Prompt user for a question
    question = input("Enter your question: ")
    
    # Search for the nearest chunk and get its ID
    nearest_chunk_id = search(question)
    
    # Get the chunk index from the ID
    chunk_index = int(nearest_chunk_id.split("-")[-1])
    
    # Retrieve the corresponding text chunk from the 'chunks' list
    nearest_chunk_text = chunks[chunk_index]
    
    # Use GPT-3 to answer the question based on the retrieved chunk
    prompt = f"The following text contains the information you are looking for:\n{nearest_chunk_text}\n\nQuestion: {question}\nAnswer:"
    answer = gpt3_completion(prompt)
    
    # Print the answer
    print("Answer:", answer)











def search(query, index_name="document-chunks"):
    embedding = create_embedding(query)
    pinecone.init(api_key=pinecone_api_key, environment="us-east1-gcp")
    index = pinecone.Index(index_name)
    results = index.query(queries=[embedding], top_k=1)
    nearest_chunk_id = results["results"][0]["matches"][0]["id"]
    return nearest_chunk_id




def gpt3_completion(prompt):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message









if __name__ == "__main__":
    main()
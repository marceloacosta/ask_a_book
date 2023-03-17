# Ask a Book
Ask a Book is a Python application that reads text from various file formats, creates embeddings using OpenAI's text-embedding-ada-002 model, stores the embeddings in Pinecone, and answers questions related to the text using GPT-3.

## Features
Reads text from .txt, .doc, .docx, and .pdf files.
Creates embeddings using OpenAI's text-embedding-ada-002 model.
Stores the embeddings in Pinecone.
Answers questions related to the text using GPT-3.
## Requirements
Python 3.6+
Python packages: dotenv, os, argparse, docx, pdfplumber, textwrap, json, re, requests, pinecone, openai, numpy.
## Installation
Clone the repository:
<pre>

git clone https://github.com/marceloacosta/ask_a_book.git
</pre>
Change directory to the project folder:
<pre>
cd ask_a_book
</pre>
## Install the required packages:
bash
Copy code
pip install -r requirements.txt
Create a .env file in the project root directory with the following contents:
<pre>
OPENAI_API_KEY= your_openai_api_key
PINECONE_API_KEY= your_pinecone_api_key
</pre>
Replace <your_openai_api_key> and <your_pinecone_api_key> with your respective API keys.

Create a folder named working in the project root directory. Place the file you want to read text from in this folder.
## Usage
Run the script with the following command:
<pre>python app.py <file></pre>
Replace <file> with the name of the file you want to read text from. The file should be located in the working directory.

Enter your question when prompted:
<pre>
Enter your question: <your_question></pre>
Replace <your_question> with the question you want to ask based on the text in the file.

The script will return an answer based on the text in the file:
<pre>
Answer: <answer>
</pre>

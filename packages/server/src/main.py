from dotenv import load_dotenv

load_dotenv()

from os import environ

import chromadb
from chromadb.config import Settings
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from pydantic import BaseModel

from .llm.utils import process_llm_response

COLLECTION = "confluence_collection"
chroma_client = chromadb.HttpClient(settings=Settings(allow_reset=True))
huggingface_embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectordb = Chroma(
    collection_name=COLLECTION,
    embedding_function=huggingface_embeddings,
    client=chroma_client,
)
vectordb_retriever = vectordb.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectordb_retriever,
    return_source_documents=True,
)

app = FastAPI()


class QueryModel(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/retrieve")
async def retrieve(body: QueryModel):
    docs = vectordb_retriever.get_relevant_documents(body.query)

    for doc in docs:
        page_id = doc.metadata["source"].split("page_")[-1].split(".txt")[0]
        doc.metadata[
            "source"
        ] = f"{environ['ATLASSIAN_URL']}/wiki/spaces/{environ['ATLASSIAN_SPACE']}/pages/{page_id}"

    # Return the docs
    return {"message": docs}


@app.post("/chat")
async def chat(body: QueryModel):
    llm_response = qa_chain(body.query)
    response = process_llm_response(llm_response)

    # Return chat response
    return {"message": response}

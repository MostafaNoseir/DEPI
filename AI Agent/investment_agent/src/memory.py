# src/memory.py
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Internal company strategy docs
docs = [
    Document(
        page_content="Microsoft target buy price is 350 USD.",
        metadata={"company": "Microsoft"}
    ),
    Document(
        page_content="Apple target buy price is 180 USD.",
        metadata={"company": "Apple"}
    ),
    Document(
        page_content="Microsoft historical average stock price was around 280 USD in previous years.",
        metadata={"company": "Microsoft", "type": "historical"}
    ),
]

vector_db = FAISS.from_documents(docs, embeddings)

@tool
def retrieve_strategy(query: str) -> str:
    """Retrieve internal target buy price for a company."""
    results = vector_db.similarity_search(query, k=1)

    if not results:
        return "No strategy found."

    return results[0].page_content
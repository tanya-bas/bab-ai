import os
import torch
from dotenv import load_dotenv
from pinecone import Pinecone
from transformers import AutoTokenizer, AutoModel


# Load environment variables
load_dotenv()

# Constants
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = "pension-doc-index"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Load tokenizer and model for generating query embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


# Query the Pinecone index
def query_pinecone_index(query_text):
    """
    Query the Pinecone index with a text query and return results.
    """
    # Generate query embedding
    inputs = tokenizer(query_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        query_embedding = model(**inputs).last_hidden_state.mean(dim=1)[0].tolist()

    # Perform the query
    results = index.query(
        vector=query_embedding,
        top_k=10,  # Number of top results to return
        include_metadata=True,
    )

    # Filter results based on a threshold
    threshold = 0.5
    filtered_results = [
        match for match in results["matches"] if match["score"] >= threshold
    ]

    if not filtered_results:
        return "No relevant results found."
    else:
        for match in filtered_results:
            return f"ID: {match['id']}, Text: {match['metadata']['text']}, Score: {match['score']}"


# Main script
if __name__ == "__main__":
    # Example query
    query_text = "Какви документи са необходими за получаване на пенсия в България?"
    query_pinecone_index(query_text)

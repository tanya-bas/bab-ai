import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Constants
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = "pension-doc-index"  
EMBEDDING_DIMENSION = 384
BATCH_SIZE = 100

# Initialize Pinecone
def initialize_pinecone():
    """
    Initialize Pinecone and return the index.
    """
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV
            )
        )
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")
    return pc.Index(INDEX_NAME)

# Upsert data into Pinecone
def upsert_data(index, data_file="data/processed_data/embeddings.json"):
    """
    Load embeddings from a file and upsert them into Pinecone in batches.
    """
    with open(data_file, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)

    to_upsert = [
        (passage_id, data["embedding"], {"text": data["text"]})
        for passage_id, data in embeddings_data.items()
    ]

    for i in range(0, len(to_upsert), BATCH_SIZE):
        batch = to_upsert[i:i + BATCH_SIZE]
        index.upsert(vectors=batch)
        print(f"Upserted batch {i // BATCH_SIZE + 1} with {len(batch)} vectors.")
    print("All data upserted successfully.")

# Main script
if __name__ == "__main__":
    # Initialize Pinecone and get the index
    index = initialize_pinecone()

    # Uncomment the following line to upsert data
    upsert_data(index)
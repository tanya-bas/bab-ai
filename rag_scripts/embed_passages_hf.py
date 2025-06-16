import os
import json
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import torch
from dotenv import load_dotenv

def split_text_into_passages(file_path, chunk_size=200):
    """Split raw text into smaller passages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split text into chunks
    words = text.split()
    passages = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return passages

def save_passages_to_json(passages, output_file):
    """Save passages to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(passages, json_file, ensure_ascii=False, indent=4)

def generate_embeddings(passages, tokenizer, model):
    embeddings = []
    for passage in passages:
        # Tokenize with padding and truncation
        inputs = tokenizer(passage, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            # Retrieve the hidden states (first element of the outputs tuple)
            hidden_states = outputs[0]  # Access the first item for hidden states
            # Perform mean pooling on the hidden states
            embedding = hidden_states.mean(dim=1).squeeze().cpu().numpy()
        embeddings.append(embedding)
    return embeddings

def save_embeddings_to_file(embeddings, output_file):
    """Save embeddings to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(embeddings, json_file, ensure_ascii=False, indent=4)

# Load environment variables (if needed for other purposes)
load_dotenv()

# # Initialize Hugging Face model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
# model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

offload_folder = "Users/tetianabas/llama_hackathon/llama_hackathon/data/raw_data/processed_data"
os.makedirs(offload_folder, exist_ok=True)
model = AutoModelForCausalLM.from_pretrained(
    "sambanovasystems/SambaLingo-Bulgarian-Base",
    device_map="auto",
    torch_dtype="auto",
    offload_folder=offload_folder
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("sambanovasystems/SambaLingo-Bulgarian-Base")
tokenizer.pad_token = tokenizer.eos_token or tokenizer.add_special_tokens({'pad_token': '[PAD]'})


# Paths to input and output files
raw_text_file = "/Users/tetianabas/llama_hackathon/llama_hackathon/data/raw_data/processed_data/extracted_cleaned_text.txt"  # Updated to use the cleaned text
output_dir = "/Users/tetianabas/llama_hackathon/llama_hackathon/data/raw_data/processed_data"  # Directory for output files

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define output file paths
passages_file = os.path.join(output_dir, "split_passages.json")
embeddings_file = os.path.join(output_dir, "embeddings.json")

# Split text into passages
passages = split_text_into_passages(raw_text_file)

# Save passages to JSON
save_passages_to_json(passages, passages_file)

# Generate embeddings
embeddings = generate_embeddings(passages, tokenizer, model)

# Save embeddings to JSON
save_embeddings_to_file(embeddings, embeddings_file)

print(f"Passages saved to '{passages_file}'.")
print(f"Embeddings saved to '{embeddings_file}'.")
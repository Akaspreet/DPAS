from transformers import AutoTokenizer, AutoModel
import torch

def initialize_llm():
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return tokenizer, model

def encode_query(tokenizer, model, query):
    inputs = tokenizer(query, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def search_properties(df, query_embedding, top_k=5):
    # Implement similarity search logic here
    # Return top_k most similar properties
    pass
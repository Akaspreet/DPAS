from sentence_transformers import SentenceTransformer
import torch

class LLMHandler:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode_query(self, query):
        return self.model.encode(query, convert_to_tensor=True)

    def encode_properties(self, df):
        # Create a combined string of all available text columns
        text_columns = ['address', 'postcode', 'district', 'sector', 'town', 'region']
        property_texts = df[text_columns].fillna('').agg(' '.join, axis=1).tolist()
        return self.model.encode(property_texts, convert_to_tensor=True)

    def search_properties(self, query_embedding, property_embeddings, top_k=5):
        similarities = torch.cosine_similarity(query_embedding.unsqueeze(0), property_embeddings)
        top_indices = similarities.argsort(descending=True)[:top_k]
        return top_indices.tolist()
import pandas as pd

class SearchEngine:
    def __init__(self, df, llm_handler):
        self.df = df
        self.llm_handler = llm_handler
        try:
            self.property_embeddings = self.llm_handler.encode_properties(df)
        except Exception as e:
            print(f"Error encoding properties: {str(e)}")
            self.property_embeddings = None

    def search(self, query, parameters, top_k=5):
        if self.property_embeddings is None:
            return pd.DataFrame()  # Return an empty DataFrame if encoding failed
        
        # Combine query and parameters into a single search string
        search_string = f"{query} {' '.join([f'{k}:{v}' for k, v in parameters.items()])}"
        query_embedding = self.llm_handler.encode_query(search_string)
        top_indices = self.llm_handler.search_properties(query_embedding, self.property_embeddings, top_k)
        return self.df.iloc[top_indices]
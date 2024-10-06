import json
import pandas as pd
from datetime import datetime

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    return df

def preprocess_data(df):
    # Convert date columns to datetime
    date_columns = ['date_created', 'date_updated', 'latest_sale_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Handle missing values in numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Handle the lease_term column
    if 'lease_term' in df.columns:
        df['lease_term'] = df['lease_term'].apply(parse_lease_term)
    
    return df

def parse_lease_term(lease_term):
    if isinstance(lease_term, dict):
        # If it's a dictionary, try to extract relevant information
        if 'term' in lease_term:
            return lease_term['term']
        elif 'term_duration_years' in lease_term:
            return f"{lease_term['term_duration_years']} years"
        else:
            return json.dumps(lease_term)  # Convert dict to string if no relevant info found
    elif isinstance(lease_term, list):
        # If it's a list, convert to string
        return json.dumps(lease_term)
    else:
        # If it's already a simple type (string, int, etc.), return as is
        return lease_term
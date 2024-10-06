import streamlit as st
import pandas as pd
import logging
from src.data_loader import load_data, preprocess_data
from src.gemini_handler import GeminiHandler
from src.llm_handler import LLMHandler
from src.search_engine import SearchEngine
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Dynamic Property Analysis and Search", layout="wide")

st.title("Dynamic Property Analysis and Search")

# Load and preprocess data
@st.cache_data
def load_and_preprocess_data():
    try:
        file_path = 'data/property_data.csv'
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        # Load the data
        df = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The data file is empty.")
        
        # Check for expected columns
        expected_columns = [
            'date_created.date', 'latest_sale_price', 'latest_sale_date',
            'secondary_latest_sale_date.lr.date'
        ]
        for col in expected_columns:
            if col not in df.columns:
                st.warning(f"Expected column '{col}' is missing in the data.")

        df = preprocess_data(df)
        df['lease_term'] = df['lease_term'].astype(str)  # Convert lease_term to string

        # Ensure date columns are in datetime format
        date_columns = [col for col in df.columns if 'date' in col]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        return df
    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Data loading error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

df = load_and_preprocess_data()

if df is not None:
    st.sidebar.success(f"Data loaded successfully. Shape: {df.shape}")
    st.sidebar.success("Data preprocessed successfully.")
else:
    st.stop()

# Initialize handlers and search engine
@st.cache_resource
def initialize_handlers():
    try:
        gemini_handler = GeminiHandler(st.secrets["GEMINI_API_KEY"])
        llm_handler = LLMHandler()
        search_engine = SearchEngine(df, llm_handler)
        return gemini_handler, llm_handler, search_engine
    except Exception as e:
        st.error(f"Error initializing handlers or search engine: {str(e)}")
        return None, None, None

gemini_handler, llm_handler, search_engine = initialize_handlers()

if None in (gemini_handler, llm_handler, search_engine):
    st.stop()

st.sidebar.success("Handlers and search engine initialized successfully.")

# Main query input
query = st.text_input("Enter your query (e.g., 'Find 2BHK houses in London' or 'Analyze property prices over time'):")

if query:
    try:
        # Use Gemini to interpret the query
        with st.spinner("Interpreting your query..."):
            interpretation = gemini_handler.interpret_query(query)
        
        st.subheader("Query Interpretation")
        st.json(interpretation)
        
        if interpretation['intent'] == 'search':
            # Perform property search
            with st.spinner("Searching for properties..."):
                results = search_engine.search(query, interpretation['parameters'])
            
            st.subheader("Search Results")
            if not results.empty:
                st.dataframe(results)
            else:
                st.info("No matching properties found.")
        
        elif interpretation['intent'] == 'analysis':
            # Generate and execute analysis
            with st.spinner("Generating and executing analysis..."):
                result = gemini_handler.generate_and_execute_analysis(query, interpretation['parameters'], df)
                
                st.subheader("Analysis Result")

                # Display the plot images
                def display_images_from_folder(folder_path):
                    # List all files in the folder
                    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    
                    # Sort files to ensure consistent order
                    image_files.sort()
                    
                    # Check if there are images to display
                    if not image_files:
                        st.write("No images found in the folder.")
                        return
                    
                    # Display each image
                    # for image_file in image_files:
                    #     image_path = os.path.join(folder_path, image_file)
                    #     st.image(image_path, caption=image_file, use_column_width=True)

                    image_file = 'result.png'
                    image_path = os.path.join(folder_path, image_file)
                    st.image(image_path, caption=image_file, use_column_width=True)

                # Set the folder path where your images are stored
                folder_path = 'graphs/'  # Change this to your folder path

                # Display the images
                display_images_from_folder(folder_path)
                # st.image(graphs/result.png, caption=image_file, use_column_width=True)
    
    except Exception as e:
        st.error(f"Error processing your query: {str(e)}")

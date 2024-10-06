# Dynamic Property Analysis and Search

This project provides a Streamlit-based web application for dynamic property analysis and search. It uses machine learning models and natural language processing to interpret user queries, search property data, and perform analyses.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Project Structure](#project-structure)
4. [Features](#features)
5. [Dependencies](#dependencies)
6. [Configuration](#configuration)
7. [Results](#results)
8. [Contributing](#contributing)
9. [License](#license)

## Installation

1. Clone the repository:
2. Create a virtual environment (optional but recommended):
3. Install the required dependencies:
4. Set up your Gemini API key:
- Create a `.streamlit/secrets.toml` file in the project root
- Add your Gemini API key:
  ```
  GEMINI_API_KEY = "your_api_key_here"
  ```

## Usage

1. Ensure you have the property data CSV and .json file in the `data` directory:
2. Run the Streamlit app: using command (streamlit run app.py)
3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Enter your property search or analysis query in the text input field.

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Source Folder of all the major functionalities
- `data_loader.py`: Functions for loading and preprocessing data
- `gemini_handler.py`: Handles interactions with the Gemini API
- `llm_handler.py`: Manages the language model for embeddings and similarity search
- `search_engine.py`: Implements the property search functionality
- `data/`: Directory for storing the property data CSV and .json file
- `graphs/`: Directory where analysis graphs are saved

## Features

- Natural language query interpretation
- Property search based on various parameters
- Dynamic property analysis with visualizations
- Integration with Gemini API for advanced query understanding

## Dependencies

- streamlit
- pandas
- google-generativeai
- sentence-transformers
- matplotlib
- sentence-transformers
- torch

For a complete list, see `requirements.txt`.

## Configuration

- Gemini API key: Set in `.streamlit/secrets.toml`
- Data file path: Update in `app.py` if necessary

## Results

[You should add a section here describing the types of results users can expect, including example queries and their outputs. Consider adding screenshots or GIFs demonstrating the application in action.]

To showcase the results:
![average_prices_over_time](https://github.com/user-attachments/assets/d9fe3119-5b68-42e7-a517-0aedc9ecccb5)
![average_sale_price_per_quarter](https://github.com/user-attachments/assets/439727a4-f5d6-4f63-8c2f-9c7cd4b249af)
![average_sale_price_per_year](https://github.com/user-attachments/assets/546a94e6-c557-494b-b57f-198bd53d9d08)
![change_in_propertytype_over_the_years](https://github.com/user-attachments/assets/cc314374-2173-42c7-b837-94455d4fddd0)
![district_counts](https://github.com/user-attachments/assets/d320025b-e110-432a-ab58-df943cfe3bf7)
![price_over_time](https://github.com/user-attachments/assets/aab67126-ba55-470c-b441-49d34b8c3a81)
![property_prices_over_time](https://github.com/user-attachments/assets/9e469048-1b07-4027-a25b-54334807e76b)
![result](https://github.com/user-attachments/assets/0f1026fc-5838-4e84-9bb6-aa0e10ebf25b)
![prices](https://github.com/user-attachments/assets/55c087bb-8103-4246-b170-d44ef0b77829)





# API Reference

## GeminiHandler

### `__init__(self, api_key: str)`

Initializes the GeminiHandler with the Gemini API key.

**Parameters:**
- `api_key` (str): The Gemini API key

### `interpret_query(self, query: str) -> Dict`

Interprets a user query using the Gemini API.

**Parameters:**
- `query` (str): The user's natural language query

**Returns:**
- Dict: A dictionary containing:
  - `intent` (str): Either "search" or "analysis"
  - `parameters` (Dict): Extracted parameters from the query

**Example:**
```python
handler = GeminiHandler("your_api_key")
result = handler.interpret_query("Find 2BHK houses in London")
print(result)
# Output: {"intent": "search", "parameters": {"bedrooms": 2, "location": "London"}}


engine = SearchEngine(property_data, llm_handler)
results = engine.search("2BHK houses in London", {"bedrooms": 2, "location": "London"})
print(results)

4. In `usage.md`, provide detailed instructions and examples:

```markdown
# Usage Guide

## Starting the Application

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the Streamlit app:


3. Your default web browser should open automatically. If not, go to the URL provided in the terminal (usually `http://localhost:8501`).

## Performing a Property Search

1. In the main input field, enter a natural language query for property search. For example:
- "Find 2BHK apartments in London under £500,000"
- "Show me houses with a garden in Manchester"

2. Press Enter or click outside the input field to submit your query.

3. The application will interpret your query and display the interpretation.

4. Below the interpretation, you'll see the search results displayed in a table.

## Conducting Property Analysis

1. In the main input field, enter a natural language query for property analysis. For example:
- "Analyze property price trends in Birmingham over the last 5 years"
- "Compare average prices of 1BHK vs 2BHK apartments in Liverpool"

2. Press Enter or click outside the input field to submit your query.

3. The application will interpret your query and display the interpretation.

4. Below the interpretation, you'll see the analysis results, which may include graphs, charts, or textual insights.

## Tips for Effective Queries

- Be as specific as possible in your queries to get more accurate results.
- You can mention multiple criteria in a single query, such as location, number of bedrooms, price range, etc.
- For analysis queries, specifying a time range or comparison factors can yield more insightful results.


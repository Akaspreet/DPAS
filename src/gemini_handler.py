import json
import logging
import google.generativeai as genai
import os
import subprocess
import pandas as pd
from typing import Dict

class GeminiHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logging.basicConfig(level=logging.DEBUG)

    def interpret_query(self, query: str) -> Dict:
        prompt = f"""
        Interpret the following user query about property search or analysis:
        "{query}"
        
        Provide a JSON response with the following structure:
        {{
            "intent": "search" or "analysis",
            "parameters": {{
                // Extracted parameters from the query
                // Include 'bedrooms' if BHK or RK is mentioned
            }}
        }}

        Note: Interpret BHK (Bedroom, Hall, Kitchen) and RK (Room, Kitchen) as follows:
        - 1BHK, 1 BHK, 1bhk, 1 bhk: 1 bedroom
        - 2BHK, 2 BHK, 2bhk, 2 bhk: 2 bedrooms
        - 3BHK, 3 BHK, 3bhk, 3 bhk: 3 bedrooms
        - 4BHK, 4 BHK, 4bhk, 4 bhk: 4 bedrooms
        - 5BHK, 5 BHK, 5bhk, 5 bhk: 5 bedrooms
        - 6BHK, 6 BHK, 6bhk, 6 bhk: 6 bedrooms
        - 7BHK, 7 BHK, 7bhk, 7 bhk: 7 bedrooms
        - 8BHK, 8 BHK, 8bhk, 8 bhk: 8 bedrooms
        - 9BHK, 9 BHK, 9bhk, 9 bhk: 9 bedrooms
        - 10BHK, 10 BHK, 10bhk, 10 bhk: 10 bedrooms
        - 1RK, 1 RK, 1rk, 1 rk: 1 bedroom (considered as a studio apartment)

        Ensure that your response is a valid JSON object and nothing else.
        """
        try:
            logging.debug(f"Sending prompt to Gemini API: {prompt}")
            response = self.model.generate_content(prompt)
            response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
            response_text = response_text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:].strip()
            if response_text.endswith('```'):
                response_text = response_text[:-3].strip()
            
            logging.debug(f"Cleaned response text: {response_text}")
            
            if not response_text:
                raise ValueError("Empty response from API")
            
            parsed_response = json.loads(response_text)
            
            if 'intent' not in parsed_response or 'parameters' not in parsed_response:
                raise ValueError("Response is missing required fields")
            
            return parsed_response
        except Exception as e:
            logging.error(f"Error interpreting query: {str(e)}")
            raise ValueError(f"Error interpreting query: {str(e)}")

    def generate_and_execute_analysis(self, query: str, parameters: Dict, df: pd.DataFrame) -> Dict:
        try:
            # Generate the code using Gemini
            prompt = f"""
            Generate Python code to analyze the following data:
            {df.head().to_json()}

            The code should perform the analysis based on the query: "{query}"
            Use print statements to output any relevant analysis results or insights.
            Ensure that the code includes the necessary imports and saves the plots to the 'graphs' directory.
            If user want to analyze by using the time in prompts plot the graph then by extracting only years from the columns and the data in column where you need to fetch year, date or anything is of this format %Y-%m-%dT%H:%M:%S.%fZ.
            Like I tell you if you want to extract year so use like this df['latest_sale_year'] = pd.to_datetime(df['latest_sale_date'], format='%Y-%m-%dT%H:%M:%S.%fZ').dt.year .
            my data is on location so
            df = pd.read_csv('data/property_data.csv') 
            please make sure that if u need data in json format it is present in location 'data/properties.json'
            and if u need data in csv format it is in location 'data/property_data.csv'
            so you can write this.
            Always save the image output with the name result.png as in graphs folder like plt.savefig('graphs/result.png') if result.png already exist overwrite it.
            these are the columns name in my csv file (address	postcode	street	lat	long	district	cc	active	sector	town	building_number	district_name	sector_name	update_required	building_name	sub_building_name	latest_sale_price	latest_price_ppsqft	epc_reference	epc_date	avm	avm_accuracy	latest_new_build	latest_tenure	latest_lr_reference	snl	habitable_rooms	tci_avm	tci_accuracy	floor_level	lease_term	locked	region	paf_postcode	paf_postcode_type	paf_udprn	paf_address_key	paf_locality_key	postcode_area	rpp_key	water_proximity_400	floor_level_discrete	fuel_source	heating	walls	listed_building_grade	roof_type	tree_proximity_10	tree_proximity_5	age_band	_id.oid	uprn.numberLong	main_reference.numberLong	secondary_bedrooms.listings.numberDouble	secondary_bedrooms.dvm	secondary_bathrooms.listings.numberDouble	secondary_bathrooms.dvm	secondary_receptions.listings.numberDouble	secondary_receptions.dvm	secondary_area.listings.numberDouble	secondary_area.epc	secondary_area.dvm	secondary_property_type.epc	secondary_property_type.lr	secondary_property_type.listings.numberDouble	secondary_property_type.dvm	secondary_num_floors.epc.numberDouble	secondary_num_floors.dvm.numberDouble	secondary_latest_sale_date.lr.date	secondary_latest_sale_date.listings.numberDouble	secondary_latest_sale_price.lr	secondary_latest_sale_price.listings.$numberDouble	secondary_new_build.listings	secondary_new_build.lr	secondary_tenure.listings	secondary_tenure.lr	coordinates.type	coordinates.coordinates	latest_sale_date	epc_values.current_energy_efficiency	epc_values.potential_energy_efficiency	epc_values.environment_impact_current	epc_values.environment_impact_potential	date_created.date	date_updated.date	street_reference.numberLong	building_reference.numberLong	secondary_sub_property_type.dvm.numberDouble	secondary_sub_property_type.epc.numberDouble	secondary_sub_property_type.listings.numberDouble
)
            """
            logging.debug(f"Sending prompt to Gemini API: {prompt}")
            response = self.model.generate_content(prompt)
            response_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
            response_text = response_text.strip()
            
            if response_text.startswith('```python'):
                response_text = response_text[7:].strip()
            if response_text.endswith('```'):
                response_text = response_text[:-3].strip()
            
            logging.debug(f"Generated code: {response_text}")

            code = response_text
            lines = code.splitlines()

            # Initialize a flag to track if the line containing "on" has been removed
            removed = False

            # Create a new list to hold the modified lines
            new_lines = []

            # Iterate through each line
            for line in lines:
                if "on" in line and not removed:
                    removed = True  # Set the flag to indicate we've removed the line
                    continue  # Skip this line
                new_lines.append(line)  # Add the line to the new list

            # Join the modified lines back into a single string
            modified_code = "\n".join(new_lines)







            # print(response_text)
            # Remove lines containing "on"
            # code_lines = response_text
            # code_lines = code_lines[1:] if code_lines[0].startswith("on") else code_lines

            # Join the modified lines back into a single string
            # modified_code = "\n".join(code_lines)
            cleaned_code = modified_code
           

            # Save the cleaned code to temp.py
            with open('temp.py', 'w') as f:
                # f.write("import pandas as pd\n")
                # f.write("import matplotlib.pyplot as plt\n")
                # f.write(f"df = pd.read_json('data/properties.json')\n")
                f.write(cleaned_code)
            
            # Execute the generated code
            result = subprocess.run(['python', 'temp.py'], capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"Error executing temp.py: {result.stderr}")

            # Collect all generated plot files
            plot_files = [os.path.join('graphs', f) for f in os.listdir('graphs') if f.endswith('.png')]
            
            return {
                'plot_files': plot_files,
                'code': cleaned_code,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            logging.error(f"Error generating and executing analysis: {str(e)}")
            raise ValueError(f"Error generating and executing analysis: {str(e)}")

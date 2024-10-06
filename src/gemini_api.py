import google.generativeai as genai

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def generate_code(model, prompt):
    response = model.generate_content(prompt)
    return response.text
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

user_input=input("Enter your query: ")

response = model.generate_content(user_input)
print(response.text)


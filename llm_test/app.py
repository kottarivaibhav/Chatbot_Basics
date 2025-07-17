import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Initialize the LangChain model with API key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=api_key,
    temperature=0.7
)

user_input = input("Enter your query: ")
response = llm.invoke(user_input)

# Get clean text response
try:
    clean_response = response.content
    print(clean_response)
except AttributeError:
    # Fallback if content attribute doesn't exist
    print(str(response).split("content='")[1].split("', additional_kwargs")[0])
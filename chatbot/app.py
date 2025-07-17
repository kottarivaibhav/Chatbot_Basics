import streamlit as st
import os
import google.generativeai as genai
import dotenv

st.title("Gemini Bot")

# Load environment variables from .env file
dotenv.load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("GOOGLE_API_KEY environment variable not set")
    st.stop()

genai.configure(api_key=api_key)

# Select the model
model = genai.GenerativeModel('gemini-2.5-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me Anything"
        }
    ]
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query):
    response = model.generate_content(query)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # Storing the assistant Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )
        
# Accept user input
query = st.chat_input("What's up?")

# Calling the Function when Input is Provided
if query:
    llm_function(query)
    st.rerun()  # Force immediate refresh to show new messages

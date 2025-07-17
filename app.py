import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import os.path

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)

# Models for different purposes
text_model = genai.GenerativeModel('gemini-2.5-flash')
vision_model = genai.GenerativeModel('gemini-2.5-pro')

def analyze_image(image_path, prompt="Explain this image"):
    """Analyze an image using Gemini Pro Vision"""
    try:
        if not os.path.exists(image_path):
            return f"Error: Image file '{image_path}' not found."
        
        image = PIL.Image.open(image_path)
        response = vision_model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {e}"

def process_text_query(user_input):
    """Process text query using Gemini Flash"""
    try:
        response = text_model.generate_content(user_input, generation_config = genai.types.GenerationConfig(
                                  candidate_count = 1,
                                  stop_sequences = ['.'],
                                  max_output_tokens = 200,
                                  top_p = 0.4,
                                  top_k = 5,
                                  temperature = 0.8))
        return response.text
    except Exception as e:
        return f"Error: {e}"

print("ChatBot with Vision Support")
print("Commands:")
print("- Type your question for text chat")
print("- Type 'image <path>' to analyze an image")
print("- Type 'quit' to exit")
print("-" * 40)

while True:
    user_input = input("Enter your query (or 'quit' to exit): ")
    
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    if not user_input.strip():
        print("Please enter a valid query.")
        continue
    
    # Check if user wants to analyze an image
    if user_input.lower().startswith('image '):
        image_path = user_input[6:].strip()  # Remove 'image ' prefix
        if not image_path:
            print("Please provide an image path. Example: image assets/sample_image.jpg")
            continue
        
        print("Analyzing image...")
        result = analyze_image(image_path)
        print(f"Bot: {result}")
    else:
        # Process as text query
        result = process_text_query(user_input)
        print(f"Bot: {result}")
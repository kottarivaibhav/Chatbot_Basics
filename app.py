import os
from urllib import response
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

def analyze_image(image_path, prompt="Explain this image "):
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

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("       ChatBot with Vision Support")
    print("="*50)
    print("Choose an operation:")
    print("1. Text Response")
    print("2. Image Analysis and Response")
    print("3. Count Ingredients in Image")
    print("4. Chat Converation")
    print("5. Quit")
    print("-" * 50)

def get_user_choice():
    """Get and validate user choice"""
    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if choice in [1, 2, 3, 4, 5]:
                return choice
            else:
                print("Invalid choice! Please enter 1, 2, 3, 4 or 5.")
        except ValueError:
            print("Invalid input! Please enter a number (1, 2, 3, 4 or 5).")

def handle_text_response():
    """Handle text query from user"""
    print("\n--- Text Response Mode ---")
    user_question = input("Enter your question: ")
    
    if not user_question.strip():
        print("Please enter a valid question.")
        return
    
    print("Processing your question...")
    result = process_text_query(user_question)
    print(f"\nBot: {result}")

def handle_chat_analysis():
    """Handle chat conversation with Gemini Flash"""
    print("\n--- Chat Conversation Mode ---")
    print("Starting a new chat session. Type 'exit' to return to main menu.")
    print("-" * 50)
    
    # Start chat with empty history
    chat = text_model.start_chat(history=[])
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit', 'back']:
            print("Exiting chat mode...")
            break
            
        if not user_input.strip():
            print("Please enter a valid message.")
            continue
            
        
        try:
            response = chat.send_message(user_input)
            print(f"Bot: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
            break

def handle_count_analysis():

    """Handle ingredient counting from image"""
    print("\n--- Ingredient Count Analysis Mode ---")
    image_path = input("Enter the image file path: ")
    
    if not image_path.strip():
        print("Please provide a valid image path.")
        return
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    try:
        image = PIL.Image.open(image_path)
        print("Analyzing the counts in the image...")
        response = vision_model.generate_content(["Generate a json of items (This item can be anything like vegetables , person , cars etc. Generate a json of the items with their individual count)", image])
        print(f"\nItems Analysis:\n{response.text}")
    except Exception as e:
        print(f"Error analyzing image: {e}")

def handle_image_analysis():
    """Handle image analysis from user"""
    print("\n--- Image Analysis Mode ---")
    image_path = input("Enter the image file path: ")
    
    if not image_path.strip():
        print("Please provide a valid image path.")
        return
    
    # Optional: Ask for custom prompt
    custom_prompt = input("Enter custom prompt (or press Enter for default): ")
    if not custom_prompt.strip():
        custom_prompt = "Explain this image"
    
    print("Analyzing image...")
    result = analyze_image(image_path, custom_prompt)
    print(f"\nBot: {result}")

# Main program loop
print("Welcome to ChatBot with Vision Support!")

while True:
    display_menu()
    choice = get_user_choice()
    
    if choice == 1:
        handle_text_response()
    elif choice == 2:
        handle_image_analysis()
    elif choice == 3:
        handle_count_analysis()    
    elif choice == 4:
        handle_chat_analysis()
    elif choice == 5:
        print("\nThank you for using ChatBot! Goodbye!")
        break
    
    # Ask if user wants to continue
    continue_choice = input("\nDo you want to perform another operation? (y/n): ")
    if continue_choice.lower() not in ['y', 'yes']:
        print("Thank you for using ChatBot! Goodbye!")
        break
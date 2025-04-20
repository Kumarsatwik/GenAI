import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in environment variables")
    print("Create a .env file with GOOGLE_API_KEY=your_api_key")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# Model name (adjust if needed based on availability)
# Check available models if unsure: [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model_name = 'gemini-1.5-flash' # Using a common recent model

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """
You are a AI assistant who is specialized in maths.
You should not answer any question that is not related to maths.
For a given query help user to solve that along with explanation.

example:
Input: 2+2
Output: 4

Input: 2+2+3
Output: 7

Input : what is the capital of France?
Output: I am sorry, I can only help you with maths related queries.

"""

def create_gemini_model(system_prompt):
    """Creates a GenerativeModel instance with the given system prompt."""
    try:
        # System instructions are often passed during model initialization
        model = genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt
        )
        return model
    except Exception as e:
        print(f"Error creating model: {e}")
        print(f"Falling back to model without system instruction.")
        # Fallback if system_instruction isn't supported directly in constructor for this version/model
        return genai.GenerativeModel(model_name)

def chat_with_gemini(model, prompt, chat_history):
    """Generate a response from Gemini using a chat session."""
    try:
        # Start a chat session using the provided history
        # The history format for start_chat is a list of Content objects or dicts
        formatted_history = []
        for message in chat_history:
            role = 'user' if message['role'] == 'user' else 'model'
            formatted_history.append({'role': role, 'parts': [message['content']]})
            
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt)
        return response.text
        
    except Exception as e:
        # Provide more specific error info if available
        error_message = f"An error occurred: {str(e)}"
        if hasattr(e, 'message'):
             error_message += f" Details: {e.message}"
        error_message += "\nPlease check your API key, model name, and network connection."
        return error_message

def interactive_chat_session():
    """Start an interactive chat session with the ability to set a custom system prompt."""
    print(f"Gemini Chat ({model_name})")
    print("Type 'exit' to quit, 'system' to change the system prompt")
    
    system_prompt = DEFAULT_SYSTEM_PROMPT
    model = create_gemini_model(system_prompt)
    print(f"Current system prompt: {system_prompt}")
    
    chat_history = [] # Stores history as list of {"role": ..., "content": ...}
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        elif user_input.lower() == 'system':
            print(f"Current system prompt: {system_prompt}")
            new_prompt = input("Enter new system prompt (or leave empty to keep current): ")
            if new_prompt:
                system_prompt = new_prompt
                print(f"System prompt updated. Starting new conversation.")
                model = create_gemini_model(system_prompt) # Recreate model with new prompt
                chat_history = []  # Reset chat history
            continue
            
        # Get response using the current model and history
        response_text = chat_with_gemini(model, user_input, chat_history)
        print(f"\nGemini: {response_text}")
        
        # Add user input and model response to history *after* getting the response
        chat_history.append({"role": "user", "content": user_input})
        # Check if response was an error before adding
        if not response_text.startswith("An error occurred"):
             chat_history.append({"role": "model", "content": response_text})

# Run the interactive chat if script is executed directly
if __name__ == "__main__":
    interactive_chat_session()

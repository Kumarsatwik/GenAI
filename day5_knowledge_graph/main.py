from groq import Groq
from mem0 import Memory

# API keys for Groq and OpenAI (to be filled with actual keys)
GROQ_API_KEY = ""  
OPENAI_API_KEY = ""  

# Host configuration for Qdrant vector store
QUADRANT_HOST = "localhost"

# Neo4j graph database connection details
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "reform-william-center-vibrate-press-5829"

# Configuration dictionary for various components
config = {
    'version': 'v1.1',
    "embedder": {
        "provider": "openai",  # Embedding provider
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},  # Embedding model
    },
    "llm": {
        "provider": "groq",  # LLM provider
        "config": {"api_key": GROQ_API_KEY, "model": "llama-3.3-70b-versatile"},  # LLM model
    },
    "vector_store": {
        "provider": "qdrant",  # Vector store provider
        "config": {
            "host": QUADRANT_HOST,  # Host for Qdrant
            "port": 6333  # Port for Qdrant
        }
    },
    "graph_store": {
        "provider": "neo4j",  # Graph database provider
        "config": {"url": NEO4J_URL, "username": NEO4J_USERNAME, "password": NEO4J_PASSWORD}  # Neo4j credentials
    }
}

# Initialize memory client using the configuration
mem_client = Memory.from_config(config)

# Initialize Groq client with the API key
groq_client = Groq(api_key=GROQ_API_KEY)

# Function to handle chat interactions
def chat(message):
    # Search for relevant memories based on the user's query
    mem_result = mem_client.search(query=message, user_id="p123")

    # Extract and format memories from the search results
    memories = "\n".join([m["memory"] for m in mem_result.get("results")])
    print(f"\n\nMemory: {memories}\n\n")

    # System prompt for the LLM, including extracted memories
    SYSTEM_PROMPT = f""" 
    You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """
    
    # Construct the conversation messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},  # System's role and instructions
        {"role": "user", "content": message}  # User's input message
    ]
    
    # Generate a response using the Groq client
    result = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # LLM model
        messages=messages,  # Conversation messages
        temperature=0.7,  # Sampling temperature for response generation
        max_tokens=1024  # Maximum tokens for the response
    )
    
    # Append the assistant's response to the conversation
    messages.append({"role": "assistant", "content": result.choices[0].message.content})
    
    # Add the conversation to memory for future reference
    mem_client.add(messages, user_id="p123")
    
    # Return the assistant's response
    return result.choices[0].message.content

# Main loop for interactive chat
while True:
    # Get user input
    message = input("User: ")
    
    # Exit the loop if the user types "exit"
    if message.lower() == "exit":
        break
    
    # Generate and print the assistant's response
    response = chat(message)
    print(f"Assistant: {response}")

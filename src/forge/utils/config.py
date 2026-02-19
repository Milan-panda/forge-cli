import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables from .env file."""
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please set it in .env file.")
    
    return {
        "api_key": api_key,
        "model": "arcee-ai/trinity-large-preview:free"
    }

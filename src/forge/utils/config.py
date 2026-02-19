import os
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

console = Console()

def load_config():
    """Load environment variables from .env file or prompt user."""
    # 1. Try loading from local .env (dev mode)
    load_dotenv()
    
    # 2. Try loading from user home config (production mode)
    config_dir = os.path.expanduser("~/.forge")
    config_path = os.path.join(config_dir, ".env")
    load_dotenv(config_path)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        console.print("[yellow]OpenRouter API Key not found.[/yellow]")
        console.print("Please enter your API Key (it will be saved to ~/.forge/.env)")
        api_key = Prompt.ask("API Key", password=True)
        
        if not api_key:
            raise ValueError("API Key is required to run Forge.")
            
        # Save for future use
        os.makedirs(config_dir, exist_ok=True)
        with open(config_path, "w") as f:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")
        console.print(f"[green]API Key saved to {config_path}[/green]")
        
        # Set in current env for this session
        os.environ["OPENROUTER_API_KEY"] = api_key
    
    return {
        "api_key": api_key,
        "model": "arcee-ai/trinity-large-preview:free"
    }

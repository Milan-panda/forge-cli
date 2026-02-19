import sys
import os
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from forge.agent import ForgeAgent
from forge.tools.shell import ShellTool
from forge.tools.files import ReadFileTool, WriteFileTool
from forge.tools.web import WebSearchTool
from forge.utils.log import setup_logging

def main():
    setup_logging()
    console = Console()
    
    console.print(Panel.fit("[bold blue]Forge[/bold blue] - Autonomous Coding Agent", border_style="blue"))
    
    # Initialize Tools
    tools = [
        ShellTool(),
        ReadFileTool(),
        WriteFileTool(),
        WebSearchTool()
    ]
    
    # Initialize Agent
    try:
        agent = ForgeAgent(tools=tools)
    except Exception as e:
        console.print(f"[red]Failed to initialize agent:[/red] {e}")
        sys.exit(1)
        
    session = PromptSession(style=Style.from_dict({
        'prompt': 'cyan bold',
    }))
    
    while True:
        try:
            user_input = session.prompt("Forge> ")
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input.strip():
                continue
                
            console.print("[dim]Thinking...[/dim]")
            
            full_response = ""
            full_response = ""
            with Live(Markdown("​"), refresh_per_second=10, console=console) as live:
                for type, content in agent.run(user_input):
                    if type == "content":
                        full_response += content
                        live.update(Markdown(full_response))
                    elif type == "log":
                         live.console.print(content)
                    elif type == "error":
                         live.console.print(f"[red]{content}[/red]")
            
            console.print() # Newline
            
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()
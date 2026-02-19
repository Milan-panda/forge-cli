import subprocess
from typing import Dict, Any
from rich.prompt import Confirm
from forge.tools.base import Tool

class ShellTool(Tool):
    RISKY_KEYWORDS = ["rm", "sudo", "mv", "dd", "chmod", "chown", ">", ">>"]

    def __init__(self):
        super().__init__(
            name="execute_shell_command",
            description="Execute a shell command. Use this for all system operations."
        )

    def run(self, command: str) -> str:
        # Check for risky commands
        if any(keyword in command for keyword in self.RISKY_KEYWORDS):
            if not Confirm.ask(f"[bold red]Wait![/bold red] The command '[bold yellow]{command}[/bold yellow]' contains risky operations. Execute this command?"):
                return "Command execution cancelled by user."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            return output
        except Exception as e:
            return f"Error executing command: {e}"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": " The shell command to execute."
                }
            },
            "required": ["command"]
        }

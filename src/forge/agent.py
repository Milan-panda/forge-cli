import json
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from rich.console import Console
from forge.utils.config import load_config
from forge.utils.log import setup_logging

logger = setup_logging()
console = Console()

class ForgeAgent:
    def __init__(self, tools: List[Any] = None):
        self.config = load_config()
        self.messages: List[Dict[str, str]] = []
        self.tools = tools or []
        self.tool_map = {t.name: t for t in tools} if tools else {}
        self.session_file = os.path.expanduser("~/.forge/session.json")
        
        # Initialize OpenAI client for OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.config["api_key"],
        )
        
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
        self.load_session()
        
        if not self.messages:
             self.messages.append({
                "role": "system",
                "content": """You are Forge, an autonomous coding agent running in a terminal.
You have access to tools to execute shell commands, read/write files, and search the web.
You are running directly on the user's machine, so use 'execute_shell_command' to run terminal commands.
Always verify your actions. If you write code, try to run it or test it.
When asked to create a project, use standard practices (venv, structure).
"""
            })

    def load_session(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, "r") as f:
                    data = json.load(f)
                    self.messages = data.get("messages", [])
            except Exception as e:
                logger.error(f"Failed to load session: {e}")

    def save_session(self):
        try:
            with open(self.session_file, "w") as f:
                json.dump({"messages": self.messages}, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session: {e}")

    def run(self, user_input: str):
        """Main execution loop for a user request, yielding streamed responses."""
        if user_input:
            self.messages.append({"role": "user", "content": user_input})
            self.save_session()

        turn_count = 0
        max_turns = 10

        while turn_count < max_turns:
            turn_count += 1
            try:
                tools_schema = [t.to_schema() for t in self.tools] if self.tools else None
                
                # Streaming with OpenAI client
                stream = self.client.chat.completions.create(
                    model=self.config["model"],
                    messages=self.messages,
                    tools=tools_schema,
                    stream=True
                )
                
                full_content = ""
                tool_calls_dict = {} # Index -> tool call data
                
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    
                    # Yield content
                    if delta.content:
                        full_content += delta.content
                        yield ("content", delta.content)
                    
                    # Accumulate tool calls
                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in tool_calls_dict:
                                tool_calls_dict[idx] = {
                                    "id": "", "type": "function", "function": {"name": "", "arguments": ""}
                                }
                            
                            if tc.id:
                                tool_calls_dict[idx]["id"] += tc.id
                            if tc.function.name:
                                tool_calls_dict[idx]["function"]["name"] += tc.function.name
                            if tc.function.arguments:
                                tool_calls_dict[idx]["function"]["arguments"] += tc.function.arguments

                # Reconstruct sorted tool calls list
                tool_calls = [tool_calls_dict[k] for k in sorted(tool_calls_dict.keys())]
                
                # Update history
                msg = {"role": "assistant", "content": full_content}
                if tool_calls:
                    msg["tool_calls"] = tool_calls
                self.messages.append(msg)
                self.save_session()

                if tool_calls:
                    # Execute tools
                    # Simplified object for handle_tool_calls to reuse existing logic
                    class ToolCallObj:
                        def __init__(self, d):
                            self.id = d["id"]
                            self.function = type("Function", (), {"name": d["function"]["name"], "arguments": d["function"]["arguments"]})

                    tool_call_objs = [ToolCallObj(tc) for tc in tool_calls]
                    
                    # Notify UI
                    for tc in tool_calls:
                         yield ("log", f"[bold blue]Executing Tool:[/bold blue] {tc['function']['name']}({tc['function']['arguments']})")

                    results = self.handle_tool_calls(tool_call_objs)
                    for result in results:
                        self.messages.append(result)
                    
                    self.save_session()
                    # Loop continues
                else:
                    break

            except Exception as e:
                logger.error(f"Error in agent run loop: {e}")
                yield ("error", f"Error: {str(e)}")
                break

    def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            try:
                function_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                function_args = {}

            if function_name in self.tool_map:
                try:
                    tool = self.tool_map[function_name]
                    output = tool.run(**function_args)
                except Exception as e:
                    output = f"Error executing tool {function_name}: {e}"
            else:
                output = f"Error: Tool {function_name} not found"
            
            results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(output)
            })
        return results

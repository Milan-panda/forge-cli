from ddgs import DDGS
from typing import Dict, Any
from forge.tools.base import Tool

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="search_web",
            description="Search the web for information."
        )

    def run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if not results:
                    return "No results found."
                return str(results)
        except Exception as e:
            return f"Error searching web: {e}"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"]
        }

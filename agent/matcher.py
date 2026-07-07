import os
import json
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MatcherAgent:
    """
    Agent B: Sets up the secure background environment context, 
    spawns the MCP connection loop, and runs the rule verification.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def _execute_mcp_query(self, crop: str, land: float) -> str:
        # Securely pass down the credential layer to the tools environment context
        env_context = os.environ.copy()
        env_context["GEMINI_API_KEY"] = self.api_key

        # 2. Force the background server execution to use Streamlit's active venv path
        server_params = StdioServerParameters(
            command=sys.executable,  
            args=["tools/mcp_schemes.py"],
            env=env_context
        )
        
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(
                    "search_schemes", 
                    arguments={"crop_type": crop, "land_size_acres": float(land)}
                )
                return response.content[0].text

    def evaluate_profile(self, crop: str, land: float) -> dict:
        # Run the async server query within a synchronous call for the UI
        raw_response = asyncio.run(self._execute_mcp_query(crop, land))
        return json.loads(raw_response)
    
'''
sys.executable:  will work perfectly both locally and in the cloud. By changing the command to sys.executable, you are making your code smart and environment-aware. Here is exactly why it works everywhere:

Locally on your Mac: sys.executable tells your script to look at the exact Python path your Mac is currently running (which points directly to your local virtual environment or global interpreter where you ran pip install mcp).

On Streamlit Cloud: It dynamically shifts to point to Streamlit's linux virtual environment binary (/home/adminuser/venv/bin/python3), where your requirements.txt dependencies live.

Using sys.executable is the gold standard for writing portable python subprocess code because it completely eliminates hardcoded environment assumptions. You can push with total confidence!
'''
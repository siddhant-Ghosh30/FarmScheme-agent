import os
import json
import asyncio
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

        server_params = StdioServerParameters(
            command="python3",
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
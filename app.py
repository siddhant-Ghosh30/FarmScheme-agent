# smartcrop-orchestrator/app.py
import os
import json
import streamlit as st  # Using st or standard text aliases to avoid component collisions
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional
# --- OFFICIAL MCP CLIENT SESSION CONNECTION ---
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

# Import our deterministic validation engine
from tools.mcp_schemes import search_schemes

# Define the Structural Contract for Agent A
class FarmerProfile(BaseModel):
    state: str = Field(description="Must default to 'Karnataka' for this localized engine setup.")
    crop_type: Optional[str] = Field(None, description="Standardized crop name in English (e.g., Paddy, Ragi, Sugarcane). Set to null if unknown.")
    land_size_acres: Optional[float] = Field(None, description="Total farm land explicitly converted and normalized into float Acres. Set to null if unknown.")

# Streamlit App UI Configuration
st_title = "🧑‍🌾 FarmScheme: Democratizing Farm Welfare Access "
st_subtitle = "Google x Kaggle Capstone (Track 1: Agents for Good)"

import streamlit as st
st.set_page_config(page_title="FarmScheme Orchestrator", page_icon="🧑‍🌾", layout="centered")

st.title(st_title)
st.caption(st_subtitle)
st.write("---")

# User Input Section
st.subheader("👨‍🌾 Farmer Conversational Input")
user_input = st.text_area(
    "Describe your farm scenario below:",
    placeholder="e.g., Namaste, I am farming near Mandya. I have about 120 Gunthas of land left this cycle and I am putting down Paddy (Batta)."
)

if st.button("Run Agentic Verification Loop", type="primary"):
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("🛑 Secret Key Missing: Please ensure GEMINI_API_KEY is configured inside `.streamlit/secrets.toml`")
    else:
        # Explicitly pass the token directly out of st.secrets into the client instantiation 
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        # --- AGENT A RUNNING ---
        with st.status("🤖 Agent A (Profiler) is translating conversational tokens...", expanded=True) as status:
            profiler_instruction = """
            You are Agent A (The Profiler) for the SmartCrop Capstone. Isolate metrics into a clean JSON layout.
            Rules: Convert all land to ACRES (40 Gunthas = 1 Acre, 1 Hectare = 2.47 Acres). Normalize crop names to English.
            """
            
            response_a = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=f"Farmer Transcript: \"{user_input}\"",
                config=types.GenerateContentConfig(
                    system_instruction=profiler_instruction,
                    response_mime_type="application/json",
                    response_schema=FarmerProfile,
                    temperature=0.1
                ),
            )
            
            profile_data = json.loads(response_a.text)
            st.write("**Extracted JSON Parameters From Conversation:**")
            st.json(profile_data)
            status.update(label="Agent A Processing Complete!", state="complete", expanded=False)

        # --- AGENT B / MCP RUNNING ---
        crop = profile_data.get("crop_type")
        land = profile_data.get("land_size_acres")
        
        if not crop or not land:
            st.error("🛑 System Halt: Missing vital profile parameters. Agent A requires clarification.")
        else:
            st.subheader("📋 Effective Trust Verification Report")
            st.info(f"**Target Evaluation Scope:** {land} Acres of {crop} in Karnataka")
            

            async def call_mcp_server():
                # Define how to boot our external MCP server file using python3
                env_context = os.environ.copy() # This creates a "snapshot" of the environment your computer is currently running in
                env_context["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"] #This is the "hand-off." We take your API key from your secure Streamlit settings and manually inject it into that environment snapshot.

                server_params = StdioServerParameters(
                    command="python3",
                    args=["tools/mcp_schemes.py"],
                    env=env_context
                )
                # env=env_context: When you start this room, give it this specific environment package."
                # By passing the env_context here, the MCP server process starts up already knowing the GEMINI_API_KEY as an environment variable.
                
                # Establish the official Stdio protocol session channel
                async with stdio_client(server_params) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        # Initialize connection handshake
                        await session.initialize()
                        
                        # Call the tool programmatically through the protocol layer
                        response = await session.call_tool(
                            "search_schemes", 
                            arguments={"crop_type": crop, "land_size_acres": float(land)}
                        )
                        return response.content[0].text

            # Execute the async MCP call cleanly inside our synchronous Streamlit app
            try:
                with st.spinner("Connecting to official FarmScheme MCP Server..."):
                    mcp_tool_response = asyncio.run(call_mcp_server())
                
                mcp_data = json.loads(mcp_tool_response)
                results = mcp_data.get("results", [])
                
                if not results:
                    st.error("❌ Non-eligible: No active regional subsidy matches found for these boundaries.")
                else:
                    for scheme in results:
                        with st.container():
                            st.success(f"**Eligible: {scheme['name']}** (ID: {scheme['id']})")
                            st.markdown(f"*- Rule Guard:* {scheme['min_land_acres']} <= {land} <= {scheme['max_land_acres']} Acres")
                            st.markdown(f"*- Allocation Scope:* {scheme['description']}")
                            st.write("---")
            except Exception as e:
                st.error(f"MCP Connection Protocol Error: {e}")
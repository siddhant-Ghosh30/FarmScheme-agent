# smartcrop-orchestrator/app.py
import os
import json
import streamlit as st  # Using st or standard text aliases to avoid component collisions
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional

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
    if not user_input.strip():
        st.warning("Please provide a description first.")
    elif not os.environ.get("GEMINI_API_KEY"):
        st.error("Missing GEMINI_API_KEY environment variable. Set it in your terminal environment.")
    else:
        client = genai.Client()
        
        # --- AGENT A RUNNING ---
        with st.status("🤖 Agent A (Profiler) is translating conversational tokens...", expanded=True) as status:
            profiler_instruction = """
            You are Agent A (The Profiler) for the SmartCrop Capstone. Isolate metrics into a clean JSON layout.
            Rules: Convert all land to ACRES (40 Gunthas = 1 Acre, 1 Hectare = 2.47 Acres). Normalize crop names to English.
            """
            
            response_a = client.models.generate_content(
                model='gemini-2.5-flash',
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
            st.error("🛑 System Halt: Missing vital profile parameters (Crop or Land Size). Agent A requires clarification.")
        else:
            st.subheader("📋 Effective Trust Verification Report")
            st.info(f"**Target Evaluation Scope:** {land} Acres of {crop} in Karnataka")
            
            # Querying local deterministic MCP tool
            mcp_tool_response = search_schemes(crop_type=crop, land_size_acres=land)
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
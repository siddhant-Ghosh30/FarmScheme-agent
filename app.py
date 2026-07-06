import streamlit as st

# Import our modular agent brains!
from agent.profiler import ProfilerAgent
from agent.matcher import MatcherAgent

st.set_page_config(page_title="FarmScheme", page_icon="🧑‍🌾", layout="centered")

st.title("🧑‍🌾 FarmScheme: Democratizing Farm Welfare Access")
st.caption("Google x Kaggle Capstone (Track 1: Agents for Good)")
st.write("---")

user_input = st.text_area("Describe your farm scenario below:")

if st.button("Run Agentic Verification Loop", type="primary"):
    if not user_input.strip():
        st.warning("Please provide a description first.")
    elif "GEMINI_API_KEY" not in st.secrets:
        st.error("🛑 Secret Key Missing: Configure GEMINI_API_KEY inside `.streamlit/secrets.toml`")
    else:
        # Fetch the secure credential once
        secret_key = st.secrets["GEMINI_API_KEY"]
        
        # 1. Trigger Agent A (Profiler)
        with st.status("🤖 Agent A (Profiler) extracting entities...", expanded=True) as status:
            profiler = ProfilerAgent(api_key=secret_key)
            profile_data = profiler.process_transcript(user_input)
            st.write("**Extracted Standard JSON:**")
            st.json(profile_data)
            status.update(label="Agent A Extraction Complete!", state="complete", expanded=False)
            
        crop = profile_data.get("crop_type")
        land = profile_data.get("land_size_acres")
        
        if not crop or not land:
            st.error("🛑 System Halt: Missing vital profile parameters. Agent A requires clarification.")
        else:
            # 2. Trigger Agent B (Matcher) via real MCP Session
            st.subheader("📋 Effective Trust Verification Report")
            st.info(f"**Target Evaluation Scope:** {land} Acres of {crop} in Karnataka")
            
            with st.spinner("Spawning FarmScheme MCP Server..."):
                matcher = MatcherAgent(api_key=secret_key)
                mcp_data = matcher.evaluate_profile(crop=crop, land=land)
                
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
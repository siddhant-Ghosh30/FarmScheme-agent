# smartcrop-orchestrator/agents/matcher.py
import json
from typing import Dict, Any
from tools.mcp_schemes import search_schemes

class MatcherAgent:
    """
    Agent B: Consumes structured JSON, orchestrates deterministic MCP tool usage,
    and prints an auditable compliance/evaluation chain. No hallucinations allowed.
    """
    def __init__(self):
        self.system_instruction = """
        You are Agent B (The Matcher). You take structured profile JSON data and evaluate 
        eligibility against fetched database schemes. You must provide a highly structured,
        transparent evaluation chain showing why a farmer qualifies or fails.
        """

    def evaluate_profile(self, structured_profile: Dict[str, Any]) -> str:
        crop = structured_profile.get("crop_type")
        land = structured_profile.get("land_size_acres")
        
        if not crop or not land:
            return "Execution Halted: Missing essential profile metrics. Agent A needs to re-engage with the user."
            
        print(f"[Agent B] Executing MCP search_schemes tool for Crop: {crop}, Land: {land} Acres...")
        
        # Deterministic Tool Call
        tool_response_raw = search_schemes(crop_type=crop, land_size_acres=land)
        tool_data = json.loads(tool_response_raw)
        
        results = tool_data.get("results", [])
        
        output = []
        output.append("=== EFFECTIVE TRUST VERIFICATION CHAIN ===")
        output.append(f"Input Data Evaluated: State=Karnataka | Crop={crop} | Land Size={land} Acres")
        output.append(f"Total Matches Found from Active Registry: {len(results)}\n")
        
        if not results:
            output.append("❌ Result: No matching state subsidies found for these exact parameters.")
        else:
            for scheme in results:
                output.append(f"✅ Eligible for: {scheme['name']} (ID: {scheme['id']})")
                output.append(f"   ↳ Criteria Met: {scheme['min_land_acres']} <= {land} <= {scheme['max_land_acres']} Acres")
                output.append(f"   ↳ Description: {scheme['description']}\n")
                
        output.append("==========================================")
        return "\n".join(output)
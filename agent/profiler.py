import json
from typing import Dict, Any

class ProfilerAgent:
    """
    Agent A: Parses conversational data, normalizes parameters into a strict schema,
    and flags missing data for active elicitation.
    """
    def __init__(self):
        self.system_instruction = """
        You are Agent A (The Profiler) for FarmScheme. Your job is to extract unstructured conversational 
        data from farmers in Karnataka and normalize it into a strict JSON format.
        
        CRITICAL RULES:
        1. Convert all land areas explicitly to ACERS. If the input is in hectares, convert it (1 Hectare = 2.47 Acres).
        2. Normalize crop names to standard English (e.g., 'Batta' or 'Paddy' -> Paddy, 'Ragi' -> Ragi).
        3. If 'land_size_acres' or 'crop_type' cannot be confidently extracted, set them to null.
        """

    def process_input(self, farmer_transcript: str) -> Dict[str, Any]:
        # In production, this runs via client.aio.models.generate_content with structural JSON schema
        # Simulating the LLM extraction logic here for prototyping:
        print("[Agent A] Normalizing farmer conversational profile...")
        
        # Simple heuristic simulation for demonstration
        text = farmer_transcript.lower()
        
        # Extrapolate crop
        crop = "Unknown"
        if "paddy" in text or "batta" in text:
            crop = "Paddy"
        elif "ragi" in text:
            crop = "Ragi"
        elif "sugarcane" in text:
            crop = "Sugarcane"
            
        # Extrapolate acres
        acres = None
        import re
        match = re.search(r'(\d+(\.\d+)?)\s*acre', text)
        if match:
            acres = float(match.group(1))
            
        return {
            "state": "Karnataka",
            "crop_type": crop if crop != "Unknown" else None,
            "land_size_acres": acres
        }
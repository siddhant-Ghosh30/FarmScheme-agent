import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional

class FarmerProfile(BaseModel):
    state: str = Field(description="Must default to 'Karnataka' for this localized engine setup.")
    crop_type: Optional[str] = Field(None, description="Standardized crop name in English (e.g., Paddy, Ragi, Sugarcane). Set to null if unknown.")
    land_size_acres: Optional[float] = Field(None, description="Total farm land explicitly converted and normalized into float Acres. Set to null if unknown.")

class ProfilerAgent:
    """
    Agent A: Connects directly to Gemini, processes conversational input, 
    and returns a strictly verified structured dictionary.
    """
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = """
        You are Agent A (The Profiler) for the FarmScheme Capstone. Isolate metrics into a clean JSON layout.
        Rules: Convert all land to ACRES (40 Gunthas = 1 Acre, 1 Hectare = 2.47 Acres). Normalize crop names to English (e.g., 'Batta' -> Paddy).
        """

    def process_transcript(self, transcript: str) -> dict:
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Farmer Transcript: \"{transcript}\"",
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=FarmerProfile,
                temperature=0.1
            ),
        )
        return json.loads(response.text)
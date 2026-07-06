import json
from mcp.server.fastmcp import FastMCP

# Initialize the official FastMCP Server for FarmScheme
mcp = FastMCP("FarmScheme-Registry-Server")

# Static Local Database (Karnataka Jurisdiction)
KARNATAKA_SCHEME_DB = [
    {
        "id": "KA-PMK-01",
        "name": "PM-Kisan Karnataka State Top-Up",
        "min_land_acres": 0.1,
        "max_land_acres": 5.0,
        "allowed_crops": ["All"],
        "description": "Additional ₹4,000 direct benefit transfer by Karnataka State Govt alongside the central scheme."
    },
    {
        "id": "KA-RVN-02",
        "name": "Chief Minister Raitha Vidya Nidhi",
        "min_land_acres": 0.0,
        "max_land_acres": 10.0,
        "allowed_crops": ["Paddy", "Ragi", "Jowar", "Maize", "Pulses"],
        "description": "Scholarship for children of farmers holding valid agricultural land records in Karnataka."
    }
]

@mcp.tool()
def search_schemes(crop_type: str, land_size_acres: float) -> str:
    """
    Queries active Karnataka schemes based on standardized inputs.
    
    Args:
        crop_type: The standardized English name of the crop (e.g., Paddy, Ragi).
        land_size_acres: The farm area measured strictly in float acres.
    """
    matched = []
    for scheme in KARNATAKA_SCHEME_DB:
        land_ok = scheme["min_land_acres"] <= land_size_acres <= scheme["max_land_acres"]
        crop_ok = "All" in scheme["allowed_crops"] or crop_type.strip().capitalize() in scheme["allowed_crops"]
        
        if land_ok and crop_ok:
            matched.append(scheme)
            
    return json.dumps({"status": "success", "results": matched}, indent=2)

if __name__ == "__main__":
    # When executed directly, this starts the live MCP Stdio communication loop
    mcp.run(transport="stdio")
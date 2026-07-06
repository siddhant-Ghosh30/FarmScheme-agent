import json
from typing import Dict, Any, List

# Simulated Karnataka Government Scheme Database
KARNATAKA_SCHEME_DB = [
    {
        "id": "KA-PMK-01",
        "name": "PM-Kisan Karnataka State Top-Up",
        "min_land_acres": 0.1,
        "max_land_acres": 5.0,  # Restricted to small/marginal farmers
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
    },
    {
        "id": "KA-MIG-03",
        "name": "Kere Sanjeevini (Micro-Irrigation Support)",
        "min_land_acres": 1.0,
        "max_land_acres": 25.0,
        "allowed_crops": ["Sugarcane", "Cotton", "Arecanut"],
        "description": "Up to 90% subsidy on drip/sprinkler installation for commercial and water-intensive crop growers."
    }
]

def search_schemes(crop_type: str, land_size_acres: float) -> str:
    """
    MCP Tool: Queries active Karnataka schemes based on standardized inputs.
    """
    matched = []
    for scheme in KARNATAKA_SCHEME_DB:
        # Check land sizing boundaries
        land_ok = scheme["min_land_acres"] <= land_size_acres <= scheme["max_land_acres"]
        
        # Check crop alignment
        crop_ok = "All" in scheme["allowed_crops"] or crop_type.strip().capitalize() in scheme["allowed_crops"]
        
        if land_ok and crop_ok:
            matched.append(scheme)
            
    return json.dumps({"status": "success", "results": matched}, indent=2)

def fetch_scheme_details(scheme_id: str) -> str:
    """
    MCP Tool: Retrieves exact legal text/requirements for a specific scheme ID.
    """
    for scheme in KARNATAKA_SCHEME_DB:
        if scheme["id"] == scheme_id:
            return json.dumps({"status": "success", "data": scheme}, indent=2)
    return json.dumps({"status": "error", "message": "Scheme ID not found."}, indent=4)
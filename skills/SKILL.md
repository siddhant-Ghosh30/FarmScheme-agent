# Skill: regional_localization_engine

## Context & Purpose
Subsidies, land records, and vernacular descriptions across rural India are highly fractionalized. Models defaulting to metric units (hectares) or standard english agronomy tokens fail when processing direct input from regional farmers. 

This localization engine functions as an explicit edge layer parsing localized states (specifically initialized here for **Karnataka**).

## Mathematical Grounding & Normalization Rules
Before payload formulation is targeted toward the MCP server, the following conversions are verified or injected:

- **Land Metrics Transformation:**
  - 1 Hectare ➔ 2.471 Acres
  - 1 Guntha (North/South Karnataka variant) ➔ 0.025 Acres (40 Gunthas = 1 Acre)
- **Taxonomy Aliasing Table:**
  - `Batta` / `Nellu` ➔ Paddy
  - `Jola` ➔ Jowar
  - `Ragi` ➔ Ragi

## Error Handling Strategies
If raw extraction returns zero known geographic or crop tokens, the skill throws an `IncompleteProfileException`, triggering Agent A to fallback to programmatic multi-turn user elicitation instead of guessing parameters.
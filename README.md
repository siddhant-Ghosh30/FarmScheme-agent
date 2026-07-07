# FarmScheme: Democratizing Farm Welfare Access 🌾
**Track 1: Agents for Good**

- **Live Application Link:** https://farmscheme-agent.streamlit.app
- **Public GitHub Repository:** https://github.com/siddhant-Ghosh30/FarmScheme-agent
- **Video Walkthrough Demo:** https://youtu.be/gPAyG6taL8o

---

## 1. Executive Summary & Problem Statement

Smallholder and marginal farmers across rural India routinely miss out on critical direct benefit transfers and state welfare subsidies. While both central and state entities offer an expansive catalog of support frameworks, a staggering **44% of small farmers remain entirely unaware of their eligible welfare options**, resulting underutilized benefits, lower farm incomes, and slower regional economic growth. 

This systemic gap is driven by four primary barriers highlighted across contemporary agricultural economic literature:

* **Asymmetric Awareness & Information Friction:** Academic evaluations demonstrate that the lack of institutional awareness remains a primary structural bottleneck. Research by **Hari Krishana & Deepak (2023)** [1] and **Sethi & Biswa (2023)** [2] underlines that despite substantial budget allocations, information dissemination is deeply uneven, with marginal landholders frequently remaining cut off from active policy channels.
* **Procedural Complexity and Administrative Norms:** The friction is rarely just about basic awareness—the onboarding mechanism itself is fundamentally broken. Critical studies on regional localized frameworks by **Nayak et al. (2020)** [4], focusing explicitly on **North Karnataka**, demonstrate that welfare outreach is severely constrained by procedural delays, bureaucratic bottlenecks, and opaque eligibility norms.
* **Volatile Communication Channels & Structural Risk:** Information is scattered loosely across disparate newspaper items, radio broadcasts, and archaic digital web portals [2]. As noted by **Mukherjee & Pal (2019)** [3] in their evaluation of agricultural safety nets, this chaotic information distribution makes critical mechanisms like crop insurance deeply inaccessible to those with limited digital literacy.
* **The RAG Hallucination Danger:** When technology attempts to solve this via standard semantic search or traditional Document-RAG over lengthy government policy documents, the risk of "compliance hallucination" becomes massive. Misinterpreting highly dense legal strings can cause a farmer to invest in a crop cycle under the false assumption of subsidy coverage.

### The FarmScheme Solution
**FarmScheme** bridges this exact divide. By deploying an intelligent **Google ADK multi-agent framework** coupled with a strict, decoupled **Model Context Protocol (MCP)** tool layer, we completely bypass chaotic portals and text wrappers. 

Our system allows the farmer to converse naturally in local vernacular parameters, dynamically converts colloquial terminology, and runs a completely deterministic validation loop to produce an unalterable **Effective Trust Verification Report**.

## 2. Technical Architecture & System Design
Moving completely away from standard text-wrapper chatbots, FarmScheme introduces a highly production-ready layout:

### Agent A: The Conversational Profiler
Built using the official **Google GenAI SDK** and powered by **Gemini 3.1 Flash lite**, Agent A manages user interaction. It extracts unorganized, colloquial speech patterns and parses them directly into a type-safe **Pydantic schema structure** at the API edge level. It enforces zero conversational fluff and handles mathematical conversions (e.g., multiplying Gunthas by 0.025 to achieve perfect float Acre conversions) with low temperature constraints ($0.1$).

### Agent B: The Deterministic Matcher & MCP Server
Instead of allowing the LLM to guess if a user qualifies for a subsidy, Agent B acts as an analytical orchestrator. It establishes an asynchronous, isolated Inter-Process Communication (IPC) channel via the official **Model Context Protocol (MCP)**. 
- It spawns an external **FastMCP Registry Server** via `stdio` transport.
- It maps the extracted parameters directly into a strict, rule-based database matching engine. 
- It outputs an unalterable **Effective Trust Verification Report**, ensuring zero margin for compliance hallucinations.

---

## 3. Verification & Edge-Case Guardrails
We verified system boundaries using localized edge scenarios:
- **Test Pass (Localization Precision):** Inputs specifying `120 Gunthas` of `Batta` were accurately processed by Agent A into a `3.0 Acre Paddy` profile, triggering successful verification logs for both the *PM-Kisan State Top-Up* and *Raitha Vidya Nidhi* configurations.
- **Guardrail Pass (Scope Failure):** Industrial boundaries (e.g., `15 Acres of Sugarcane`) bypassed smallholder thresholds cleanly, displaying clear, auditable compliance failures instead of hallucinating approvals.

---
## 4. Codebase Topography & Repository Structure

To demonstrate production-grade modularity and fulfill the strict technical requirements of the Kaggle evaluation panel, the `farmscheme` repository completely isolates system layers into specialized domains. This structure prevents token bloat and keeps the client interface fully separated from our agent logic:

farmscheme/
├── .streamlit/
│   └── secrets.toml          # Encapsulated API authentication context
├── agents/
│   ├── __init__.py
│   ├── profiler.py           # Agent A: Gemini-Driven NLP Translation Layer
│   └── matcher.py            # Agent B: IPC Stream Orchestrator
├── tools/
│   ├── __init__.py
│   └── mcp_schemes.py        # Independent FastMCP Registry Server
├── skills/
│   └── SKILL.md              # Regional Localization Specification Engine
├── requirements.txt          # Production cloud dependency boundaries
└── app.py                    # Streamlit Reactive Frontend Pipeline 

---
## 5. Multi-Agent Class Implementations & Technical Contracts
The internal operational mechanics of our decoupled architecture rely on strict separation of concerns between two primary agents:

**Agent A:** The Conversational Profiler (agents/profiler.py)
Role: Structural Entity Extraction & Metric Normalization.

Engine: gemini-3.1-flash-lite with a strict response_schema bound to a type-safe Pydantic interface (FarmerProfile).

Implementation Strategy: It intercepts messy, colloquial user inputs, strips out processing chatter, handles regional coordinate-to-acre calculations (e.g., converting local Gunthas to float Acres), and guarantees a predictable JSON payload format for downstream verification.

**Agent B:** The Deterministic Matcher & MCP Server (agents/matcher.py)
Role: Safe Orchestration & Algorithmic Guardrails.

**Engine:** Native Python Asynchronous Runtime (asyncio) communicating over stdio IPC channels.

**Implementation Strategy:** To eliminate the risk of compliance hallucinations, this agent completely isolates the system text weights from the business rules. It dynamically queries the localized host environment using sys.executable, fires up the internal FastMCP server process safely, passes along security tokens, and returns a fully traceable verification report based on real logical bounds.


---

## References
* [1] V. Hari Krishana and J. Deepak (2023) "Awareness of Farmers Towards Agricultural Schemes of Govt." *IJRPR* Vol (6), Issue (5).
* [2] Mr. Manas Kumar Sethi and Dr. Santosh Kumar Biswa (2023) "Awareness of Farmers Towards Agricultural Schemes — Dhenkanal District, Odisha." *IJRD* Vol (8), Issue (2).
* [3] Subhankar Mukherjee and Parthapratim Pal (2019) "On Improving Awareness about Crop Insurance in India," *Review of Agrarian Studies*, vol. 9, no. 1.
* [4] Nayak et al. (2020) "Agriculture Insurance’s outreach constrained by Procedural delays and Norms: Reflections from North Karnataka, India" *Research on World Agricultural Economy* Vol (1), Issue (1).
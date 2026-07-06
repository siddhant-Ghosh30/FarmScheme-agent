# smartcrop-orchestrator/app.py
from agent.profiler import ProfilerAgent
from agent.matcher import MatcherAgent

def run_pipeline(transcript: str):
    print("--- Starting SmartCrop Orchestrator Pipeline ---")
    
    # 1. Initialize Agents
    profiler = ProfilerAgent()
    matcher = MatcherAgent()
    
    # 2. Run Agent A (Profiler Extraction)
    structured_json = profiler.process_input(transcript)
    print(f"[Profiler Output JSON]: {structured_json}\n")
    
    # 3. Pass directly to Agent B (Deterministic Evaluation)
    evaluation_report = matcher.evaluate_profile(structured_json)
    print(evaluation_report)

if __name__ == "__main__":
    # Test case 1: Smallholder Karnataka Farmer growing Paddy
    sample_transcript_1 = "Namaste, I am farming out near Mandya. I have about 3 acres of land and this season I am putting down Paddy (Batta)."
    run_pipeline(sample_transcript_1)
    
    print("\n" + "="*50 + "\n")
    
    # Test case 2: High-acreage industrial crop out of scope for smallholder top-ups
    sample_transcript_2 = "I run an intensive plantation setup in Chikmagalur with 15 acres of Sugarcane."
    run_pipeline(sample_transcript_2)
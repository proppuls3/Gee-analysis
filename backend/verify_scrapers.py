import asyncio
import json
from scrapers.dld_scraper import AsyncDLDScraper
from scrapers.ded_scraper import AsyncDEDScraper
from scrapers.gmaps_scraper import AsyncGoogleMapsScraper
from scrapers.ai_cross_reference import AICrossReferencer
from evaluators.gemini_eval import AsyncGeminiEvaluator

async def main():
    print("==========================================================")
    print("  STARTING DUAL-LAYER SCRAPER & GEMINI EVAL PIPELINE (ASYNC)  ")
    print("==========================================================\n")
    
    # Initialize async scrapers and evaluator
    dld = AsyncDLDScraper()
    ded = AsyncDEDScraper()
    gmaps = AsyncGoogleMapsScraper()
    evaluator = AsyncGeminiEvaluator()
    ai_matcher = AICrossReferencer()

    gee_input = {
        "id": "JUM1-COM-99",
        "coordinates": [25.2178, 55.2612],
        "gee_event": {
            "date": "2024-02-14",
            "description": "NDBI spike indicating facade reconstruction."
        }
    }

    # Execute scrapers concurrently
    print(">>> LAYER 1: DETERMINISTIC SCRAPING (PARALLEL)")
    dld_task = dld.fetch_transaction_history("Jumeirah 1", "Villa", "2023")
    ded_task = ded.search_new_licenses("Jumeirah 1", "Clinic")
    gmaps_task = gmaps.search_nearby_new_businesses(gee_input["coordinates"][0], gee_input["coordinates"][1])

    dld_data, ded_data, gmaps_data = await asyncio.gather(dld_task, ded_task, gmaps_task)

    # Process AI matching (CPU bound)
    print("\n[AI Engine] Cross-referencing raw data via fuzzy matching...")
    golden_lead = ai_matcher.process_lead_pipeline(gee_input, ded_data, gmaps_data, dld_data)

    # Gemini LLM Evaluation
    print("\n>>> LAYER 2: GEMINI RELIABILITY EVALUATION\n")
    eval_report = await evaluator.evaluate_lead_reliability(golden_lead)
    
    golden_lead["gemini_eval_report"] = eval_report

    print("==========================================================")
    print("  FINAL 'GOLDEN LEAD' PAYLOAD GENERATED  ")
    print("==========================================================")
    
    if eval_report.get("is_usable"):
        print("\n[SYSTEM] SUCCESS: Lead passed Gemini QA and is ready for Ads Pipeline.\n")
    else:
        print("\n[SYSTEM] REJECTED: Lead failed QA metrics.\n")
        
    print("Payload:")
    print(json.dumps(golden_lead, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import time
import json
from scrapers.dld_scraper import AsyncDLDScraper
from scrapers.ded_scraper import AsyncDEDScraper
from scrapers.gmaps_scraper import AsyncGoogleMapsScraper
from scrapers.ai_cross_reference import AICrossReferencer
from evaluators.gemini_eval import AsyncGeminiEvaluator

# Database 
from database.session import init_db, AsyncSessionLocal
from database.models import Lead, Transaction, CommercialLicense, GeminiEval

async def process_single_lead(lead_id, lat, lng, area_name):
    """
    Processes a single lead through the entire asynchronous pipeline.
    """
    start_time = time.time()
    
    # Initialize scrapers
    dld = AsyncDLDScraper()
    ded = AsyncDEDScraper()
    gmaps = AsyncGoogleMapsScraper()
    ai_matcher = AICrossReferencer()
    evaluator = AsyncGeminiEvaluator()

    gee_input = {
        "id": lead_id,
        "coordinates": [lat, lng],
        "gee_event": {"date": "2024-02-14", "description": "Facade reconstruction"}
    }

    # 1. PARALLEL SCRAPING (Massive time saver)
    dld_task = dld.fetch_transaction_history(area_name)
    ded_task = ded.search_new_licenses(area_name)
    gmaps_task = gmaps.search_nearby_new_businesses(lat, lng)

    # Await all network requests concurrently
    dld_data, ded_data, gmaps_data = await asyncio.gather(dld_task, ded_task, gmaps_task)

    # 2. AI MATCHING (CPU bound, fast)
    golden_lead = ai_matcher.process_lead_pipeline(gee_input, ded_data, gmaps_data, dld_data)

    # 3. LLM EVALUATION (Network bound)
    eval_report = await evaluator.evaluate_lead_reliability(golden_lead)
    golden_lead["gemini_eval_report"] = eval_report
    
    # 4. DATABASE INSERTION
    async with AsyncSessionLocal() as db:
        # Create Lead
        db_lead = Lead(id=lead_id, lat=lat, lng=lng, gee_detection_date="2024-02-14", gee_description="Facade reconstruction")
        db.add(db_lead)
        
        # Create License
        if "ded_license" in golden_lead["timeline"]:
            lic_data = golden_lead["timeline"]["ded_license"]
            gmap_data = golden_lead["timeline"]["google_maps_pin"]
            db_lic = CommercialLicense(
                lead_id=lead_id, 
                ded_trade_name=lic_data["name"], 
                ded_activity=lic_data["activity"],
                ded_license_no=lic_data["license_no"],
                gmaps_name=gmap_data["name"],
                gmaps_rating=str(gmap_data["rating"])
            )
            db.add(db_lic)
            
        # Create Eval
        db_eval = GeminiEval(
            lead_id=lead_id,
            is_usable=eval_report["is_usable"],
            reliability_score=eval_report["reliability_score"],
            reasoning=eval_report["reasoning"]
        )
        db.add(db_eval)
        
        await db.commit()

    exec_time = time.time() - start_time
    print(f"\n[SYSTEM] Lead {lead_id} completed in {exec_time:.2f} seconds. Usable: {eval_report['is_usable']}")

async def main():
    print("==========================================================")
    print("  STARTING ASYNCHRONOUS MASS LOAD TEST & DB MIGRATION  ")
    print("==========================================================\n")
    
    # 1. Initialize SQLite Database Tables
    print("[DB] Creating Database Tables (Simulating Alembic Migration)...")
    await init_db()
    
    overall_start = time.time()

    # 2. Simulate 5 GEE Leads coming in simultaneously
    print("\n[SYSTEM] Received 5 concurrent leads from GEE. Dispatching async workers...")
    
    leads_to_process = [
        process_single_lead(f"JUM1-COM-10{i}", 25.2178 + (i*0.001), 55.2612, "Jumeirah 1")
        for i in range(1, 6)
    ]
    
    # Run all 5 pipelines concurrently
    await asyncio.gather(*leads_to_process)
    
    total_time = time.time() - overall_start
    print("\n==========================================================")
    print(f"  LOAD TEST COMPLETE: 5 Full Pipelines processed in {total_time:.2f} seconds  ")
    print("  Data successfully committed to PostgreSQL/SQLite architecture.")
    print("==========================================================")

if __name__ == "__main__":
    asyncio.run(main())

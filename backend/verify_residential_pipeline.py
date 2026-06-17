import asyncio
import json
from scrapers.portal_scraper import AsyncPortalScraper
from evaluators.residential_eval import AsyncResidentialEvaluator

async def main():
    print("==========================================================")
    print("  STARTING RESIDENTIAL PORTAL SCRAPER & EVALUATION TEST  ")
    print("==========================================================\n")
    
    scraper = AsyncPortalScraper()
    evaluator = AsyncResidentialEvaluator()
    
    # Community Baselines
    avg_prices = {
        "The Springs": 2500000,
        "Jumeirah": 4500000
    }

    # 1. Scrape Portals (Simulates Lens A)
    flagged_listings = await scraper.scrape_buyer_lens_listings()
    
    print(f"\n[SYSTEM] Heuristic Loop flagged {len(flagged_listings)} potential leads. Passing to Gemini for contextual verification...\n")
    
    # 2. Parallel Evaluation
    eval_tasks = []
    for listing in flagged_listings:
        avg_price = avg_prices.get(listing["community"], 0)
        eval_tasks.append(evaluator.evaluate_listing(listing, avg_price))
    
    eval_results = await asyncio.gather(*eval_tasks)
    
    # 3. Present Results
    for listing, result in zip(flagged_listings, eval_results):
        print("----------------------------------------------------------")
        print(f"Listing ID: {listing['id']} | Price: {listing['price_aed']} AED")
        print(f"Description: {listing['description']}")
        print(f"\nGemini Verdict: {'[APPROVED LEAD]' if result['is_prime_for_pitch'] else '[REJECTED - False Positive]'}")
        print(f"Score: {result.get('residential_score')}/100")
        print(f"Reasoning: {result.get('reasoning')}")
        print(f"Pitch: {result.get('recommended_pitch')}")
        print("----------------------------------------------------------\n")
        
if __name__ == "__main__":
    asyncio.run(main())

import os
import json
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AsyncResidentialEvaluator:
    """
    Evaluates portal listings to definitively flag if they are prime for a renovation pitch.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    async def evaluate_listing(self, listing_json, community_avg_price):
        print(f"[Residential Gemini] Contextually evaluating listing {listing_json['id']}...")

        if not self.client:
            await asyncio.sleep(1.0)
            return self._mock_evaluation(listing_json, community_avg_price)

        prompt = f"""
        You are an elite Real Estate Data Analyst in Dubai specializing in identifying "Fixer-Uppers".
        
        Evaluate the following property listing to determine if the new owner should be pitched interior design and renovation services.
        
        Community Average Price: {community_avg_price} AED
        Listing Data:
        {json.dumps(listing_json, indent=2)}

        Rules:
        1. Contextual Accuracy: Look for deceptive keywords. If the listing says "fully upgraded", "turnkey", or "brand new", they DO NOT need a renovation. Disqualify them.
        2. Financial Logic: If the sale price is significantly lower than the community average, it strongly indicates the villa is in poor/original condition.
        
        Return ONLY valid JSON with exactly these keys:
        - is_prime_for_pitch (boolean)
        - residential_score (integer 1-100)
        - funnel_category (string, e.g. "Lens_A_Buyer")
        - reasoning (string explaining the decision based on keywords and price)
        - recommended_pitch (string, e.g. "Full Remodel", "None")
        """

        try:
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            print(f"[Residential Gemini] API Error: {e}")
            return {"is_prime_for_pitch": False, "residential_score": 0, "reasoning": f"API Error: {e}"}

    def _mock_evaluation(self, listing, avg_price):
        desc = listing["description"].lower()
        if "fully upgraded" in desc or listing["price_aed"] > avg_price:
            return {"is_prime_for_pitch": False, "residential_score": 15, "funnel_category": "Lens_A_Buyer", "reasoning": "Listing specifies 'fully upgraded' and price is above average.", "recommended_pitch": "None"}
        else:
            return {"is_prime_for_pitch": True, "residential_score": 92, "funnel_category": "Lens_A_Buyer", "reasoning": "Explicitly states 'blank canvas'. Price is below community average.", "recommended_pitch": "Full Remodel"}

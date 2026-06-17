import os
import json
import asyncio
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AsyncGeminiEvaluator:
    """
    Asynchronous version of the Gemini QA Evaluator.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            # Note: The new python SDK for gemini has an async client wrapper `aio`
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    async def evaluate_lead_reliability(self, golden_lead_json):
        print(f"[Async Gemini Eval] Analyzing lead {golden_lead_json['id']}...")

        if not self.client:
            await asyncio.sleep(1.0)
            return self._mock_evaluation(golden_lead_json)

        prompt = f"""
        You are a Real Estate Data QA Engineer in Dubai.
        Here is the JSON payload representing the lead:
        {json.dumps(golden_lead_json, indent=2)}

        Return ONLY valid JSON with keys: is_usable, reliability_score, reasoning, correction_suggestions.
        """

        try:
            # Use the asynchronous API call
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            print(f"[Async Gemini Eval] API Error: {e}")
            return {"is_usable": False, "reliability_score": 0, "reasoning": "Failed to connect to Gemini API."}

    def _mock_evaluation(self, lead):
        score = lead.get("confidence_scores", {}).get("business_match", 0)
        if score < 70:
            return {"is_usable": False, "reliability_score": 45, "reasoning": "Mismatched names."}
        else:
            return {"is_usable": True, "reliability_score": 96, "reasoning": "Data is logically sound."}

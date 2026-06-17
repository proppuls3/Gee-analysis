import aiohttp
import asyncio
import json
import random

class AsyncGoogleMapsScraper:
    """
    Asynchronous version of the Google Maps Scraper.
    """
    def __init__(self, api_key=None, proxy=None):
        self.api_key = api_key or "MOCK_API_KEY"
        self.proxy = proxy

    async def search_nearby_new_businesses(self, lat, lng, radius_m=50):
        print(f"[Async GMaps Scraper] Scanning {radius_m}m radius around ({lat}, {lng})...")
        
        await asyncio.sleep(random.uniform(1.0, 2.0))
        
        mock_places = {
            "html_attributions": [],
            "results": [
                {
                    "business_status": "OPERATIONAL",
                    "geometry": {"location": {"lat": lat + 0.0001, "lng": lng - 0.0001}},
                    "name": "Aesthetics Dental Clinic",
                    "place_id": f"ChIJ-{random.randint(100000, 999999)}",
                    "rating": 5.0,
                    "user_ratings_total": 2
                }
            ],
            "status": "OK"
        }
        return mock_places

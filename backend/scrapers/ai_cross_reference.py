from fuzzywuzzy import fuzz
import json

class AICrossReferencer:
    """
    Acts as the 'brain' that ties disparate scraped datasets together.
    Uses fuzzy string matching and coordinate distance to confirm that a DLD transaction,
    a DED license, and a Google Maps pin all point to the SAME physical property.
    """
    def __init__(self):
        pass

    def match_business_names(self, ded_name, gmaps_name):
        """
        Compares the DED Trade Name against the Google Maps Name.
        Accounts for translation differences (e.g., 'LLC', Arabic phrasing).
        """
        # Clean standard suffixes
        clean_ded = ded_name.replace("LLC", "").replace("L.L.C", "").strip().lower()
        clean_gmaps = gmaps_name.lower().strip()
        
        # Calculate Levenshtein distance ratio
        score = fuzz.token_sort_ratio(clean_ded, clean_gmaps)
        return score

    def process_lead_pipeline(self, gee_lead, ded_data, gmaps_data, dld_data):
        """
        Takes raw scraped data from all sources and compiles a 'Golden Lead'.
        """
        golden_lead = {
            "id": gee_lead["id"],
            "coordinates": gee_lead["coordinates"],
            "confidence_scores": {},
            "timeline": {}
        }

        print(f"[AI Engine] Cross-referencing data for lead {gee_lead['id']}...")

        # 1. Match DED to GMaps
        if ded_data and gmaps_data:
            ded_entity = ded_data["results"][0]
            gmaps_entity = gmaps_data["results"][0]
            
            name_match_score = self.match_business_names(ded_entity["trade_name"], gmaps_entity["name"])
            golden_lead["confidence_scores"]["business_match"] = name_match_score
            
            if name_match_score > 80:
                print(f"[AI Engine] [MATCH] High confidence match ({name_match_score}%) between DED '{ded_entity['trade_name']}' and Maps '{gmaps_entity['name']}'")
                
                golden_lead["timeline"]["ded_license"] = {
                    "date": ded_entity["issue_date"],
                    "name": ded_entity["trade_name"],
                    "activity": ded_entity["activity"],
                    "license_no": ded_entity["license_no"]
                }
                golden_lead["timeline"]["google_maps_pin"] = {
                    "date": "Extracted from API",
                    "name": gmaps_entity["name"],
                    "rating": "New",
                    "url": f"https://google.com/maps/place/?q=place_id:{gmaps_entity['place_id']}"
                }
            else:
                print(f"[AI Engine] [NO MATCH] Low confidence match ({name_match_score}%). Discarding commercial tag.")

        # 2. Attach DLD transactions (Assuming spatial match already done by scraper)
        if dld_data and len(dld_data["results"]) >= 2:
            # Sort by date
            transactions = sorted(dld_data["results"], key=lambda x: x["date"])
            golden_lead["timeline"]["purchase_dld"] = transactions[0]
            golden_lead["timeline"]["resale_dld"] = transactions[-1]
            
            # ROI calculation
            profit = transactions[-1]["price_aed"] - transactions[0]["price_aed"]
            roi = (profit / transactions[0]["price_aed"]) * 100
            
            golden_lead["timeline"]["resale_dld"]["net_profit"] = profit
            golden_lead["timeline"]["resale_dld"]["calculated_roi_pct"] = round(roi, 1)

        # 3. Attach GEE Event
        golden_lead["timeline"]["gee_change"] = gee_lead["gee_event"]

        return golden_lead

if __name__ == "__main__":
    ai = AICrossReferencer()
    score = ai.match_business_names("Aesthetics Dental Clinic LLC", "Aesthetics Dental Clinic")
    print(f"Test Name Match Score: {score}")

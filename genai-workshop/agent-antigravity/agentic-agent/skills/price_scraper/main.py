import random

def main(params):
    """
    Skill: price_scraper
    Purpose: Simulates scraping B2B portals for the best price.
    """
    item_name = params.get("item_name")
    
    if not item_name:
        return {"error": "NO_VENDORS_FOUND", "message": "Search term is empty."}

    # Simulated vendor results
    vendors = [
        {"name": "GlobalSupply Corp", "price": round(random.uniform(40, 60), 2), "lead_time_days": 3},
        {"name": "FastTrack Logistics", "price": round(random.uniform(55, 75), 2), "lead_time_days": 1},
        {"name": "BulkIndustrial", "price": round(random.uniform(35, 45), 2), "lead_time_days": 7}
    ]
    
    return {"vendors": vendors}
def main(params):
    """
    Skill: check_stock
    Purpose: Retrieves inventory data from the mock ERP.
    """
    part_id = params.get("part_id")
    
    # Mock ERP Database
    inventory_db = {
        "PART_77A": {"stock": 12, "min_threshold": 50, "location": "Warehouse-B"},
        "PART_88B": {"stock": 250, "min_threshold": 100, "location": "Warehouse-A"},
        "PART_99C": {"stock": 5, "min_threshold": 20, "location": "Warehouse-C"}
    }
    
    if not part_id:
        return {"error": "INVALID_INPUT", "message": "part_id is required."}
        
    result = inventory_db.get(part_id)
    
    if not result:
        return {"error": "ITEM_NOT_FOUND", "message": f"Part {part_id} not in ERP."}
        
    return result
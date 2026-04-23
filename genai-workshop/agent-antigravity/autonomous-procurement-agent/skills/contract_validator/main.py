def main(params):
    """
    Skill: contract_validator
    Purpose: Ensures the order stays within budget and uses approved vendors.
    """
    total_cost = params.get("total_cost", 0)
    vendor_name = params.get("vendor_name", "")
    
    # Hardcoded business rules
    MAX_BUDGET = 50000.0
    APPROVED_VENDORS = ["GlobalSupply Corp", "FastTrack Logistics", "BulkIndustrial"]

    if vendor_name not in APPROVED_VENDORS:
        return {
            "status": "REJECTED",
            "message": f"Vendor '{vendor_name}' is not on the Approved Vendor List (AVL)."
        }

    if total_cost > MAX_BUDGET:
        return {
            "status": "REJECTED",
            "message": f"Order cost ${total_cost} exceeds authorized limit of ${MAX_BUDGET}."
        }
    
    return {
        "status": "VALIDATED",
        "message": "Compliance check passed: Within budget and approved vendor."
    }
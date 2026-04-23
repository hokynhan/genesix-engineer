import uuid
from datetime import datetime, timedelta

def main(params):
    """
    Skill: order_submit
    Purpose: Finalizes the purchase via external API.
    """
    part_id = params.get("part_id")
    vendor_name = params.get("vendor_name")
    quantity = params.get("quantity")

    if not all([part_id, vendor_name, quantity]):
        return {"error": "SUBMISSION_FAILED", "message": "Missing required order fields."}

    # Simulate an API call delay or successful response
    tx_id = f"ANTIGRAV-{uuid.uuid4().hex[:8].upper()}"
    arrival_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    return {
        "transaction_id": tx_id,
        "estimated_delivery": arrival_date,
        "status": "SUCCESS"
    }
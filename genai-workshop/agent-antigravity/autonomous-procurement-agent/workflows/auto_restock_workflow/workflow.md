# Workflow: Auto-Restock Disruption Guard

## Overview
An autonomous loop designed to monitor inventory depletion and execute procurement orders through validated vendor channels.

## Execution Steps

### 1. Inventory Check
- **Skill**: `check_stock`
- **Inputs**: 
    - `part_id`: `{{workflow.input.part_id}}`
- **Condition**: 
    - If `stock` < `min_threshold`, continue to **Step 2**.
    - Else, Terminate (Stock Adequate).

### 2. Market Sourcing
- **Skill**: `price_scraper`
- **Inputs**: 
    - `item_name`: `{{steps.1.outputs.part_name}}`
- **Logic**: Agent parses vendor list to select the lowest `price` with a `lead_time_days` < 3.

### 3. Compliance Audit
- **Skill**: `contract_validator`
- **Inputs**: 
    - `total_cost`: `{{agent.selection.total_price}}`
    - `vendor_name`: `{{agent.selection.vendor_name}}`
- **Condition**: 
    - If `status` == "VALIDATED", continue to **Step 4**.
    - If `status` == "REJECTED", Escalate to Human.

### 4. Execution
- **Skill**: `order_submit`
- **Inputs**: 
    - `part_id`: `{{workflow.input.part_id}}`
    - `vendor_name`: `{{agent.selection.vendor_name}}`
    - `quantity`: `{{agent.selection.optimal_quantity}}`
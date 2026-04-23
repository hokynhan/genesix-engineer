# Antigravity Ecosystem Registry

This registry serves as the central index for the autonomous procurement ecosystem.

## Agents
- **Procurement Officer**
  - **Path:** `agents/procurement_officer/agent.md`
  - **Status:** Active
  - **Description:** Autonomous buyer for inventory replenishment.

## Skills
- **check_stock**
  - **Path:** `skills/check_stock/skill.md`
  - **Implementation:** `skills/check_stock/main.py`
  - **Tags:** #erp #inventory #data
- **price_scraper**
  - **Path:** `skills/price_scraper/skill.md`
  - **Implementation:** `skills/price_scraper/main.py`
  - **Tags:** #web #finance #market
- **contract_validator**
  - **Path:** `skills/contract_validator/skill.md`
  - **Implementation:** `skills/contract_validator/main.py`
  - **Tags:** #legal #compliance #budget
- **order_submit**
  - **Path:** `skills/order_submit/skill.md`
  - **Implementation:** `skills/order_submit/main.py`
  - **Tags:** #api #procurement #action

## Workflows
- **auto_restock_workflow**
  - **Path:** `workflows/auto_restock_workflow.md`
  - **Primary Agent:** `procurement_officer`
  - **Trigger:** Schedule (Every 4 Hours) / Low Stock Event

## Connections
- **procurement_officer** is granted access to all skills listed above.
- **auto_restock_workflow** is the default behavior for **procurement_officer** when a stock anomaly is detected.

## Commands
- **/auto_restock_workflow**
  - **Workflow:** `workflows/auto_restock_workflow.md`
  - **Description:** Manually trigger the inventory check and restock loop.
  - **Arguments:** - `part_id`: (required) The SKU to process.
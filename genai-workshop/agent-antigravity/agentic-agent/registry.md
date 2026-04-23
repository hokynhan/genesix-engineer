# Antigravity Ecosystem Registry

This registry serves as the central index for the autonomous procurement ecosystem.

## Base Agents (Reasoning Engines)
- **base_autonomous_agent**
  - **Path:** `agents/agent_base.md`
  - **Type:** Core Reasoning Engine
  - **Description:** Provides the standard agent reasoning loop (Observe → Evaluate → Decide → Act → Adjust).
  - **Usage:** All agents MUST inherit from this base agent.

## Agents (Domain Extensions)
- **procurement_officer**
  - **Base:** `base_autonomous_agent`
  - **Domain Path:** `agents/procurement_officer/procurement_agent.md`
  - **Status:** Active
  - **Description:** Autonomous buyer for inventory replenishment.
- **growth_strategist**
  - **Base:** `base_autonomous_agent`
  - **Domain Path:** `agents/growth_strategist/growth_strategist_agent.md`
  - **Status:** Active
  - **Description:** Autonomous marketing agent for content lifecycle and virality analysis.

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
- **analyze_sentiment**
  - **Path:** `skills/analyze_sentiment/skill.md`
  - **Implementation:** `skills/analyze_sentiment/main.py`
  - **Tags:** #nlp #semantic #repurposing
- **content_generator**
  - **Path:** `skills/content_generator/skill.md`
  - **Implementation:** `skills/content_generator/main.py`
  - **Tags:** #creative #format #automation
- **fetch_engagement_data**
  - **Path:** `skills/fetch_engagement_data/skill.md`
  - **Implementation:** `skills/fetch_engagement_data/main.py`
  - **Tags:** #analytics #api #metrics
- **social_scheduler**
  - **Path:** `skills/social_scheduler/skill.md`
  - **Implementation:** `skills/social_scheduler/main.py`
  - **Tags:** #api #distribution #scheduling

## Workflows
- **auto_restock_workflow**
  - **Path:** `workflows/auto_restock_workflow.md`
  - **Primary Agent:** `procurement_officer`
  - **Trigger:** Schedule (Every 4 Hours) / Low Stock Event
- **content_repurposing_workflow**
  - **Path:** `workflows/content_repurposing_workflow/workflow.md`
  - **Primary Agent:** `growth_strategist`
  - **Trigger:** Performance Spike (> 20% engagement increase)

## Connections
- **procurement_officer** is granted access to **check_stock**, **price_scraper**, **contract_validator**, and **order_submit**.
- **growth_strategist** is granted access to **analyze_sentiment**, **content_generator**, **fetch_engagement_data**, and **social_scheduler**.
- **auto_restock_workflow** is the default behavior for **procurement_officer** when a stock anomaly is detected.
- **content_repurposing_workflow** is the default behavior for **growth_strategist** when a virality spike is detected.

## Commands
- **/auto_restock_workflow**
  - **Workflow:** `workflows/auto_restock_workflow.md`
  - **Description:** Manually trigger the inventory check and restock loop.
  - **Arguments:** - `part_id`: (required) The SKU to process.
- **/content_repurposing_workflow**
  - **Workflow:** `workflows/content_repurposing_workflow.md`
  - **Description:** Initiates autonomous analysis and cross-platform distribution for a specific asset.
  - **Arguments:** - `post_id`: (optional) The target content ID.
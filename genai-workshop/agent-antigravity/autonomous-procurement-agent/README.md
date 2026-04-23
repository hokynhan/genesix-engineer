# Antigravity Procurement Ecosystem 🚀

This repository contains a reference implementation of an autonomous supply chain agent built on the **Antigravity Framework**. It demonstrates the separation of **Agents**, **Skills**, and **Workflows** to create a self-healing inventory management system.

---

## 🏗️ Architecture Overview

The system is built on the **Antigravity Triad**:

1.  **The Agent (The Brain):** An autonomous `Procurement Officer` that makes reasoning-based decisions on vendor selection and budget management.
2.  **The Skills (The Tools):** Atomic Python functions that interact with ERPs, scrapers, and legal validators.
3.  **The Workflow (The Path):** A structured logic flow (`Auto-Restock Disruption Guard`) that orchestrates the agent's actions when stock is low.

---

## 📂 Project Structure

```text
.
├── registry.md              # Central manifest of all components
├── agents/
│   └── procurement_officer/
│       └── agent.md         # Persona and decision logic
├── skills/
│   ├── check_stock/         # ERP connectivity
│   ├── price_scraper/       # Market data aggregation
│   ├── contract_validator/  # Compliance & budget checking
│   └── order_submit/        # Transaction execution
└── workflows/
    └── auto_restock_workflow.md # Multi-step orchestration logic
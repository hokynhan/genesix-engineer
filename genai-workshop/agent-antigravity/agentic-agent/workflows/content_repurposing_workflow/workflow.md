# Workflow: content_repurposing_workflow

## Overview
Defines the goals, constraints, and conditions for autonomous identification and repurposing of high-performing marketing content.

> ⚠️ This workflow contains no execution steps.  
> The agent determines all actions dynamically based on performance signals.

---

## Input

- `post_id`: `{{workflow.input.post_id}}` (Optional: If empty, agent scans all recent content)

---

## Goal

Maximize the reach of high-performing content by identifying engagement spikes and autonomously distributing repurposed versions across secondary platforms.

---

## Constraints

- Repurposing must only be triggered if `increase_pct` > 20% over the 30-day average.
- Social threads must maintain the original "vibe" and sentiment of the source material.
- Posts must be scheduled for peak traffic windows only (e.g., 09:00 - 11:00 AM).
- Generated content must include a call-to-action (CTA) back to the original source.

---

## Success Condition

- `job_id` generated and content successfully queued in `social_scheduler`.

---

## Failure Conditions

- No content exceeds the 20% engagement threshold.
- Content generation fails to meet platform character limits.
- Social API authentication error.
- Sentiment analysis indicates negative or controversial triggers unsuitable for automation.

---

## Escalation

If any failure condition is met (excluding "No viral signal found"):
→ Notify `marketing_manager`

---

## Tool Requirements

This workflow assumes the agent has access to tools required for:
- Performance metric retrieval (`fetch_engagement_data`)
- Natural Language Processing (`analyze_sentiment`)
- Creative content transformation (`content_generator`)
- Platform scheduling (`social_scheduler`)

---

## Notes

- This workflow defines environment and rules only.
- Capabilities and creative "voice" are defined in the agent.
- The agent is responsible for:
  - Selecting the optimal target platform (e.g., LinkedIn vs X).
  - Drafting the specific "hook" based on sentiment data.
  - Adapting the distribution strategy based on the content type.
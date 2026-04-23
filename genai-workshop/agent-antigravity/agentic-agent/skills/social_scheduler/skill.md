# social_scheduler

## Description
Interfaces with external social media APIs to queue repurposed content for distribution. It calculates optimal posting windows based on platform-specific peak traffic data.

## Context
The final execution step in the content repurposing workflow. It transitions a drafted social thread from the agent's workspace to a live platform queue.

---

## Inputs

- `post_content`: (string) The finalized, formatted text to be published.
- `platform`: (string) The target destination (e.g., "LinkedIn", "X", "Threads").
- `scheduled_time`: (string) Default is "Next_Available_Slot". Can accept ISO 8601 timestamps.

---

## Outputs

- `status`: (string) "QUEUED" or "FAILED".
- `platform`: (string) Confirmed destination platform.
- `scheduled_iso`: (string) The exact timestamp the post is set to go live.
- `job_id`: (string) Unique reference ID for the scheduled task.

---

## Constraints
- Must validate content length against platform-specific character limits (e.g., 280 for X, 3000 for LinkedIn).
- Cannot schedule more than 5 posts in a 24-hour period to prevent "spam" flagging.
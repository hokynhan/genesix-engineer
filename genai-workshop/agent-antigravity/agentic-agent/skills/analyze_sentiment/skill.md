# Skill: analyze_sentiment

## Description
Performs semantic analysis on source text to identify emotional triggers, tone, and key themes. This allows the agent to maintain brand consistency when repurposing content.

## Context
Used by the Growth Strategist to understand *why* a post is performing well before attempting to rewrite it for a secondary platform.

---

## Inputs

- `text`: (string) The full body text of the high-performing content.

---

## Outputs

- `status`: (string) "SUCCESS" or "ERROR".
- `analysis`: (object)
    - `sentiment_score`: (float) Numeric representation of positivity/negativity.
    - `primary_emotion`: (string) The dominant emotional driver (e.g., "Inspirational", "Fear of Missing Out").
    - `tone`: (string) The stylistic approach (e.g., "Provocative", "Educational").
- `hook_suggestion`: (string) A recommended angle for the social media "hook."

---

## Constraints
- Must handle text up to 10,000 characters.
- If sentiment is "Highly Negative" or "Controversial," the skill must flag a warning for human review.
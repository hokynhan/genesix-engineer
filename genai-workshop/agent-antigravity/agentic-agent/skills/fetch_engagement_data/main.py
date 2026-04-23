import random

def main(params):
    """
    Skill: fetch_engagement_data
    Purpose: Retrieves performance metrics. 
    Logic: If post_id is provided, fetch that specific post. 
           If post_id is empty, scan all content and return the top performer.
    """
    target_id = params.get("post_id")
    time_period = params.get("time_period", "last_24_hours")
    
    # Mock Content Database
    content_library = [
        {"post_id": "BLOG_001", "title": "The Future of AI Agents", "base_engagement": 0.04, "content": "Full text of BLOG_001..."},
        {"post_id": "BLOG_002", "title": "Supply Chain Automation Tips", "base_engagement": 0.03, "content": "Full text of BLOG_002..."},
        {"post_id": "BLOG_003", "title": "Why Antigravity is Different", "base_engagement": 0.05, "content": "Full text of BLOG_003..."},
        {"post_id": "BLOG_004", "title": "Marketing in 2026", "base_engagement": 0.02, "content": "Full text of BLOG_004..."}
    ]

    processed_posts = []

    # 1. Process all posts with simulated real-time fluctuations
    for post in content_library:
        # Simulate a "Viral Spike" (randomly scales engagement)
        spike_factor = random.uniform(0.8, 1.8) 
        current_engagement = round(post["base_engagement"] * spike_factor, 3)
        increase_pct = round(((current_engagement - post["base_engagement"]) / post["base_engagement"]) * 100, 2)

        processed_posts.append({
            "post_id": post["post_id"],
            "title": post["title"],
            "engagement_rate": current_engagement,
            "increase_pct": increase_pct,
            "content": post["content"],
            "views": random.randint(1000, 5000)
        })

    # 2. Selection Logic
    selected_post = None

    if target_id:
        # Scenario A: User/Workflow requested a specific ID
        selected_post = next((p for p in processed_posts if p["post_id"] == target_id), None)
        if not selected_post:
            return {"error": "NOT_FOUND", "message": f"Post ID {target_id} not found."}
    else:
        # Scenario B: No ID provided, find the post with the highest increase_pct (The "Viral" choice)
        processed_posts.sort(key=lambda x: x['increase_pct'], reverse=True)
        selected_post = processed_posts[0]

    # 3. Return payload formatted for Agent consumption
    return {
        "status": "SUCCESS",
        "mode": "TARGETED" if target_id else "DISCOVERY",
        "time_period": time_period,
        "post_id": selected_post["post_id"],
        "title": selected_post["title"],
        "increase_pct": selected_post["increase_pct"],
        "engagement_rate": selected_post["engagement_rate"],
        "top_post_content": selected_post["content"],
        "all_scanned_metrics": processed_posts if not target_id else [selected_post]
    }
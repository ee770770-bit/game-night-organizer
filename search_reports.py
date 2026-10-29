"""
search_reports.py - Querying, tag search, and statistical summary reports.
"""

def search_by_tag(games, tag):
    """Case-insensitive search for games containing a specific tag."""
    if not games or not tag:
        return []
    tag_clean = tag.strip().lower()
    return [g for g in games if any(tag_clean == t.lower() for t in g["tags"])]

def get_games_summary(games):
    """Generates catalog summary statistics."""
    if not games:
        return {"total": 0, "avg_duration": 0.0, "all_tags": []}

    total = len(games)
    avg_duration = sum(g["duration"] for g in games) / total
    all_tags = sorted(list({t.lower() for g in games for t in g["tags"]}))

    return {
        "total": total,
        "avg_duration": round(avg_duration, 1),
        "all_tags": all_tags
    }
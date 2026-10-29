"""
recommender.py - Game ranking, filtering, scoring, and tie-breaking algorithms.
"""

def filter_games(games, players_count, max_time):
    """
    Strict filter: excludes games that do not fit the player count or exceed the time limit.
    """
    if not games or players_count <= 0 or max_time <= 0:
        return []

    eligible = []
    for g in games:
        if g["min_players"] <= players_count <= g["max_players"] and g["duration"] <= max_time:
            eligible.append(g)
    return eligible

def calculate_game_score(game, preferred_tags, target_duration):
    """
    Calculates a match score and explanation:
    - +10 points per matching tag.
    - Duration proximity bonus: up to +10 points the closer it is to the available time.
    """
    score = 0
    reasons = []

    preferred_clean = [t.lower() for t in preferred_tags]
    matching_tags = [t for t in game["tags"] if t.lower() in preferred_clean]
    if matching_tags:
        tag_points = len(matching_tags) * 10
        score += tag_points
        reasons.append(f"Matches preferred tags: {', '.join(matching_tags)} (+{tag_points} pts)")

    time_diff = target_duration - game["duration"]
    time_points = max(0, 10 - (time_diff // 10))
    score += time_points
    reasons.append(f"Duration {game['duration']}m fits target time window (+{time_points} pts)")

    return score, "; ".join(reasons)

def rank_games(games, players_count, max_time, preferred_tags=None):
    """
    Ranks eligible games descending by score.
    Tie-breaking: longer duration first, then alphabetical by name.
    """
    if preferred_tags is None:
        preferred_tags = []

    eligible = filter_games(games, players_count, max_time)
    if not eligible:
        return []

    ranked_results = []
    for game in eligible:
        score, reason = calculate_game_score(game, preferred_tags, max_time)
        ranked_results.append({
            "game": game,
            "score": score,
            "reason": reason
        })

    ranked_results.sort(
        key=lambda item: (-item["score"], -item["game"]["duration"], item["game"]["name"])
    )
    return ranked_results
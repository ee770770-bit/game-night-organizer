"""
games_data.py - Board game catalog management and data validation.
"""

def get_initial_games():
    """Returns sample game records to initialize the catalog."""
    return [
        {
            "id": "catan",
            "name": "Catan",
            "min_players": 3,
            "max_players": 4,
            "duration": 75,
            "tags": ["strategy", "board"]
        },
        {
            "id": "codenames",
            "name": "Codenames",
            "min_players": 4,
            "max_players": 8,
            "duration": 20,
            "tags": ["party", "words"]
        },
        {
            "id": "dixit",
            "name": "Dixit",
            "min_players": 3,
            "max_players": 6,
            "duration": 30,
            "tags": ["party", "creative"]
        },
        {
            "id": "carcassonne",
            "name": "Carcassonne",
            "min_players": 2,
            "max_players": 5,
            "duration": 45,
            "tags": ["strategy", "tile-placement"]
        },
        {
            "id": "taco_cat",
            "name": "Taco Cat Goat Cheese Pizza",
            "min_players": 3,
            "max_players": 8,
            "duration": 15,
            "tags": ["fast", "party"]
        }
    ]

def validate_game_data(game_data, existing_games):
    """
    Validates a game record.
    Returns (is_valid: bool, error_message: str).
    """
    required_keys = ["id", "name", "min_players", "max_players", "duration", "tags"]
    for key in required_keys:
        if key not in game_data or game_data[key] in (None, ""):
            return False, f"Missing or empty field: {key}"

    if any(g["id"] == game_data["id"] for g in existing_games):
        return False, f"Game ID '{game_data['id']}' already exists."

    if not isinstance(game_data["min_players"], int) or game_data["min_players"] <= 0:
        return False, "min_players must be a positive integer."

    if not isinstance(game_data["max_players"], int) or game_data["max_players"] < game_data["min_players"]:
        return False, "max_players must be an integer greater than or equal to min_players."

    if not isinstance(game_data["duration"], int) or game_data["duration"] <= 0:
        return False, "duration must be a positive integer in minutes."

    if not isinstance(game_data["tags"], list) or len(game_data["tags"]) == 0:
        return False, "tags must be a non-empty list of strings."

    return True, "Valid"

def add_game(games_list, new_game):
    """
    Validates and adds a game to the catalog.
    Returns a new updated list without mutating the original input.
    """
    is_valid, msg = validate_game_data(new_game, games_list)
    if not is_valid:
        raise ValueError(msg)
    updated_list = list(games_list)
    updated_list.append(new_game)
    return updated_list
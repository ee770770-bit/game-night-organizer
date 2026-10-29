"""
main.py - Interactive CLI interface and application entry point.
"""
from games_data import get_initial_games, add_game
from recommender import rank_games
from search_reports import search_by_tag, get_games_summary

def print_menu():
    print("\n=== Game Night Organizer ===")
    print("1. View All Games & Catalog Summary")
    print("2. Add a New Game")
    print("3. Search Games by Tag")
    print("4. Get Ranked Recommendations (Core Logic)")
    print("5. Exit")

def handle_add_game(games):
    print("\n--- Add a New Game ---")
    game_id = input("Game ID (e.g. ticket_to_ride): ").strip().lower()
    name = input("Game Name: ").strip()
    try:
        min_p = int(input("Minimum Players: "))
        max_p = int(input("Maximum Players: "))
        duration = int(input("Duration in minutes: "))
    except ValueError:
        print("Error: Player counts and duration must be integers.")
        return games

    tags_str = input("Tags (comma-separated, e.g. strategy, board): ")
    tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]

    new_game = {
        "id": game_id,
        "name": name,
        "min_players": min_p,
        "max_players": max_p,
        "duration": duration,
        "tags": tags
    }

    try:
        updated = add_game(games, new_game)
        print(f"Success: Game '{name}' added successfully!")
        return updated
    except ValueError as e:
        print(f"Validation Error: {e}")
        return games

def handle_recommendations(games):
    print("\n--- Find the Best Games for Tonight ---")
    try:
        players = int(input("Number of players: "))
        time_limit = int(input("Available time (minutes): "))
    except ValueError:
        print("Error: Player count and time limit must be integers.")
        return

    tags_input = input("Preferred styles/tags (comma-separated, or leave empty): ")
    preferred_tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()]

    results = rank_games(games, players, time_limit, preferred_tags)

    if not results:
        print("No matching games found for the given player count and time window.")
        return

    print(f"\nFound {len(results)} matching game(s) (ranked highest to lowest):")
    for idx, r in enumerate(results, 1):
        g = r["game"]
        print(f"{idx}. {g['name']} (Match Score: {r['score']})")
        print(f"   Players: {g['min_players']}-{g['max_players']} | Duration: {g['duration']}m")
        print(f"   Why recommended: {r['reason']}")

def main():
    games = get_initial_games()
    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            summary = get_games_summary(games)
            print(f"\nTotal Games: {summary['total']} | Avg Duration: {summary['avg_duration']} mins")
            print(f"Available Tags: {', '.join(summary['all_tags'])}")
            print("-" * 45)
            for g in games:
                print(f"- {g['name']} ({g['min_players']}-{g['max_players']} players, {g['duration']}m) [Tags: {', '.join(g['tags'])}]")
        elif choice == "2":
            games = handle_add_game(games)
        elif choice == "3":
            tag = input("Enter tag to search: ").strip()
            found = search_by_tag(games, tag)
            if found:
                print(f"Found {len(found)} game(s) matching '{tag}':")
                for g in found:
                    print(f"- {g['name']} ({g['duration']} mins)")
            else:
                print(f"No games found with tag '{tag}'.")
        elif choice == "4":
            handle_recommendations(games)
        elif choice == "5":
            print("Goodbye! Enjoy your game night.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
from flask import Flask, jsonify, request

app = Flask(__name__)

standings = [
    {"team_id": 1, "team": "Team A", "wins": 3, "losses": 1},
    {"team_id": 2, "team": "Team B", "wins": 2, "losses": 2},
]

next_team_id = 3


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Mini Tournament Scoreboard API!",
        "available_endpoints": [
            "/standings (GET)",
            "/standings/<team_id> (GET)",
            "/standings (POST)",
            "/standings/<team_id> (PUT)",
            "/standings/<team_id> (DELETE)",
        ],
    })


def find_team(team_id):
    return next((team for team in standings if team["team_id"] == team_id), None)


def error(message, status=400):
    return jsonify({"error": message}), status


@app.route("/standings", methods=["GET"])
def get_standings():
    ordered = sorted(
        standings,
        key=lambda team: (-team["wins"], team["losses"], team["team"].casefold()),
    )
    return jsonify(ordered), 200


@app.route("/standings/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    data = request.get_json(silent=True)

    if data is None:
        return error("The request body must be JSON. :<", 400)

    for field in ("team", "wins", "losses"):
        if field not in data:
            return error(f"Missing field: {field}. :<", 400)

    name = data.get("team")
    wins = data.get("wins")
    losses = data.get("losses")

    if not isinstance(name, str) or name.strip() == "":
        return error("The team must not be empty. :<", 400)

    if not isinstance(wins, int) or isinstance(wins, bool) or wins < 0:
        return error("The wins must be a whole number not less than 0. :<", 400)

    if not isinstance(losses, int) or isinstance(losses, bool) or losses < 0:
        return error("The losses must be a whole number not less than 0. :<", 400)

    team["team"] = name.strip()
    team["wins"] = wins
    team["losses"] = losses

    return jsonify(team), 200


@app.route("/standings/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    return jsonify(team), 200


@app.route("/standings", methods=["POST"])
def create_team():
    global next_team_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("A JSON object is required. :<", 400)

    team_name = data.get("team")

    if not isinstance(team_name, str) or not team_name.strip():
        return error("Team name is required. :<", 400)

    team_name = team_name.strip()

    if any(t["team"].casefold() == team_name.casefold() for t in standings):
        return error("Team already exists. :<", 409)

    team = {
        "team_id": next_team_id,
        "team": team_name,
        "wins": 0,
        "losses": 0,
    }

    standings.append(team)
    next_team_id += 1

    return jsonify(team), 201


@app.route("/standings/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    standings.remove(team)

    return jsonify({"message": "Team deleted successfully. :>"}), 200


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request

app = Flask(__name__)

standings = [
    {"team_id": 1, "team": "Team A", "wins": 3, "losses": 1},
    {"team_id": 2, "team": "Team B", "wins": 2, "losses": 2}
]

next_team_id = 3

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Mini Tournament Scoreboard API!",
        "available_endpoints": [
            {"method": "GET", "path": "/standings"},
            {"method": "GET", "path": "/standings/<int:team_id>"},
            {"method": "POST", "path": "/standings"},
            {"method": "PUT", "path": "/standings/<int:team_id>"},
            {"method": "DELETE", "path": "/standings/<int:team_id>"}
        ]
    })

def find_team(team_id):
    return next((team for team in standings if team["team_id"] == team_id), None)

def error(message, status=400):
    return jsonify({"error": message}), status

def team_exists(name, exclude_id=None):
    return any(
        team["team"].casefold() == name.casefold()
        and team["team_id"] != exclude_id
        for team in standings
    )

def valid_stats(wins, losses):
    return (
        type(wins) is int and wins >= 0
        and type(losses) is int and losses >= 0
    )

@app.route("/standings", methods=["GET"])
def get_standings():
    ordered = sorted(
        standings,
        key=lambda team: (
            -team["wins"],
            team["losses"],
            team["team"].casefold()
        )
    )
     
    return jsonify({
        "message": "Standings retrieved successfully. :>",
        "standings": ordered
    }), 200

@app.route("/standings/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    return jsonify({
        "message": "Team retrieved successfully. :>",
        "team": team
    }), 200

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

    if team_exists(team_name):
        return error("Team already exists. :<", 409)

    team = {
        "team_id": next_team_id,
        "team": team_name,
        "wins": 0,
        "losses": 0
    }

    standings.append(team)
    next_team_id += 1

    return jsonify({
        "message": "Team created successfully. :>",
        "team": team
    }), 201

@app.route("/standings/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("A JSON object is required. :<", 400)

    if not all(field in data for field in ("team", "wins", "losses")):
        return error("Team, wins, and losses are required. :<", 400)
    
    team_name = data["team"]
    wins = data["wins"]
    losses = data["losses"]
    
    if not isinstance(team_name, str) or not team_name.strip():
        return error("Team name cannot be empty. :<", 400)

    team_name = team_name.strip()
    
    if team_exists(team_name, team_id):
        return error("Team already exists. :<", 409)

    if not valid_stats(wins, losses):
        return error("Wins and losses must be non-negative integers. :<", 400)

    team.update({
        "team": team_name,
        "wins": wins,
        "losses": losses
    })
    
    return jsonify({
        "message": "Team updated successfully. :>",
        "team": team
    }), 200

@app.route("/standings/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    team = find_team(team_id)

    if team is None:
        return error("Team not found. :<", 404)

    standings.remove(team)

    return jsonify({
        "message": "Team deleted successfully. :>",
        "team_id": team_id
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
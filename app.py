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
            "/standings (GET)",
            "/standings/<team_id> (GET)",
            "/standings (POST)",
            "/standings/<team_id> (PUT)",
            "/standings/<team_id> (DELETE)"
        ]
    })

def find_team(team_id):
    return next((team for team in standings if team["team_id"] == team_id), None)

def error(message, status=400):
    return jsonify({"error": message}), status

@app.route("/standings", methods=["GET"])
def get_standings():
    ordered = sorted(
        standings,
        key=lambda team: (-team["wins"], team["losses"], team["team"].casefold())
    )
    return jsonify(ordered), 200

#Mi parte
@app.route("/standings/<int:team_id>", methods=['PUT'])
def update_team(team_id)
    if team is None:
        return error(f"Team not founderror", 404)

    data = request.get_json(silent = True)
    if data is None:
        return error("The request body must be JSON")

    for field in ("team", "wins", "losses"):
        if field not in data:
            return error(f"Missing field: {data}")

    name = data['team']
    wins = data['wins']
    losses = data['losses']

    
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request

app = Flask(__name__)

standings = [
    {"team_id": 1, "team": "Team A", "wins": 3, "losses": 1},
    {"team_id": 2, "team": "Team B", "wins": 2, "losses": 2}
]

next_team_id = 3

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

if __name__ == "__main__":
    app.run(debug=True)
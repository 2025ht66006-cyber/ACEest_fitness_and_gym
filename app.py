from flask import Flask, jsonify, request

app = Flask(__name__)

members = [
    {"id": 1, "name": "Alice", "plan": "Premium", "workouts": ["cardio", "strength"]},
    {"id": 2, "name": "Bob", "plan": "Standard", "workouts": ["yoga"]},
]

workouts = [
    {"id": 1, "name": "cardio", "duration": 30},
    {"id": 2, "name": "strength", "duration": 45},
    {"id": 3, "name": "yoga", "duration": 60},
]

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "ACEest Fitness Gym API"})

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members)

@app.route("/members", methods=["POST"])
def add_member():
    payload = request.get_json() or {}
    if "name" not in payload or "plan" not in payload:
        return jsonify({"error": "name and plan required"}), 400
    new_id = max(m["id"] for m in members) + 1
    new_member = {"id": new_id, "name": payload["name"], "plan": payload["plan"], "workouts": payload.get("workouts", [])}
    members.append(new_member)
    return jsonify(new_member), 201

@app.route("/workouts", methods=["GET"])
def get_workouts():
    return jsonify(workouts)

@app.route("/metrics", methods=["GET"])
def get_metrics():
    return jsonify({
        "members_count": len(members),
        "workouts_count": len(workouts),
        "avg_workouts_per_member": round(sum(len(m["workouts"]) for m in members) / len(members), 2),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

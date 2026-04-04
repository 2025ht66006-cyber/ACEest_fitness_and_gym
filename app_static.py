from flask import Flask, jsonify, request, send_file
import os

static_folder = os.path.join(os.path.dirname(__file__), "static")
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

@app.route("/")
def serve_index():
    return send_file(os.path.join(static_folder, "index.html"))

@app.route("/index.html")
def serve_index_direct():
    return send_file(os.path.join(static_folder, "index.html"))

@app.route("/style.css")
def serve_css():
    return send_file(os.path.join(static_folder, "style.css"), mimetype="text/css")

@app.route("/main.js")
def serve_js():
    return send_file(os.path.join(static_folder, "main.js"), mimetype="application/javascript")

@app.route("/members", methods=["GET", "POST"])
def members_handler():
    if request.method == "GET":
        return jsonify(members)
    payload = request.get_json() or {}
    if "name" not in payload or "plan" not in payload:
        return jsonify({"error": "name and plan required"}), 400
    new_id = max(m["id"] for m in members) + 1
    new_member = {
        "id": new_id,
        "name": payload["name"],
        "plan": payload["plan"],
        "workouts": payload.get("workouts", []),
    }
    members.append(new_member)
    return jsonify(new_member), 201

@app.route("/workouts")
def get_workouts():
    return jsonify(workouts)

@app.route("/metrics")
def get_metrics():
    avg = 0
    if members:
        avg = round(sum(len(m["workouts"]) for m in members) / len(members), 2)
    return jsonify({
        "members_count": len(members),
        "workouts_count": len(workouts),
        "avg_workouts_per_member": avg,
    })

if __name__ == "__main__":
    print(f"Starting server... Static folder: {static_folder}")
    app.run(host="0.0.0.0", port=5000, debug=False)

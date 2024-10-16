from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "m1a2r3k4"

assignments = [
    {"subject": "Math", "assignment": "Algebra", "due_date": "2021-10-10", "id": 1, "done": False},
]


@app.before_request
def Authenticate():
    userToken = request.headers.get("Authorization")
    if not userToken or userToken != "Bearer " + TOKEN:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/assignments", methods=["GET"])
def get_assignments():
    return jsonify(assignments)


@app.route("/assignments", methods=["POST"])
def add_assignment():
    assignment = request.json
    idExist = [True for assignment in assignments if assignment["id"] == assignment["id"]]
    if "subject" not in assignment or "assignment" not in assignment or "due_date" not in assignment or assignment["id"] in idExist:
        return jsonify({"error": "Missing data or wrong id"}), 400
    assignments.append(assignment)
    return jsonify({"message": "Assignment added successfully"}), 201

@app.route("/assignments/<int:id>", methods=["DELETE"])
def delete_assignment(id):
    global assignments
    assignments = [assignment for assignment in assignments if assignment["id"] != id]
    return "",204

@app.route("/assignments/done/<int:id>", methods=["PUT"])
def update_assignment(id):
    for a in range(len(assignments)):
        if assignments[a]["id"] == id:
            assignments[a]["done"]= True
            return jsonify({"message": "Assignment updated successfully"}), 200
    return jsonify({"error": "Assignment not found"}), 404

@app.route("/assignments/undone/<int:id>", methods=["PUT"])
def update_assignment_not(id):
    for a in range(len(assignments)):
        if assignments[a]["id"] == id:
            assignments[a]["done"]= False
            return jsonify({"message": "Assignment updated successfully"}), 200
    return jsonify({"error": "Assignment not found"}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

app.run(port=3000)
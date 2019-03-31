from flask import (
    Flask,
    jsonify,
    abort,
    make_response,
    request,
    url_for
)

app = Flask(__name__)

student_data = {
    "John": {
        "id": 1,
        "grade": "A"
    },
    "Doe": {
        "id": 2,
        "grade": "B"
    }
}


@app.route("/task", methods=["GET"])
def initiate_student():
    app.logger.warning("THIS IS A LOG")
    return jsonify({"student_data": student_data})
# curl -i http://127.0.0.1:5000/task/


# @app.route("/task/<string:student_name>", methods=["GET"])
# def get_student_data(student_name):
#     query_student_data = student_data.get(student_name)
#     if not query_student_data:
#         abort(404)
#     return jsonify({"query_res": query_student_data})
# curl -i http://127.0.0.1:5000/task/Doe


@app.route("/task/insert", methods=["POST"])
def create_student():
    if not request.json:
        abort(400)
    res = request.json

    student_data[res.get("name")] = {
        "id": res.get("id"),
        "grade": res.get("grade")
    }
    return jsonify({"student_data": student_data}, 201)
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Smith", "id": 3, "grade": "C"}'
# http://127.0.0.1:5000/task/insert


@app.route("/task/edit/<string:student_name>", methods=["PUT"])
def edit_student(student_name):
    if student_name not in student_data.keys():
        abort(404)
    if not request.json:
        abort(400)
    # if student_name in student_data.keys() and type(request.json["grade"]) != :
    student_data["John"]["grade"] = request.json["grade"]
    return jsonify({"student_data": student_data})
# curl -i -H "Content-Type: application/json" -X PUT -d '{"grade": "X"}' http://127.0.0.1:5000/task/edit/John


@app.route("/task/remove/<string:student_name>", methods=["DELETE"])
def remove_student(student_name):
    if student_name not in student_data.keys():
        abort(404)
    return jsonify(student_data.pop(student_name))
# curl -X "DELETE" http://127.0.0.1:5000/task/remove/Doe


def make_public_data(student_data):
    new_student_data = dict()
    for student_name, info in student_data.items():
        for key, value in info.items():
            if key == "id":
                new_student_data[student_name] = url_for("initiate_student", student_id=value, _external=True)
    return new_student_data


@app.route("/student_data", methods=["GET"])
def get_student_data():
    return jsonify({"student_data": [make_public_data(student_data)]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(debug=True)

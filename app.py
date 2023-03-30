from flask import Flask
from flask import request
import copy

app = Flask(__name__)

group_example = {
    "id": 1,
    "name": "asd",
    "description": "asd",
    "participants": []
}

group_list = []


@app.route('/group', methods=["POST"])
def group_create():
    param = request.get_json()
    if "name" not in param.keys():
        return "Name required", 400
    if "description" not in param.keys():
        param["description"] = ""
    new_id = len(group_list) + 1
    new_group = {
        "id": new_id,
        "name": param["name"],
        "description": param["description"],
        "participants": []
    }
    group_list.append(new_group)
    return str(new_id), 201


@app.route('/groups', methods=["GET"])
def group_get():
    group_resp = []
    for group in group_list:
        group_resp.append(
            {
                "id": group["id"],
                "name": group["name"],
                "description": group["description"],
            }
        )

    return group_resp

@app.route('/group/<int:id>', methods=["GET"])
def group_get_by_id(id):

    for group in group_list:
        if group["id"] == id:
            return group
    return "Not Found", 404

@app.route('/group/<int:id>', methods=["DELETE"])
def group_delete(id):
    for group in group_list:
        if group["id"] == id:
            id_delete = group_list.index(group)
            group_list.pop(id_delete)
            return "OK", 200
    return "Not Found", 404

@app.route('/group/<int:id>', methods=["PUT"])
def group_edit(id):
    params = request.get_json()
    if "name" not in params.keys():
        return "Name required", 400
    if "description" not in params.keys():
        params["description"] = ""
    for group in group_list:
        if group["id"] == id:
            group["name"] = params["name"]
            group["description"] = params["description"]
            return "OK", 200
    return "Not Found", 404

@app.route('/group/<int:id>/participant', methods=["POST"])
def add_participant(id):
    param = request.get_json()
    if "name" not in param.keys():
        return "Name required", 400
    if "wish" not in param.keys():
        param["wish"] = ""
    for group in group_list:
        if group["id"] == id:
            participant_list = group["participants"]

            new_id = len(participant_list) + 1
            new_participant = {
                "id": new_id,
                "name": param["name"],
                "wish": param["wish"],

            }
            participant_list.append(new_participant)
            return str(new_id)

@app.route('/group/<int:id>/participant/<int:idpart>', methods=["DELETE"])
def delete_participant(id, idpart):
    for group in group_list:
        if group["id"] == id:
            participant_list = group["participants"]
            for participant in participant_list:
                if participant["id"] == idpart:
                    id_delete = participant_list.index(participant)
                    participant_list.pop(id_delete)
                    return "OK", 200
    return "Not Found", 404

@app.route('/group/<int:id>/toss', methods=["POST"])
def toss(id):
    for group in group_list:
        if group["id"] == id:
            participant_list = group["participants"]
            if len(participant_list) < 3:
                return "Conflict, participants less than 3", 409
            participant_list_copy = copy.deepcopy(participant_list)
            # participant_list_allowed = copy.copy(participant_list)
            i = len(participant_list)
            while i != 0:
                participant_list[i-1]["recipient"] = participant_list_copy[i - 2]
                i = i - 1


            return participant_list

@app.route('/group/<int:id>/participant/<int:id_part>/recipient', methods=["GET"])
def get_recipient(id, id_part):
    for group in group_list:
        if group["id"] == id:
            participant_list = group["participants"]
            for participant in participant_list:
                if participant["id"] == id_part:
                    return participant["recipient"]
    return "Not Found", 404


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

import datetime

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import StickyNote, User

stickynotes_blueprint = Blueprint("stickynotes", __name__)


class AddAPI(MethodView):
    def post(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                post_data = request.get_json()

                try:
                    stickynote = StickyNote(user_id=post_data.get("user_id"),
                                            note_content=post_data.get("note_content"))

                    db.session.add(stickynote)
                    db.session.commit()

                    response_object = {
                        "status": "success",
                        "message": "Successfully added."
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    print(e)
                    response_object = {
                        "status": "fail",
                        "message": "Some error occurred. Please try again."
                    }
                    return make_response(jsonify(response_object)), 400
            else:
                response_object = {
                    "status": "fail",
                    "message": resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid token."
            }
            return make_response(jsonify(response_object)), 403


class DeleteAPI(MethodView):
    def post(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                post_data = request.get_json()

                try:
                    StickyNote.query.filter_by(id=post_data.get("id")).delete()
                    db.session.commit()

                    response_object = {
                        "status": "success",
                        "message": "Successfully deleted."
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    print(e)
                    response_object = {
                        "status": "fail",
                        "message": "Some error occurred. Please try again."
                    }
                    return make_response(jsonify(response_object)), 400
            else:
                response_object = {
                    "status": "fail",
                    "message": resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid token."
            }
            return make_response(jsonify(response_object)), 403


class UpdateAPI(MethodView):
    def post(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                post_data = request.get_json()

                try:
                    sticky_note = StickyNote.query.filter_by(id=post_data.get("id")).first()

                    if sticky_note:
                        sticky_note.note_content = post_data.get("note_content")
                        sticky_note.updated_on = datetime.datetime.now()

                        db.session.commit()

                        response_object = {
                            "status": "success",
                            "message": "Successfully updated."
                        }
                        return make_response(jsonify(response_object)), 200
                    else:
                        response_object = {
                            "status": "fail",
                            "message": "Provide valid id."
                        }
                        return make_response(jsonify(response_object)), 404
                except Exception as e:
                    response_object = {
                        "status": "fail",
                        "message": "Some error occurred. Please try again."
                    }
                    return make_response(jsonify(response_object)), 400
            else:
                response_object = {
                    "status": "fail",
                    "message": resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid token."
            }
            return make_response(jsonify(response_object)), 403


class GetAPI(MethodView):
    def get(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    sticky_notes = StickyNote.query.filter_by(user_id=request.args.get("user_id")).order_by(StickyNote.id).all()

                    if sticky_notes:
                        sticky_notes_str = "["

                        for note in sticky_notes:
                            sticky_notes_str += '{"id": ' + str(note.id) + ', "user_id": ' + str(note.user_id) \
                                                + ', "note_content": "' + note.note_content + '"}, '
                        sticky_notes_str = sticky_notes_str[:-2] + "]"

                        response_object = {
                            "status": "success",
                            "message": "Successfully got sticky notes.",
                            "sticky_notes": sticky_notes_str
                        }
                        return make_response(jsonify(response_object)), 200
                    else:
                        response_object = {
                            "status": "fail",
                            "message": "Provide a valid user id."
                        }
                        return make_response(jsonify(response_object)), 404
                except Exception as e:
                    print(e)
                    response_object = {
                        "status": "fail",
                        "message": "Some error occurred. Please try again."
                    }
                    return make_response(jsonify(response_object)), 400
            else:
                response_object = {
                    "status": "fail",
                    "message": resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid token."
            }
            return make_response(jsonify(response_object)), 403


# define the API resources
add_view = AddAPI.as_view("add_api")
delete_view = DeleteAPI.as_view("delete_api")
update_view = UpdateAPI.as_view("update_api")
get_view = GetAPI.as_view("get_api")

# add rules for API endpoints
stickynotes_blueprint.add_url_rule(
    "/stickynote/add",
    view_func=add_view,
    methods=["POST"]
)
stickynotes_blueprint.add_url_rule(
    "/stickynote/delete",
    view_func=delete_view,
    methods=["POST"]
)
stickynotes_blueprint.add_url_rule(
    "/stickynote/update",
    view_func=update_view,
    methods=["POST"]
)
stickynotes_blueprint.add_url_rule(
    "/stickynote/get",
    view_func=get_view,
    methods=["GET"]
)

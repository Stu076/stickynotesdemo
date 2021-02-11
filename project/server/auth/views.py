from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User, BlacklistToken

auth_blueprint = Blueprint("auth", __name__)


class RegisterAPI(MethodView):
	def post(self):
		post_data = request.get_json()

		user = User.query.filter_by(email=post_data.get("email")).first()
		if not user:
			try:
				user = User(email=post_data.get("email"), password=post_data.get("password"))

				db.session.add(user)
				db.session.commit()

				auth_token = user.encode_auth_token(user.id)
				response_object = {
					"status": "success",
					"message": "Successfully registered.",
					"auth_token": auth_token,
					"user_id": user.id
				}
				return make_response(jsonify(response_object)), 201
			except Exception as e:
				print(e)
				response_object = {
					"status": "fail",
					"message": "Some error occured. Please try again."
				}
				return make_response(jsonify(response_object)), 401
		else:
			response_object = {
				"status": "fail",
				"message": "User already exists. Please log in."
			}
			return make_response(jsonify(response_object)), 202


class LoginAPI(MethodView):
	def post(self):
		post_data = request.get_json()
		try:
			print(post_data.get("email"))
			user = User.query.filter_by(
				email=post_data.get("email")
			).first()
			if user and bcrypt.check_password_hash(
				user.password, post_data.get("password")
			):
				auth_token = user.encode_auth_token(user.id)
				if auth_token:
					response_object = {
						"status": "success",
						"message": "Successfully logged in.",
						"auth_token": auth_token,
						"user_id": user.id
					}
					return make_response(jsonify(response_object)), 200
			else:
				response_object = {
					"status": "fail",
					"message": "User does not exist."
				}
				return make_response(jsonify(response_object)), 404
		except Exception as e:
			print(e)
			response_object = {
				"status": "fail",
				"message": "Try again"
			}
			return make_response(jsonify(response_object)), 500


class UserAPI(MethodView):
	def get(self):
		auth_header = request.headers.get("Authorization")
		if auth_header:
			try:
				auth_token = auth_header.split(" ")[1]
			except IndexError as e:
				print(e)
				response_object = {
					"status": "fail",
					"message": "Bearer token malformed."
				}
				return make_response(jsonify(response_object)), 401
		else:
			auth_token = ""
		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				user = User.query.filter_by(id=resp).first()
				response_object = {
					"status": "success",
					"data": {
						"user_id": user.id,
						"email": user.email,
						"admin": user.admin,
						"registered_on": user.registered_on
					}
				}
				return make_response(jsonify(response_object)), 200
			response_object = {
				"status": "fail",
				"message": resp
			}
			return make_response(jsonify(response_object)), 401
		else:
			print("Provide valid token")
			response_object = {
				"status": "fail",
				"message": "Provide a valid auth token."
			}
			return make_response(jsonify(response_object)), 401


class LogoutAPI(MethodView):
	def post(self):
		auth_header = request.headers.get("Authorization")
		if auth_header:
			auth_token = auth_header.split(" ")[1]
		else:
			auth_token = ""

		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				blacklist_token = BlacklistToken(token=auth_token)
				try:
					db.session.add(blacklist_token)
					db.session.commit()
					response_object = {
						"status": "success",
						"message": "Successfully logged out."
					}
					return make_response(jsonify(response_object)), 200
				except Exception as e:
					response_object = {
						"status": "fail",
						"message": e
					}
					return make_response(jsonify(response_object)), 200
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
registration_view = RegisterAPI.as_view("register_api")
login_view = LoginAPI.as_view("login_api")
user_view = UserAPI.as_view("user_api")
logout_view = LogoutAPI.as_view("logout_api")

# add rules for API endpoints
auth_blueprint.add_url_rule(
	"/auth/register",
	view_func=registration_view,
	methods=["POST"]
)
auth_blueprint.add_url_rule(
	"/auth/login",
	view_func=login_view,
	methods=["POST"]
)
auth_blueprint.add_url_rule(
	"/auth/status",
	view_func=user_view,
	methods=["GET"]
)
auth_blueprint.add_url_rule(
	"/auth/logout",
	view_func=logout_view,
	methods=["POST"]
)

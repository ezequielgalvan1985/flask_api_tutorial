from flask import request, Blueprint
from flask_restful import Api, Resource

from schemas import UserSchema
from models import User
from db import db
user_serializer = UserSchema()
users_blueprint = Blueprint('users_blueprint', __name__)
api = Api(users_blueprint)


class UserListResource(Resource):
    def get(self):
        print('flag1')
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        result = user_serializer.dump(users, many=True)
        print('flag2')
        return result

    def post(self):
        data = request.get_json()
        record_dict = user_serializer.load(data)
        user = User(username=record_dict['username'],
                    email=record_dict['email'],

                    )
        user.save()
        resp = user_serializer.dump(user)
        return resp, 201


class UserResource(Resource):
    def get(self, id):
        r = User.get_by_id(id)
        if r is None:
            return {"mensaje": "usuario no existe"}, 404
        resp = user_serializer.dump(r)
        return resp

    def delete(self, id):
        r = User.get_by_id(id)
        if r is None:
            return {"mensaje": "usuario no existe"}, 500
        users = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = User.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = user_serializer.load(data)
        r.username = record_dict['username']
        r.email = record_dict['email']
        r.save()
        resp = user_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(UserListResource, '/api/v1.0/users',endpoint='users_list_resource')
api.add_resource(UserResource, '/api/v1.0/users/<int:id>', endpoint='user_resource')

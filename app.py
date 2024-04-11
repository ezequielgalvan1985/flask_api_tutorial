from datetime import timedelta
from flask import Flask, request, jsonify
from flask_restful import Api, abort
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from models import User, Permiso, RolPermiso, Categoria, Empresa
from resources_empresas import empresas_blueprint, empresa_serializer
from resources_marcas import marcas_blueprint
from resources_permisos import permisos_blueprint
from resources_roles import roles_blueprint
from resources_rolpermisos import rolpermisos_serializer, rolpermisos_blueprint
from resources_rubros import rubros_blueprint
from resources_users import users_blueprint, user_serializer
from resources_categorias import categorias_blueprint, categoria_serializer
from resources_productos import productos_blueprint
from db import db
from schemas import UserSchemaDto, PermisoSchema, RolPermisoSchema
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, current_user, \
    get_jwt
from flask_jwt_extended import jwt_required
from flask_cors import CORS, cross_origin



#variables globales
SECRET_KEY = '123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'
PROPAGATE_EXCEPTIONS = True
# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
ERROR_404_HELP = False

#configuracion
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8100", "http://127.0.0.1:8100"]}})

#app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = PROPAGATE_EXCEPTIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SHOW_SQLALCHEMY_LOG_MESSAGES'] = SHOW_SQLALCHEMY_LOG_MESSAGES
app.config['ERROR_404_HELP'] = ERROR_404_HELP
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

jwt = JWTManager(app)

#urls de pruebas
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@app.route('/user-profile')
@jwt_required()
def user_profile():
    current_user_id = get_jwt_identity()
    return f'Profile of user {current_user_id}'


@app.errorhandler(401)
def custom_401(error):
    return jsonify({"message": "Token has expired"}), 401

@app.route('/api/v1.0/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    claims = get_jwt()
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, claims=claims), 200


@app.route('/api/v1.0/auth/login', methods=['POST'])
@cross_origin("http://localhost:8100")
def login():
    data = request.get_json()
    record_dict = user_serializer.load(data)
    user = User.query.filter_by(username=record_dict['username']).first()
    if user is None:
        abort(404, description="No se encontro usuario")
    if not check_password_hash(user.password, record_dict['password']):
        abort(400, "Usuario o contraseña Invalido")
    #setear los permisos
    permisos = RolPermiso.query.filter_by(rol_id=user.rol_id).all()

    rolPermiso_serializer = RolPermisoSchema()
    permisosJson = rolPermiso_serializer.dump(permisos,many=True)

    additional_claims = {"permisos": permisosJson}
    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    return {"access_token":access_token,"login":user.username, "user_id":user.id},200



@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
    )


#metodos personalizados
#Consultas Categorias
@app.route("/api/v1.0/categorias/consultas/findbyrubro/<int:rubro_id>", methods=["GET"])
@jwt_required()
def categoriasFindByRubro(rubro_id):
    c=Categoria.query.filter_by(rubro_id=rubro_id).all()
    if c is None:
        return abort(500, "No existen Categorias para el Rubro "+ rubro_id)
    resp = categoria_serializer.dump(c,many=True)
    return resp,200



@app.route("/api/v1.0/empresas/consultas/findbyuser/<int:user_id>", methods=["GET"])
@jwt_required()
def empresasFindByUserId(user_id):
    r=Empresa.query.filter_by(user_id=user_id).first()
    #empresa_serializer.dump(r)
    if r is None:
        return abort(500, "No existe Empresa para el Usuario "+ user_id)
    resp = empresa_serializer.dump(r, many=False)
    return resp, 200



ma = Marshmallow()
migrate = Migrate()

db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

user_dto_serializer = UserSchemaDto()


# Captura todos los errores 404
Api(app, catch_all_404s=True)

# Deshabilita el modo estricto de acabado de una URL con /
app.url_map.strict_slashes = False

# Registra los blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(categorias_blueprint)
app.register_blueprint(productos_blueprint)
app.register_blueprint(roles_blueprint)
app.register_blueprint(permisos_blueprint)
app.register_blueprint(rolpermisos_blueprint)
app.register_blueprint(rubros_blueprint)
app.register_blueprint(marcas_blueprint)
app.register_blueprint(empresas_blueprint)





#urls para hacer pruebas


if __name__ == '__main__':
    app.run(debug=True)
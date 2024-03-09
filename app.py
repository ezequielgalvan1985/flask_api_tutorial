from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from resources_users import users_blueprint
from resources_categorias import categorias_blueprint
from resources_productos import productos_blueprint
from db import db


SECRET_KEY = '123447a47f563e90fe2db0f56b1b17be62378e31b7cfd3adc776c59ca4c75e2fc512c15f69bb38307d11d5d17a41a7936789'
PROPAGATE_EXCEPTIONS = True
# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False
ERROR_404_HELP = False


#app = create_app(settings_module)

app = Flask(__name__)
#app.config.from_object(settings_module)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = PROPAGATE_EXCEPTIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SHOW_SQLALCHEMY_LOG_MESSAGES'] = SHOW_SQLALCHEMY_LOG_MESSAGES
app.config['ERROR_404_HELP'] = ERROR_404_HELP




# configure the SQLite database, relative to the app instance folder
# Inicializa las extensiones

ma = Marshmallow()
migrate = Migrate()

db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

# Captura todos los errores 404
Api(app, catch_all_404s=True)

# Deshabilita el modo estricto de acabado de una URL con /
app.url_map.strict_slashes = False

# Registra los blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(categorias_blueprint)
app.register_blueprint(productos_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
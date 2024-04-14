from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import CategoriaSchema, RolPermisoSchema
from models import Categoria, Permiso
from db import db
from flask_jwt_extended import get_jwt_identity
import json

categoria_serializer = CategoriaSchema()
categorias_findbyrubro_blueprint = Blueprint('categorias_findbyrubro_bp', __name__)

@categorias_findbyrubro_blueprint.route("/api/v1.0/categorias/consultas/findbyrubro/<int:rubro_id>", methods=["GET"])
@jwt_required()
def categoriasFindByRubro(rubro_id):
    c=Categoria.query.filter_by(rubro_id=rubro_id).all()
    if c is None:
        return abort(500, "No existen Categorias para el Rubro "+ rubro_id)
    resp = categoria_serializer.dump(c,many=True)
    return resp,200


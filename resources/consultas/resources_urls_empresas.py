from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import CategoriaSchema, RolPermisoSchema, EmpresaSchema
from models import Categoria, Permiso, Empresa
from db import db
from flask_jwt_extended import get_jwt_identity
import json

empresa_serializer = EmpresaSchema()
empresas_findbyrubro_blueprint = Blueprint('empresas_findbyrubro_bp', __name__)

@empresas_findbyrubro_blueprint.route("/api/v1.0/empresas/consultas/findbyuser/<int:user_id>", methods=["GET"])
@jwt_required()
def empresasFindByUserId(user_id):
    r=Empresa.query.filter_by(user_id=user_id).first()
    #empresa_serializer.dump(r)
    if r is None:
        return abort(500, "No existe Empresa para el Usuario "+ user_id)
    resp = empresa_serializer.dump(r, many=False)
    return resp, 200



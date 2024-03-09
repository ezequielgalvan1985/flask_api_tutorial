import werkzeug
from flask import jsonify
from flask import json
from werkzeug.exceptions import HTTPException
from flask import abort, jsonify
from app import app


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

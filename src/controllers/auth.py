from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models.models import Usuario
from src.app import db

app_blp = Blueprint("auth", __name__, url_prefix="/auths")


@app_blp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    usuario = db.session.execute(db.select(Usuario).where(Usuario.nome == username)).scalar()
    if not usuario or usuario.senha != password:
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=usuario.id)
    return {"access_token": access_token}
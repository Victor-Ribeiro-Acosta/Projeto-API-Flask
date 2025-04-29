from flask import Blueprint, request
from src.app import db
from models.models import Role

app_blp = Blueprint("role", __name__, url_prefix="/roles")

@app_blp.route('/', methods = ['POST'])
def create_role():
    data = request.json
    role = Role(nome = data['nome'])
    db.session.add(role)
    db.session.commit()
    return {"message": "Cadastro realizado com sucesso"}

from http import HTTPStatus

from flask import Blueprint, request
from models.models import Usuario
from sqlalchemy.inspection import inspect
from src.app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import required_roles

app_blp = Blueprint("usuario", __name__, url_prefix="/usuarios")
# Blueprint é um método alternativo para criar rotas em urls
# usuario - identificação
# __name__ - diferenciação
# url_prefix - prefixo da url 9 o padrão RestFUL deve sempre estar no plural

# Criar função para criar usuario
def _criar_usuario():
  data = request.json
  usuario = Usuario(
    nome = data['nome'],
    senha = data['senha'],
    role_id = data['role_id']
    )
  db.session.add(usuario)
  db.session.commit()


# Função para retornar todos os usuarios cadastrados
def _listar_usuarios():
  resultado = db.session.execute(db.select(Usuario)).scalar()
  # corrigindo o erro ao apresentar os usuarios
  return [
    {'id_Admin': get_jwt_identity(), 'id': usuario.id, 'nome': usuario.id, 'Status': usuario.role.id} for usuario in resultado
         ]


# Criar as rotas
# Criar usuarios
@app_blp.route("/", methods = ["GET", "POST"])
@jwt_required()
@required_roles('admin')
def create_usuario():
  usuario_id = get_jwt_identity()
  usuario = db.get_or_404(Usuario, usuario_id)
  if usuario.role.nome != 'admin':
    return {"msg": "Bad username or password"}, 401
  
  if request.method == 'POST':
    _criar_usuario()
    return {"message":"Usuario registrado com sucesso"}, HTTPStatus.CREATED
    # 201 - significa criação de recursos
    # HTTPStatus.CREATED - retorna o status de recurso criado com sucesso.
  if request.method == 'GET':
    return {"usuarios":_listar_usuarios()} # retorna a lista de todos os usuarios cadastrados

#Buscar usuario
@app_blp.route("/<int:usuario_id>")
def buscar_usuario(usuario_id):
  usuario = db.get_or_404(Usuario, usuario_id)
  return {'id': usuario.id, 'username': usuario.nome}

# Atualizar usuario
@jwt_required()
@required_roles('admin')
@app_blp.route('/<int:usuario_id>', methods = ['PATCH'])
def atualizar_usuario(usuario_id):
  usuario = db.get_or_404(Usuario, usuario_id)
  data = request.json

  map = inspect(usuario)
  for column in map.attrs:
    if column.key in data:
      setattr(usuario, column.key, data[column.key])
  db.session.commit()

  return {'Idnetity': get_jwt_identity(),'id': usuario.id, 'username': usuario.nome}


# Deletar usuario
@jwt_required()
@required_roles('admin')
@app_blp.route('/<int:usuario_id>', methods = ['DELETE'])
def remover_usuario(usuario_id):
  usuario = db.get_or_404(Usuario, usuario_id)
  db.session.delete(usuario)
  db.session.commit()

  return {"message": "usuario removido com sucesso"}
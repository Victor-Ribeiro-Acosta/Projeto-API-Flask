from src.app import db
from models.models import Usuario
from flask import request
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def required_roles(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            usuario_id = get_jwt_identity()
            usuario = db.get_or_404(Usuario, usuario_id)
            if usuario.role.nome != role_name:
                return {"msg": "Bad username or password"}, 401
            
            return f(*args, **kwargs)
        
        return wrapped
    
    return decorator
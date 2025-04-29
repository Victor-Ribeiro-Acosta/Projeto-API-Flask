# Instalar Flask-SQLAlchemy

import click
from flask import Flask, current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass



db = SQLAlchemy(model_class=Base)
# Criar instancia da migração
migrate = Migrate()
jwt = JWTManager()




# Registrando comando init-db no terminal
# -> comando no terminal: flask --app app init-db
@click.command('init-db')
# função a ser executada quando o comando for passado no terminal
def init_db_command():
    """Clear the existing data and create new tables."""
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')



def create_app(test_config=None):
  # criar e configurar app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
      SECRET_KEY='dev',  # criar chave secreta
      SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db', # criar banco de dados
      JWT_SECRET_KEY = 'super-secret'
  )
#   -> app.instance_path cria um caminho até um diretorio

    if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile('config.py', silent=True)
    else:
      # load the test config if passed in
      app.config.from_mapping(test_config)

    # Criar aplicação
    db.init_app(app)
  
    # Iniciando a migração
    migrate.init_app(app, db)

    # Iniciar autenticação
    jwt.init_app(app)

    app.cli.add_command(init_db_command) # registrar comando


  # registrar blueprint dos models
    from controllers import usuario
    from controllers import auth
    from controllers import role
    app.register_blueprint(usuario.app_blp)
    app.register_blueprint(auth.app_blp)
    app.register_blueprint(role.app_blp)
    return app
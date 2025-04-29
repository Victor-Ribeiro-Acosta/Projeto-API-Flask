from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.app import db

class Role(db.Model):
   id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
   nome: Mapped[str] = mapped_column(db.String(100))
   usuario: Mapped[("Usuario")] = relationship(back_populates = "role")

class Usuario(db.Model):
  id = mapped_column(db.Integer, primary_key=True, autoincrement=True)
  nome = mapped_column(db.String(100))
  senha: Mapped[str] = mapped_column(db.String(100))
  role_id: Mapped[int] = mapped_column(db.ForeignKey("role.id"))
  role: Mapped["Role"] = relationship(back_populates = "usuario")
  info: Mapped["Info"] = relationship(back_populates = "usuario")

class Info(db.Model):
  id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
  usuario_id: Mapped[int] = mapped_column(db.ForeignKey('usuario.id'))
  email: Mapped[str] = mapped_column(db.String(100))
  usuario: Mapped["Usuario"] = relationship(back_populates = 'info')
  
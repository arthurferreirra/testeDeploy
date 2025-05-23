import os

from flask import Flask, g , current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

import sqlalchemy as sa
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from markupsafe import escape
from jinja2 import escape

import click


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str]=mapped_column(sa,String, nullable=False)
    user:Mapped[list["User"]] = relationship(back_populates="role")
    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r}"

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String,unique=True, nullable=False)
    role_id:Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r},  active={self.active!r}"

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] =  mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
    

@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) #instace é usado para verificar arquivo de configuração na pasta raiz
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY="super-secret",

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

   

    ##from . import db
    app.cli.add_command(init_db_command) #registrando click comando
    db.init_app(app) #inicializando extensão

    migrate = Migrate(app, db)
    migrate.init_app(app)
    jwt.init_app(app)

    ##register blueprints
    from src.controllers import user
    from src.controllers import auth
    from src.controllers import role

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    return app
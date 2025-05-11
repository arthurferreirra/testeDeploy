from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from src.utils import requires_role

app = Blueprint('user', __name__, url_prefix='/users')

def _creat_user():
    data = request.json
    user = User(username = data["username"],password=data["password"], role_id=data["role-id"])
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username" : user.username,
            "role":{"id": user.role.id, "name": user.role.name,},
        }
        for user in users
    ]

@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("normal")
def hadle_user(): ##mesmo que list or create user
    if (request.method == 'POST'):
        _creat_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users":_list_users()}
    
@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return{
        "id": user.id,
        "username" : user.username,
    }


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json # request json retorna um dicionario
        #metodo simples de update
    #if "username" in data:
       # user.username = data["username"] # dessa forma o user ira receber o username que está no dicionario data
       # db.session.commit()

       #metodo de update dinamico
    from sqlalchemy import inspect

    mapper = inspect(User)
    for column in mapper.attrs:
        if(column.key in data):
            setattr(user,column.key, data[column.key])
    db.session.commit()

    return{
        "id": user.id,
        "username" : user.username,
    }

@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id) # RECUPERAR USUARIO
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT

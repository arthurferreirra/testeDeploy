from http import HTTPStatus
from src.app import User, Role ,db
from sqlalchemy import func

def test_get_user_success(client):
    #given
    role = Role(name= 'admin')
    db.session.add(role)
    db.session.commit()

    user = User(username = "arthur", password="test", role_id=role.id)

    db.session.add(user)
    db.session.commit()
#when
    response = client.get(f"/users/{user.id}")
#then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username" : user.username,}
    
#função de error
def test_get_user_not_found(client):

    #given
    role = Role(name= 'admin')
    db.session.add(role)
    db.session.commit()
    user_id = 1
#when
    response = client.get(f"/users/{user_id}")
#then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_user(client, acess_token):
    user = db.session.execute(db.select(User).where(User.username == "arthur")).scalar()
    payload = {"username": "testUser2", "password": "teste", "role_id":role_id}
    
    response = client.post(f"/users/", json=payload,headers= {'Authorization': f"Bearer{access_token}"})

    assert response.status.code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_list_users(client):
    #given
    role = Role(name= 'admin')
    db.session.add(role)
    db.session.commit()

    user = User(username = "arthur", password="test", role_id=role.id)

    db.session.add(user)
    db.session.commit()

    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    access_token = response.json["access_token"]
#when
    response = client.get(f"/users/", headers= {'Authorization': f'{access_token}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users":[
            {
                "id": user.id,
                "username" : user.username,
                "role":{
                    "id": user.role.id,
                    "name": user.role.name,
                    },
            }

        ]
        
    }

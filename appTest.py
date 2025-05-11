from flask import Flask , request , url_for, jsonify

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return {"message": "ola mundo, dict"}

@app.route("/testeVar/<usuario>/<int:idade>/<float:altura>")
def testeVar(usuario, idade, altura):
    return {
        "Usuario": usuario,
        "Idade": idade,
        "Altura": altura,
    }

@app.route("/about", methods=["GET","POST"])
def about():
    if request.method == 'GET':
        return 'This is a get'
    else:
        return 'This is a post'


with app.test_request_context():
    url = "/about"
    print(url_for("hello_world"))
    print(url_for("about", next="/"))
    print(url_for('testeVar', usuario="arthur", idade=22, altura=169))



from flask import request, jsonify
from functools import wraps


#usuario de exemplo
USUARIOS = {
    "admin": "password123"
}


def autenticar(username, password):
    return USUARIOS.get(username) == password


def autenticar_requisicao():
    auth = request.authorization
    if not auth or not autenticar(auth.username, auth.password):
        return jsonify({"message": "Autenticação falhou."}), 401


def requer_autenticacao(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        resultado = autenticar_requisicao()
        if resultado:
            return resultado
        return f(*args, **kwargs)
    return decorated
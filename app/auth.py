from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

auth_bp = Blueprint('auth', __name__)
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def gerar_token(usuario_id):
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def verificar_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def autenticar_requisicao():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token não fornecido.'}), 401

    #token = token.split(" ")[1] # Remover o prefixo 'Bearer' do token

    try:
        decoded_token = verificar_token(token)
        if not decoded_token:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 401
    except IndexError:
        return jsonify({'message': 'Token mal formado!'}), 401

    return decoded_token


def requer_autenticacao(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        resultado = autenticar_requisicao()
        if isinstance(resultado, tuple): # autenticação falhou
            return resultado
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if Usuario.query.filter_by(nome_usuario=data['nome_usuario']).first():
        return jsonify({'message': 'Usuário já existe.'}), 400

    hashed_password = generate_password_hash(data['senha'], method='pbkdf2:sha256')
    novo_usuario = Usuario(nome_usuario=data['nome_usuario'], senha=hashed_password, email=data['email'])

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(nome_usuario=data['nome_usuario']).first()

    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        return jsonify({'message': 'Usuário ou senha inválidos!'}), 401

    token = gerar_token(usuario.id)
    return jsonify({'token': token}), 200





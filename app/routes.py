from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario, Produto, Pedido, ItemPedido
from app.schemas import UsuarioSchema, ProdutoSchema, PedidoSchema, ItemPedidoSchema

bp = Blueprint('main', __name__)

usuario_schema = UsuarioSchema()
produto_schema = ProdutoSchema()
pedido_schema = PedidoSchema()
item_pedido_schema = ItemPedidoSchema()


@bp.route('/')
def home():
    return "Bem-vindo à Disponatus Store"


@bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    errors = usuario_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    usuario = usuario_schema.load(data, session=db.session)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'id': usuario.id}), 201


@bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuario_schema.dump(usuarios, many=True))


@bp.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    errors = produto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    produto = produto_schema.load(data, session=db.session)
    db.session.add(produto)
    db.session.commit()
    return jsonify({'id': produto.id}), 201


@bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify(produto_schema.dump(produtos, many=True))


@bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    data = request.get_json()
    errors = pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    pedido = pedido_schema.load(data, session=db.session)
    db.session.add(pedido)
    db.session.commit()
    return jsonify({'id': pedido.id}), 201


@bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify(pedido_schema.dump(pedidos, many=True))


@bp.route('/itens_pedido', methods=['POST'])
def criar_item_pedido():
    data = request.get_json()
    errors = item_pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    item = item_pedido_schema.load(data, session=db.session)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201


@bp.route('/itens_pedido', methods=['GET'])
def listar_itens_pedido():
    itens = ItemPedido.query.all()
    return jsonify(item_pedido_schema.dump(itens, many=True))

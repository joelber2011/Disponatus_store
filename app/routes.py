from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from app.models import Usuario, Produto, Pedido, ItemPedido
from app.schemas import UsuarioSchema, ProdutoSchema, PedidoSchema, ItemPedidoSchema
from app.auth import requer_autenticacao, gerar_token

bp = Blueprint('main', __name__)

usuario_schema = UsuarioSchema()
produto_schema = ProdutoSchema()
pedido_schema = PedidoSchema()
item_pedido_schema = ItemPedidoSchema()


@bp.route('/')
def home():
    return "Bem-vindo à Disponatus Store"


#----------------------------- ROTAS PARA USUARIO -------------------------------------------------------

# @bp.route('/usuarios', methods=['POST'])
# @requer_autenticacao
# def criar_usuario():
#     data = request.get_json()
#
#     try:
#         usuario = usuario_schema.load(data, session=db.session)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#
#     db.session.add(usuario)
#     db.session.commit()
#     return jsonify({'Usuário criado com sucesso. id': usuario.id}), 201


@bp.route('/usuarios', methods=['GET'])
@requer_autenticacao
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuario_schema.dump(usuarios, many=True))


@bp.route('/usuarios/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado.'}), 404

    try:
        usuario_atualizado = usuario_schema.load(data, instance=usuario, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify(usuario_schema.dump(usuario_atualizado))


@bp.route('/usuarios/<int:id>', methods=['DELETE'])
@requer_autenticacao
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado.'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso.'})


#----------------------------- ROTAS PARA PRODUTO -------------------------------------------------------

@bp.route('/produtos', methods=['POST'])
@requer_autenticacao
def criar_produto():
    data = request.get_json()

    try:
        produto = produto_schema.load(data, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(produto)
    db.session.commit()
    return jsonify({'Produto inserido com sucesso. id': produto.id}), 201


@bp.route('/produtos', methods=['GET'])
@requer_autenticacao
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify(produto_schema.dump(produtos, many=True))


@bp.route('/produtos/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_produto(id):
    data = request.get_json()
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    try:
        produto_atualizado = produto_schema.load(data, instance=produto, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify(produto_schema.dump(produto_atualizado))


@bp.route('/produtos/<int:id>', methods=['DELETE'])
@requer_autenticacao
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado com sucesso'})


#----------------------------- ROTAS PARA PEDIDO -------------------------------------------------------

@bp.route('/pedidos', methods=['POST'])
@requer_autenticacao
def criar_pedido():
    data = request.get_json()

    try:
        pedido = pedido_schema.load(data, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(pedido)
    db.session.commit()
    return jsonify({'Pedido criado com sucesso. id': pedido.id}), 201


@bp.route('/pedidos', methods=['GET'])
@requer_autenticacao
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify(pedido_schema.dump(pedidos, many=True))


@bp.route('/pedidos/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_pedido(id):
    data = request.get_json()
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    try:
        pedido_atualizado = pedido_schema.load(data, instance=pedido, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify(pedido_schema.dump(pedido_atualizado))


@bp.route('/pedidos/<int:id>', methods=['DELETE'])
@requer_autenticacao
def deletar_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': 'Pedido deletado com sucesso'})


#----------------------------- ROTAS PARA ITEM PEDIDO -------------------------------------------------------

@bp.route('/itens_pedido', methods=['POST'])
@requer_autenticacao
def criar_item_pedido():
    data = request.get_json()

    try:
        item_pedido = item_pedido_schema.load(data, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(item_pedido)
    db.session.commit()
    return jsonify({'Item inserido com sucesso. id': item_pedido.id}), 201


@bp.route('/itens_pedido', methods=['GET'])
@requer_autenticacao
def listar_itens_pedido():
    itens = ItemPedido.query.all()
    return jsonify(item_pedido_schema.dump(itens, many=True))


@bp.route('/itens_pedido/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_item_pedido(id):
    data = request.get_json()
    item_pedido = ItemPedido.query.get(id)
    if not item_pedido:
        return jsonify({'error': 'Item não encontrado no pedido'}), 404

    try:
        item_pedido_atualizado = item_pedido_schema.load(data, instance=item_pedido, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify(item_pedido_schema.dump(item_pedido_atualizado))


@bp.route('/itens_pedido/<int:id>', methods=['DELETE'])
@requer_autenticacao
def deletar_item_pedido(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'ItemPedido deletado com sucesso'})

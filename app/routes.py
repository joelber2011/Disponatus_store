from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario, Produto, Pedido, ItemPedido
from app.schemas import UsuarioSchema, ProdutoSchema, PedidoSchema, ItemPedidoSchema
from app.auth import requer_autenticacao

bp = Blueprint('main', __name__)

usuario_schema = UsuarioSchema()
produto_schema = ProdutoSchema()
pedido_schema = PedidoSchema()
item_pedido_schema = ItemPedidoSchema()


@bp.route('/')
def home():
    return "Bem-vindo à Disponatus Store"


#----------------------------- ROTAS PARA USUARIO -------------------------------------------------------

@bp.route('/usuarios', methods=['POST'])
@requer_autenticacao
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
@requer_autenticacao
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify(usuario_schema.dump(usuarios, many=True))


@bp.route('/usuarios/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_usuario(id):
    data = request.get_json()
    errors = usuario_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado.'}), 404

    usuario.nome_usuario = data.get('nome_usuario', usuario.nome_usuario)
    usuario.email = data.get('email', usuario.email)
    usuario.senha = data.get('senha', usuario.senha)
    db.session.commit()
    return jsonify(usuario_schema.dump(usuario))


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
    errors = produto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    produto = produto_schema.load(data, session=db.session)
    db.session.add(produto)
    db.session.commit()
    return jsonify({'id': produto.id}), 201


@bp.route('/produtos', methods=['GET'])
@requer_autenticacao
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify(produto_schema.dump(produtos, many=True))


@bp.route('/produtos/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_produto():
    data = request.get_json()
    errors = produto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    produto.nome = data.get('nome', produto.nome)
    produto.descricao = data.get('descricao', produto.descricao)
    produto.preco = data.get('preco', produto.preco)
    produto.estoque = data.get('estoque', produto.estoque)
    db.session.commit()
    return jsonify(produto_schema.dump(produto))


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
    errors = pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    pedido = pedido_schema.load(data, session=db.session)
    db.session.add(pedido)
    db.session.commit()
    return jsonify({'id': pedido.id}), 201


@bp.route('/pedidos', methods=['GET'])
@requer_autenticacao
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify(pedido_schema.dump(pedidos, many=True))


@bp.route('/pedidos/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_pedido(id):
    data = request.get_json()
    errors = pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    pedido.id_usuario = data.get('id_usuario', pedido.id_usuario)
    pedido.valor_total = data.get('valor_total', pedido.valor_total)
    pedido.status = data.get('status', pedido.status)
    db.session.commit()
    return jsonify(pedido_schema.dump(pedido))


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
    errors = item_pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    item = item_pedido_schema.load(data, session=db.session)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201


@bp.route('/itens_pedido', methods=['GET'])
@requer_autenticacao
def listar_itens_pedido():
    itens = ItemPedido.query.all()
    return jsonify(item_pedido_schema.dump(itens, many=True))


@bp.route('/itens_pedido/<int:id>', methods=['PUT'])
@requer_autenticacao
def atualizar_item_pedido(id):
    data = request.get_json()
    errors = item_pedido_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({'error': 'ItemPedido não encontrado'}), 404

    item.id_pedido = data.get('id_pedido', item.id_pedido)
    item.id_produto = data.get('id_produto', item.id_produto)
    item.quantidade = data.get('quantidade', item.quantidade)
    item.preco = data.get('preco', item.preco)
    db.session.commit()
    return jsonify(item_pedido_schema.dump(item))


@bp.route('/itens_pedido/<int:id>', methods=['DELETE'])
@requer_autenticacao
def deletar_item_pedido(id):
    item = ItemPedido.query.get(id)
    if not item:
        return jsonify({'error': 'ItemPedido não encontrado'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'ItemPedido deletado com sucesso'})

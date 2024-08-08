from marshmallow import Schema, fields, validate, ValidationError
from app.models import Usuario, Produto, Pedido, ItemPedido
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

    nome_usuario = auto_field(required=True, validat=validate.Length(min=1))
    email = auto_field(required=True, validate=validate.Email())
    senha = auto_field(required=True, validate=validate.Length(min=6))


class ProdutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True

    nome = auto_field(required=True, validate=validate.Length(min=1))
    descricao = auto_field(required=True, validate=validate.Length(min=1))
    preco = auto_field(required=True, validate=validate.Range(min=0))
    estoque = auto_field(required=True, validate=validate.Range(min=0))


class PedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        load_instance = True

    id_usuario = auto_field(required=True)
    valor_total = auto_field(required=True, validate=validate.Range(min=0))
    status = auto_field(required=True, validate=validate.Length(min=1))


class ItemPedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemPedido
        load_instance = True

    id_pedido = auto_field(required=True)
    id_produto = auto_field(required=True)
    quantidade = auto_field(required=True, validate=validate.Range(min=1))
    preco = auto_field(required=True, validate=validate.Range(min=0))
from vemango import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))



class Cargo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_cargo = database.Column(database.String, nullable=False, unique=True)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


class Pessoa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_pessoa = database.Column(database.String, nullable=False, unique=True)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

class Funcionario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_funcionario = database.Column(database.String, nullable=False, unique=True)
    lider = database.Column(database.String, nullable=False, default='Não Possui')
    cargo = database.Column(database.String, nullable=False)
    id_funcionario = database.Column(database.String, nullable=False, unique=True)
    departamento = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome_usuario = database.Column(database.String, nullable=False, unique=True)
    login = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


class RegistroHoraExtra(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_colaborador = database.Column(database.Integer, nullable=False)
    nome_colaborador = database.Column(database.String, nullable=False)
    data_ponto = database.Column(database.String, nullable=False)
    entrada_escala = database.Column(database.Time, nullable=False)
    saida_escala = database.Column(database.Time, nullable=False)
    entrada_ponto = database.Column(database.Time, nullable=False)
    saida_ponto = database.Column(database.Time, nullable=False)
    qtde_horas = database.Column(database.Time, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

class SolicitarHE(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_solicitante = database.Column(database.Integer, nullable=False)
    solicitante = database.Column(database.String, nullable=False)
    lider = database.Column(database.String, nullable=False)
    data = database.Column(database.String, nullable=False)
    motivo = database.Column(database.Text, nullable=False)
    quantidade = database.Column(database.Time, nullable=False)
    status = database.Column(database.String, nullable=False, default='Aguardando Retorno')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


class BancoHE_ADM_Unificado(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_registro = database.Column(database.Integer, nullable=False)
    id_colaborador = database.Column(database.Integer, nullable=False)
    nome_colaborador = database.Column(database.String, nullable=False)
    #lider = database.Column(database.String, nullable=False)
    data_ponto = database.Column(database.String, nullable=False)
    entrada_escala = database.Column(database.Time, nullable=False)
    saida_escala = database.Column(database.Time, nullable=False)
    entrada_ponto = database.Column(database.Time, nullable=False)
    saida_ponto = database.Column(database.Time, nullable=False)
    total_he = database.Column(database.Time, nullable=False)
    #he_liberadas = database.Column(database.Time, nullable=False)
    #desvio = database.Column(database.String, nullable=False)
    #he_desviada = database.Column(database.Time, nullable=False)

class Solicitar_Orcamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    datasolicitacao = database.Column(database.String, nullable=False)
    solicitante = database.Column(database.String, nullable=False)
    tipo_aquisicao = database.Column(database.String, nullable=False)
    tipo_solicitacao = database.Column(database.String, nullable=False)
    motivo = database.Column(database.String, nullable=False)
    area = database.Column(database.String, nullable=False)
    planilha = database.Column(database.String, nullable=False, default='Nome do Arquivo')
    #motivo_cancelamento = database.Column(database.String, nullable=False, default='')
    #usuario_cancelamento = database.Column(database.String, nullable=False, default='')
    #datahora_cancelamento = database.Column(database.String, nullable=False, default='')
    datahora_envio_orcamento = database.Column(database.String, nullable=False, default='')
    usuario_envio_orcamento = database.Column(database.String, nullable=False, default='')
    status = database.Column(database.String, nullable=False, default='Aguardando Orçamento')


class Enviar_Orcamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    numero_solicitacao = database.Column(database.String, nullable=False)
    numero_orcamento = database.Column(database.String, nullable=False)
    data_orcamento = database.Column(database.String, nullable=False)
    fornecedor = database.Column(database.String, nullable=False)
    valor_orcamento = database.Column(database.Numeric(10,2), nullable=False)
    metodo_pagamento = database.Column(database.String, nullable=False)
    anexo_orcamento = database.Column(database.String, nullable=False, default='Nome do Arquivo')
    usuario_registro = database.Column(database.String, nullable=False)
    data_hora_registro = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False, default='Aguardando Aprovação - Departamento')
    usuario_reprovacao_departamento = database.Column(database.String, nullable=False, default='')
    data_hora_reprovacao_departamento = database.Column(database.String, nullable=False, default='')
    usuario_aprovacao_departamento = database.Column(database.String, nullable=False, default='')
    data_hora_aprovacao_departamento = database.Column(database.String, nullable=False, default='')
    #datahora_envio_orcamento = database.Column(database.String, nullable=False, default='')
    #usuario_envio_orcamento = database.Column(database.String, nullable=False, default='')


class Serviços_Produtos_Temporario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_solicitante = database.Column(database.String, nullable=False)
    servico_produto = database.Column(database.String, nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    classificacao = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)

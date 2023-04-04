from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SearchField, SelectField, FileField, DateField,\
    TimeField, TextAreaField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from vemango.models import Cargo, Pessoa, Funcionario, Usuario
from flask_wtf.file import FileField, FileRequired, FileAllowed

class CriarCargo(FlaskForm):
    nome_cargo = StringField('Nome do Cargo', validators=[DataRequired()])
    botao_submit_cargo = SubmitField('Criar Cargo')

    def validate_nome_cargo(self, nome_cargo):
        cargo = Cargo.query.filter_by(nome_cargo = nome_cargo.data).first()
        if cargo:
            raise ValidationError('Cargo já cadastrado.')


class EditarCargo(FlaskForm):
    nome_cargo = StringField('Nome do Cargo', validators=[DataRequired()])
    botao_submitedite_cargo = SubmitField('Editar Cargo')

    def validate_nome_cargo(self, nome_cargo):
        cargo = Cargo.query.filter_by(nome_cargo = nome_cargo.data).first()
        if cargo:
            raise ValidationError('Cargo já cadastrado.')

class ConsultarCargo(FlaskForm):
    pesquisar = SearchField('Pesquisar', validators=[DataRequired()])
    botao_pesquisar_cargo = SubmitField('Pesquisar')


class CadastrarPessoa(FlaskForm):
    nome_pessoa = StringField('Nome da Pessoa', validators=[DataRequired()])
    botao_submit_pessoa = SubmitField('Cadastrar Pessoa')

    def validate_nome_pessoa(self, nome_pessoa):
        pessoa = Pessoa.query.filter_by(nome_pessoa = nome_pessoa.data).first()
        if pessoa:
            raise ValidationError('Pessoa já cadastrada.')

class CriarFuncionario(FlaskForm):
    nome_funcionario = SelectField('Nome',choices=[],validators=[DataRequired()])
    lider = SelectField('Líder',choices=[])
    cargo = SelectField('Cargo',choices=[],validators=[DataRequired()])
    id_funcionario = StringField('ID', validators=[DataRequired()])
    botao_submit_funcionario = SubmitField('Cadastrar Funcionário')

    def validate_nome_funcionario(self, nome_funcionario):
        funcionario = Funcionario.query.filter_by(nome_funcionario = nome_funcionario.data).first()
        if funcionario:
            raise ValidationError('Funcionário já cadastrado.')

    def validate_id_funcionario(self, id_funcionario):
        id_funcionario = Funcionario.query.filter_by(id_funcionario = id_funcionario.data).first()
        if id_funcionario:
            raise ValidationError('ID já cadastrado.')


class EditarFuncionario(FlaskForm):
    nome_funcionario = SelectField('Nome')
    id_funcionario = StringField('ID', validators=[DataRequired()])
    botao_submit_funcionario = SubmitField('Cadastrar Funcionário')


    def validate_id_funcionario(self, id_funcionario):
        id_funcionario = Funcionario.query.filter_by(id_funcionario = id_funcionario.data).first()
        if id_funcionario:
            raise ValidationError('ID já cadastrado.')


class CriarUsuario(FlaskForm):
    nome_usuario = SelectField('Nome',choices=[],validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_usuario = SubmitField('Cadastrar Usuário')

    def validate_nome_usuario(self, nome_usuario):
        funcionario = Usuario.query.filter_by(nome_usuario = nome_usuario.data).first()
        if funcionario:
            raise ValidationError('Funcionário já cadastrado.')

    def validate_login(self, login):
        usuario = Usuario.query.filter_by(login = login.data).first()
        if usuario:
            raise ValidationError('Nome de Usuário já cadastrado.')


class ImportarHoraExtraAdm(FlaskForm):
    arquivo = FileField('Arquivo', validators=[FileRequired()])
    botao_submit_dados = SubmitField('Carregar Dados')
    botao_submit_enviar = SubmitField('Enviar Dados')


class Login(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Entrar')

class Solicitarhora(FlaskForm):
    datasolicitada = DateField('Data', validators=[DataRequired()])
    solicitante = StringField('Solicitante', validators=[DataRequired()])
    lider = StringField('Líder', validators=[DataRequired()])
    quantidade = TimeField('Quantidade de Horas Extras', validators=[DataRequired()])
    motivo = TextAreaField('Motivo da Solicitação', validators=[DataRequired()])
    botao_submit_solicitarHE = SubmitField('Solicitar')


class SolicitarOrcamento(FlaskForm):
    datasolicitacao = DateField('Data da Solicitação', validators=[DataRequired()])
    solicitante = StringField('Solicitante', validators=[DataRequired()])
    motivo = TextAreaField('Motivo da Solicitação', validators=[DataRequired()])
    tipo_aquisicao = SelectField('Tipo de Aquisição',choices=['Produto', 'Serviço', 'Produto e Serviço'],validators=[DataRequired()])
    tipo_solicitacao = SelectField('Tipo de Solicitação', choices=['Normal', 'Urgência'],validators=[DataRequired()])
    area = StringField('Departamento', validators=[DataRequired()])
    planilha = FileField('Planilha', validators=[FileRequired(), FileAllowed(['csv'], 'Somente arquivos CSV permitidos.')])
    servico_produto = StringField('Produto ou Serviço', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    classificacao = SelectField('Classificação',choices=['Produto', 'Serviço'],validators=[DataRequired()])
    botao_submit_solicitarOrcamento = SubmitField('Solicitar')


class RetornarOrcamento(FlaskForm):
    data_orcamento = DateField('Data do Orçamento', validators=[DataRequired()])
    fornecedor = StringField('Fornecedor', validators=[DataRequired()])
    numero_orcamento = StringField('Número do Orçamento', validators=[DataRequired()])
    valor_orcamento = DecimalField('Valor do Orçamento', places=2,validators=[DataRequired()])
    metodo_pagamento = SelectField('Método de Pagamento', choices=['Faturamento', 'Cartão'],validators=[DataRequired()])
    anexo_orcamento = FileField('Anexo', validators=[FileRequired()])
    botao_submit_anexarOrcamento = SubmitField('Anexar Orçamento')
    botao_submit_enviarOrcamento = SubmitField('Enviar Orçamento')
    botao_submit_outroOrcamento = SubmitField('Solicitar Outros Orçamentos')


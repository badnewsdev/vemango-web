import os.path
import struct

from datetime import date

import pandas as pd
from flask import render_template, redirect, url_for, flash, request
from vemango import app, database, bcrypt
from vemango.forms import CriarCargo, EditarCargo, CadastrarPessoa, CriarFuncionario, ImportarHoraExtraAdm, \
    CriarUsuario, Login, Solicitarhora, EditarFuncionario, SolicitarOrcamento, RetornarOrcamento
from vemango.models import Cargo, Pessoa, Funcionario, RegistroHoraExtra, Usuario, SolicitarHE, BancoHE_ADM_Unificado, \
    Solicitar_Orcamento,Enviar_Orcamento
from flask_login import login_user, logout_user, current_user
from datetime import datetime


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/sair')
def sair():
    logout_user()
    return redirect(url_for('login'))


@app.route('/recursoshumanos')
def recursoshumanos():
    return render_template('recursoshumanos.html')


@app.route('/planejamento_e_controle')
def planejamento_e_controle():
    return render_template('planejamento_e_controle.html')


@app.route('/administrador')
def administrador():
    return render_template('administrador.html')


@app.route('/cargos', methods=['GET', 'POST'])
def cargos():
    cadastro_cargo = CriarCargo()
    lista_cargos = Cargo.query.all()
    if cadastro_cargo.validate_on_submit() and 'botao_submit_cargo' in request.form:
        cargo = Cargo(nome_cargo=cadastro_cargo.nome_cargo.data)
        database.session.add(cargo)
        database.session.commit()
        flash(f'Cargo {cadastro_cargo.nome_cargo.data} cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('cargos'))
    return render_template('cargos.html', cadastro_cargo=cadastro_cargo, lista_cargos=lista_cargos)


@app.route('/cadastrobase')
def cadastrobase():
    return render_template('cadastrobase.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')


@app.route('/editarcargo/<cargo_id>', methods=['GET', 'POST'])
def editarcargo(cargo_id):
    cargo = Cargo.query.get(cargo_id)
    cadastro_cargo = EditarCargo()
    if request.method == 'GET':
        cadastro_cargo.nome_cargo.data = cargo.nome_cargo
    elif cadastro_cargo.validate_on_submit():
        cargo.nome_cargo = cadastro_cargo.nome_cargo.data
        database.session.commit()
        flash('Cargo Atualizado com Sucesso', 'alert-success')
    return render_template('editarcargo.html', cargo=cargo, cadastro_cargo=cadastro_cargo)


@app.route('/cargos/<cargo_id>/excluir', methods=['GET', 'POST'])
def excluircargo(cargo_id):
    cargo = Cargo.query.get(cargo_id)
    database.session.delete(cargo)
    database.session.commit()
    flash('Cargo Excluído com Sucesso', 'alert-danger')
    return redirect(url_for('cargos'))


@app.route('/pessoas', methods=['GET', 'POST'])
def cadastrarpessoas():
    cadastro_pessoa = CadastrarPessoa()
    lista_pessoas = Pessoa.query.all()
    if cadastro_pessoa.validate_on_submit() and 'botao_submit_pessoa' in request.form:
        pessoa = Pessoa(nome_pessoa=cadastro_pessoa.nome_pessoa.data)
        database.session.add(pessoa)
        database.session.commit()
        flash(f'{cadastro_pessoa.nome_pessoa.data} cadastrado(a) com sucesso.', 'alert-success')
        return redirect(url_for('cadastrarpessoas'))
    return render_template('pessoas.html', cadastro_pessoa=cadastro_pessoa, lista_pessoas=lista_pessoas)


@app.route('/editarpessoa/<pessoa_id>', methods=['GET', 'POST'])
def editarpessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    cadastro_pessoa = CadastrarPessoa()
    if request.method == 'GET':
        cadastro_pessoa.nome_pessoa.data = pessoa.nome_pessoa
    elif cadastro_pessoa.validate_on_submit():
        pessoa.nome_pessoa = cadastro_pessoa.nome_pessoa.data
        database.session.commit()
        flash('Pessoa Atualizada com Sucesso', 'alert-success')
    return render_template('editarpessoa.html', pessoa=pessoa, cadastro_pessoa=cadastro_pessoa)


@app.route('/pessoas/<pessoa_id>/excluir', methods=['GET', 'POST'])
def excluirpessoa(pessoa_id):
    pessoa = Pessoa.query.get(pessoa_id)
    database.session.delete(pessoa)
    database.session.commit()
    flash('Pessoa Excluída com Sucesso', 'alert-danger')
    return redirect(url_for('cadastrarpessoas'))


@app.route('/funcionarios', methods=['GET', 'POST'])
def cadastrarfuncionario():
    cadastro_funcionario = CriarFuncionario()
    lista_funcionarios = Funcionario.query.all()
    cadastro_funcionario.nome_funcionario.choices = [(pessoa.nome_pessoa) for pessoa in Pessoa.query.all()]
    cadastro_funcionario.lider.choices = [(pessoa.nome_pessoa) for pessoa in Pessoa.query.all()]
    cadastro_funcionario.cargo.choices = [(cargo.nome_cargo) for cargo in Cargo.query.all()]
    lista_cargos = Cargo.query.all()
    if cadastro_funcionario.validate_on_submit() and 'botao_submit_funcionario' in request.form:
        funcionario = Funcionario(nome_funcionario=cadastro_funcionario.nome_funcionario.data,
                                  id_funcionario=cadastro_funcionario.id_funcionario.data,
                                  lider=cadastro_funcionario.lider.data,
                                  cargo=cadastro_funcionario.cargo.data)
        database.session.add(funcionario)
        database.session.commit()
        flash(f'Funcionário {cadastro_funcionario.nome_funcionario.data} cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('cadastrarfuncionario'))
    return render_template('funcionarios.html', cadastro_funcionario=cadastro_funcionario,
                           lista_funcionarios=lista_funcionarios, lista_cargos=lista_cargos)


@app.route('/editarfuncionario/<funcionario_id>', methods=['GET', 'POST'])
def editarfuncionario(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    cadastro_funcionario = EditarFuncionario()
    cadastro_funcionario.nome_funcionario.choices = [funcionario.nome_funcionario]
    if request.method == 'GET':
        cadastro_funcionario.id_funcionario.data = funcionario.id_funcionario
        cadastro_funcionario.nome_funcionario.data = funcionario.nome_funcionario
    elif cadastro_funcionario.validate_on_submit():
        funcionario.id_funcionario = cadastro_funcionario.id_funcionario.data
        funcionario.nome_funcionario = cadastro_funcionario.nome_funcionario.data
        database.session.commit()
        flash('Funcionário Atualizado com Sucesso', 'alert-success')
    return render_template('editarfuncionario.html', funcionario=funcionario, cadastro_funcionario=cadastro_funcionario)


@app.route('/registrar_hora_extra', methods=['GET', 'POST'])
def registrar_hora_extra():
    registro = ImportarHoraExtraAdm()
    veman_df = 0
    nome_arquivo = []
    if registro.validate_on_submit() and 'botao_submit_dados' in request.form:
        nome_arquivo = registro.arquivo.data
        # filename = secure_filename(nome_arquivo.filename)
        # nome_arquivo.save(os.path.join(app.instance_path,'xlsx', filename))
        # print(filename)

        veman_df = pd.read_excel(nome_arquivo)
        veman_df['Data'] = veman_df['Data'].dt.strftime('%d/%m/%Y')

    if request.form.get('enviar'):
        print(1, 2, 3)
        nome_arquivo = registro.arquivo.data
        if nome_arquivo == None:
            pass
        else:
            veman_df = pd.read_excel(nome_arquivo)
            veman_df['Data'] = veman_df['Data'].dt.strftime('%d/%m/%Y')

            for i in veman_df.index:
                horas = RegistroHoraExtra(id_colaborador=int(veman_df['ID'][i]),
                                          nome_colaborador=veman_df['Colaborador'][i],
                                          data_ponto=veman_df['Data'][i],
                                          entrada_escala=veman_df['Entrada (Escala)'][i],
                                          saida_escala=veman_df['Saída (Escala)'][i],
                                          entrada_ponto=veman_df['Entrada (Ponto)'][i],
                                          saida_ponto=veman_df['Saída (Ponto)'][i],
                                          qtde_horas=veman_df['Total de HE'][i])

                database.session.add(horas)
                database.session.commit()

            flash('Dados Enviados Com Sucesso', 'alert-success')
    return render_template('registrar_hora_extra.html', registro=registro, veman_df=veman_df)


@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    cadastro_usuario = CriarUsuario()
    lista_funcionarios = Funcionario.query.all()
    lista_usuarios = Usuario.query.all()
    cadastro_usuario.nome_usuario.choices = [(funcionario.nome_funcionario) for funcionario in Funcionario.query.all()]
    if cadastro_usuario.validate_on_submit() and 'botao_submit_usuario' in request.form:
        usuario = Usuario(nome_usuario=cadastro_usuario.nome_usuario.data,
                          login=cadastro_usuario.login.data, senha=cadastro_usuario.senha.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Usuário {cadastro_usuario.nome_usuario.data} cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('usuarios'))
    return render_template('usuarios.html', cadastro_usuario=cadastro_usuario,
                           lista_funcionarios=lista_funcionarios, lista_usuarios=lista_usuarios)


@app.route('/', methods=['GET', 'POST'])
def login():
    form_login = Login()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(login=form_login.usuario.data).first()
        if usuario:
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso para o usuário(a): {form_login.usuario.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. Usuário ou Senha Incorretos', 'alert-danger')

    return render_template('login.html', form_login=form_login)


@app.route('/solicitarhe', methods=['GET', 'POST'])
def solicitarhe():
    solicitarhe = Solicitarhora()
    lista_funcionarios = Funcionario.query.all()
    lista_usuarios = Usuario.query.all()
    # nome = Funcionario.query.filter_by(nome_funcionario=current_user.nome_usuario).first()
    # usuario = nome.nome_funcionario
    usuario = current_user.nome_usuario
    lideranca = Funcionario.query.filter_by(nome_funcionario=current_user.nome_usuario).first()
    liderr = lideranca.lider
    id = lideranca.id
    if 'botao_submit_solicitarHE' in request.form:
        correcaodata = solicitarhe.datasolicitada.data
        dataFormatada = correcaodata.strftime('%d/%m/%Y')
        solicitacao = SolicitarHE(solicitante=usuario,
                                  lider=liderr, data=dataFormatada, motivo=solicitarhe.motivo.data,
                                  quantidade=solicitarhe.quantidade.data, id_solicitante=id)
        database.session.add(solicitacao)
        database.session.commit()
        print('deu cerot')
        flash(f'Solicitação realizada com sucesso.', 'alert-success')
        return redirect(url_for('solicitarhe'))
    return render_template('solicitarhoraextra.html', solicitarhe=solicitarhe,
                           lista_funcionarios=lista_funcionarios, lista_usuarios=lista_usuarios, liderr=liderr)


@app.route('/solicitar_orcamento', methods=['GET', 'POST'])
def solicitar_orcamento():
    solicitar_orcamento = SolicitarOrcamento()
    lista_funcionarios = Funcionario.query.all()
    lista_usuarios = Usuario.query.all()
    usuario = current_user.nome_usuario
    area = Funcionario.query.filter_by(nome_funcionario=current_user.nome_usuario).first()
    departamento = area.departamento
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y')
    if 'botao_submit_solicitarOrcamento' in request.form:
        data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
        solicitacao = Solicitar_Orcamento(solicitante=usuario,
                                          area=departamento, datasolicitacao=data_atual_formatada,
                                          motivo=solicitar_orcamento.motivo.data,
                                          tipo_aquisicao=solicitar_orcamento.tipo_aquisicao.data,
                                          tipo_solicitacao=solicitar_orcamento.tipo_solicitacao.data,
                                          planilha=solicitar_orcamento.planilha.data)
        database.session.add(solicitacao)
        database.session.commit()
        flash(f'Solicitação realizada com sucesso.', 'alert-success')
        return redirect(url_for('solicitar_orcamento'))
    return render_template('solicitar_orcamento.html', solicitar_orcamento=solicitar_orcamento, departamento=departamento,
                           data_atual_formatada=data_atual_formatada,
                           lista_funcionarios=lista_funcionarios, lista_usuarios=lista_usuarios)


@app.route('/enviar_orcamento/<solicitacao_id>', methods=['GET', 'POST'])
def enviar_orcamento(solicitacao_id):
    solicitacao = Solicitar_Orcamento.query.get(solicitacao_id)
    cadastrar_orcamento = RetornarOrcamento()
    data_atual = datetime.now()
    orcamentos = Enviar_Orcamento.query.filter_by(numero_solicitacao=solicitacao_id, status='Aguardando Aprovação - Departamento')
    lista = []
    for orcamento in orcamentos:
        lista.append(orcamento)
    if 'botao_submit_anexarOrcamento' in request.form:
        data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
        correcaodata = cadastrar_orcamento.data_orcamento.data
        dataFormatada = correcaodata.strftime('%d/%m/%Y')
        orcamento = Enviar_Orcamento(numero_solicitacao=solicitacao.id,numero_orcamento=cadastrar_orcamento.numero_orcamento.data,
                                     data_orcamento=dataFormatada, fornecedor=cadastrar_orcamento.fornecedor.data,
                                     valor_orcamento=cadastrar_orcamento.valor_orcamento.data,metodo_pagamento=cadastrar_orcamento.metodo_pagamento.data,
                                     anexo_orcamento=cadastrar_orcamento.anexo_orcamento.data, usuario_registro=current_user.nome_usuario,data_hora_registro=data_atual_formatada,
                                     )
        database.session.add(orcamento)
        database.session.commit()
        return redirect(url_for('enviar_orcamento',solicitacao_id=solicitacao.id))

    if 'botao_submit_enviarOrcamento' in request.form:
        data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
        if lista == []:
            flash(f'Favor anexar pelo menos um orçamento.', 'alert-danger')
        else:
            solicitacao.status = 'Aguardando Aprovação - Departamento'
            solicitacao.datahora_envio_orcamento = data_atual_formatada
            solicitacao.usuario_envio_orcamento = current_user.nome_usuario
            database.session.commit()
            flash('Orçamento Enviado com sucesso', 'alert-success')
            return redirect(url_for('retornar_solicitacao_orcamento'))
    return render_template('enviar_orcamento.html', solicitacao=solicitacao, cadastrar_orcamento=cadastrar_orcamento,orcamentos=orcamentos)


@app.route('/verificar_orcamento/<orcamento_id>', methods=['GET', 'POST'])
def verificar_orcamento(orcamento_id):
    solicitacao = Solicitar_Orcamento.query.get(orcamento_id)
    cadastrar_orcamento = RetornarOrcamento()
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
    orcamentos = Enviar_Orcamento.query.filter_by(numero_solicitacao=solicitacao.id,status='Aguardando Aprovação - Departamento')

    if 'botao_submit_outroOrcamento' in request.form:
        for orcamento in orcamentos:
            orcamento.status = 'Reprovado - Departamento'
            orcamento.usuario_reprovacao_departamento = current_user.nome_usuario
            orcamento.data_hora_reprovacao_departamento = data_atual_formatada
            database.session.commit()

        solicitacao.status = 'Aguardando Orçamento'
        solicitacao.datasolicitacao = data_atual_formatada
        database.session.commit()
        flash('Solicitação realizada com sucesso', 'alert-success')
        return redirect(url_for('aprovar_orcamento_departamento'))
    return render_template('verificar_orcamento.html', solicitacao=solicitacao, cadastrar_orcamento=cadastrar_orcamento,
                           orcamentos=orcamentos)


@app.route('/valirdar_orcamento/<orcamento_id>', methods=['GET', 'POST'])
def validar_orcamento(orcamento_id):
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
    orcamento = Enviar_Orcamento.query.get(orcamento_id)
    solicitacoes = Solicitar_Orcamento.query.filter_by(id=orcamento.numero_solicitacao)
    for solicitacao in solicitacoes:
        solicitacao.status = 'Aguardando Aprovação - Contrato'
    orcamento.status = 'Aguardando Aprovação - Contrato'
    orcamento.usuario_aprovacao_departamento = current_user.nome_usuario
    orcamento.data_hora_aprovacao_departamento = data_atual_formatada
    orcamentos = Enviar_Orcamento.query.filter_by(numero_solicitacao=orcamento.numero_solicitacao ,status='Aguardando Aprovação - Departamento')
    for itens in orcamentos:
        itens.status = 'Reprovado - Departamento'
        itens.usuario_reprovacao_departamento = current_user.nome_usuario
        itens.data_hora_reprovacao_departamento = data_atual_formatada

    database.session.commit()
    flash(f'Orçamento aprovado com sucesso.', 'alert-success')
    return redirect(url_for('aprovar_orcamento_departamento'))




@app.route('/orcamento/<orcamento_id>/excluir', methods=['GET', 'POST'])
def excluirorcamento(orcamento_id):
    orcamento = Enviar_Orcamento.query.get(orcamento_id)
    #orcamento1 = Enviar_Orcamento.query.filter_by(numero_solicitacao=orcamento)
    #solicitacao = Solicitar_Orcamento.query.filter_by(id=orcamento1)
    database.session.delete(orcamento)
    database.session.commit()
    return redirect(url_for('enviar_orcamento', solicitacao_id=orcamento.numero_solicitacao))


@app.route('/aprovar_orcamento_departamento', methods=['GET', 'POST'])
def aprovar_orcamento_departamento():
    aprovar_orcamento_departamento = Solicitar_Orcamento.query.filter_by(status='Aguardando Aprovação - Departamento', solicitante=current_user.nome_usuario)
    lista = []
    for item in aprovar_orcamento_departamento:
        lista.append(item)
    contagem = len(lista)
    return render_template('aprovar_orcamento_departamento.html',aprovar_orcamento_departamento=aprovar_orcamento_departamento,contagem=contagem)

@app.route('/aprovar_orcamento_contrato', methods=['GET', 'POST'])
def aprovar_orcamento_contrato():
    aprovar_orcamento_contrato = Solicitar_Orcamento.query.filter_by(status='Aguardando Aprovação - Contrato')
    lista = []
    for item in aprovar_orcamento_contrato:
        lista.append(item)
    contagem = len(lista)
    return render_template('aprovar_orcamento_contrato.html',aprovar_orcamento_contrato=aprovar_orcamento_contrato, contagem=contagem)


@app.route('/visualizar_solicitacao_orcamento/<solicitacao_id>', methods=['GET', 'POST'])
def visualizar_solicitacao_orcamento(solicitacao_id):
    solicitacao = Solicitar_Orcamento.query.get(solicitacao_id)
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
    #return redirect(url_for('visualizar_solicitacao_orcamento', solicitacao_id=solicitacao.id))
    return render_template('visualizar_solicitacao_orcamento.html',solicitacao=solicitacao, data_atual_formatada=data_atual_formatada)


@app.route('/visualizar_solicitacao_e_orcamento/<solicitacao_id>', methods=['GET', 'POST'])
def visualizar_solicitacao_e_orcamento(solicitacao_id):
    solicitacao = Solicitar_Orcamento.query.get(solicitacao_id)
    orcamento = Enviar_Orcamento.query.filter_by(numero_solicitacao=solicitacao.id,status='Aguardando Aprovação - Contrato')
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
    for item in orcamento:
        orcamento = Enviar_Orcamento.query.get(item.id)


    #return redirect(url_for('visualizar_solicitacao_orcamento', solicitacao_id=solicitacao.id))
    return render_template('visualizar_solicitacao_e_orcamento.html',solicitacao=solicitacao, data_atual_formatada=data_atual_formatada,orcamento=orcamento)


@app.route('/visualizar_orcamento/<orcamento_id>', methods=['GET', 'POST'])
def visualizar_orcamento(orcamento_id):
    orcamento = Enviar_Orcamento.query.get(orcamento_id)
    data_atual = datetime.now()
    data_atual_formatada = data_atual.strftime('%d/%m/%Y %H:%M')
    return render_template('visualizar_orcamento.html',orcamento=orcamento, data_atual_formatada=data_atual_formatada)


@app.route('/consusolicihe', methods=['GET', 'POST'])
def consusolicihe():
    solicitacoes = SolicitarHE.query.filter_by(solicitante=current_user.nome_usuario)
    bancohe_adm_unificado()
    return render_template('consusolicihe.html', solicitacoes=solicitacoes)


@app.route('/consultar_solicitacao_orcamento', methods=['GET', 'POST'])
def consultar_solicitacao_orcamento():
    consultar_solicitacao_orcamento = Solicitar_Orcamento.query.all()

    if request.method == 'GET':
        return render_template('consultar_solicitacao_orcamento.html',
                               consultar_solicitacao_orcamento=consultar_solicitacao_orcamento)
    if request.method == 'POST':
        id = request.form.get('id')
        solicitante = request.form.get('solicitante')
        area = request.form.get('departamento')
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        query = database.session.query(Solicitar_Orcamento)

        if id:
            query = query.filter_by(id=id)

        if solicitante:
            query = query.filter(Solicitar_Orcamento.solicitante.like(f'%{solicitante}%'))

        if area:
            query = query.filter(Solicitar_Orcamento.area.like(f'%{area}%'))

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Solicitar_Orcamento.datasolicitacao >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Solicitar_Orcamento.datasolicitacao <= end_date)

        results = query.all()

        if results:
            for resultado in results:
                print(resultado.id)
            return render_template('consultar_solicitacao_orcamento.html',
                                   consultar_solicitacao_orcamento=consultar_solicitacao_orcamento, results=results)
        else:
            flash(f'Nenhum resultado encontrado.', 'alert-danger')
            return render_template('consultar_solicitacao_orcamento.html',
                                   consultar_solicitacao_orcamento=consultar_solicitacao_orcamento, results=results)





@app.route('/retornar_solicitacao_orcamento', methods=['GET', 'POST'])
def retornar_solicitacao_orcamento():
    retornar_solicitacao_orcamento = Solicitar_Orcamento.query.filter_by(status='Aguardando Orçamento')
    lista = []
    for item in retornar_solicitacao_orcamento:
        lista.append(item)
    contagem = len(lista)

    return render_template('retornar_solicitacao_orcamento.html',retornar_solicitacao_orcamento=retornar_solicitacao_orcamento, contagem=contagem)


@app.route('/consulregistrohe', methods=['GET', 'POST'])
def consulregistrohe():
    registros = RegistroHoraExtra.query.all()
    return render_template('consulregistrohe.html', registros=registros)



@app.route('/validarhoraextra', methods=['GET', 'POST'])
def validarhoraextra():
    solicitacoes = SolicitarHE.query.filter_by(lider=current_user.nome_usuario)
    return render_template('validarhoraextra.html', solicitacoes=solicitacoes)


@app.route('/reprovarhoraextrabotao/<solicitacao_id>/reprovar', methods=['GET', 'POST'])
def reprovarhoraextrabotao(solicitacao_id):
    solicitacoes = SolicitarHE.query.get(solicitacao_id)
    solicitacoes.status = 'Reprovada'
    database.session.commit()
    flash('Solicitação reprovada com sucesso', 'alert-danger')
    return redirect(url_for('validarhoraextra'))


@app.route('/validarhoraextrabotao/<solicitacao_id>/validar', methods=['GET', 'POST'])
def validarhoraextrabotao(solicitacao_id):
    solicitacoes = SolicitarHE.query.get(solicitacao_id)
    solicitacoes.status = 'Aprovada'
    database.session.commit()
    flash('Solicitação aprovada com sucesso', 'alert-success')
    return redirect(url_for('validarhoraextra'))


def bancohe_adm_unificado():
    registros = RegistroHoraExtra.query.all()
    banco2 = BancoHE_ADM_Unificado.query.all()
    funcionarios = Funcionario.query.all()
    solicitacoes = SolicitarHE.query.all()
    lista_banco2 = []
    df = pd.DataFrame({'id_registro': [(item.id) for item in registros],
                       'id_colaborador': [(item.id_colaborador) for item in registros],
                       'nome_colaborador': [(item.nome_colaborador) for item in registros],
                       'data_ponto': [(item.data_ponto) for item in registros],
                       'entrada_escala': [(item.entrada_escala) for item in registros],
                       'saida_escala': [(item.saida_escala) for item in registros],
                       'entrada_ponto': [(item.entrada_ponto) for item in registros],
                       'saida_ponto': [(item.saida_ponto) for item in registros],
                       'qtde_horas': [(item.qtde_horas) for item in registros]})

    df2 = pd.DataFrame({'id_solicitação': [(solicitacao.id) for solicitacao in solicitacoes],
                        'id_solicitante': [(solicitacao.id_solicitante) for solicitacao in solicitacoes],
                        'solicitante': [(solicitacao.solicitante) for solicitacao in solicitacoes],
                        'lider': [(solicitacao.lider) for solicitacao in solicitacoes],
                        'data': [(solicitacao.data) for solicitacao in solicitacoes],
                        'motivo': [(solicitacao.motivo) for solicitacao in solicitacoes],
                        'quantidade': [(solicitacao.quantidade) for solicitacao in solicitacoes],
                        'status': [(solicitacao.status) for solicitacao in solicitacoes]})

    funcionarosdb = pd.DataFrame({'id_solicitante': [(funcionario.id_funcionario) for funcionario in funcionarios],
                                  'nome_colaborador': [(funcionario.nome_funcionario) for funcionario in funcionarios],
                                  'lider_2': [(funcionario.lider) for funcionario in funcionarios]})

    funcionarosdb.to_excel('funcionarios.xlsx')
    df2.to_excel('solicitação.xlsx')
    df.to_excel('registro.xlsx')
    df = df.rename(columns={'data_ponto': 'data', 'id_colaborador': 'id_solicitante'})
    df3 = df.merge(df2, on=['data', 'id_solicitante'], how='left')

    df3['qtde_horas'] = pd.to_datetime(df3['qtde_horas'], dayfirst=True, format='%H:%M:%S')
    df3['quantidade'] = pd.to_datetime(df3['quantidade'], dayfirst=True, format='%H:%M:%S')

    df3.loc[df3['status'] == 'Aprovada', 'desvio'] = (df3['qtde_horas'] - df3['quantidade']) * 24 * 60
    df3.loc[df3['qtde_horas'] < df3[
        'quantidade'], 'desvio'] = 0  # para quando a qtde de hrs executada for menor que a qtde aprovada
    df3.loc[df3['status'] == 'Reprovada', 'desvio'] = ((df3['qtde_horas'].dt.hour) * 60 + (df3['qtde_horas'].dt.minute))
    df3.loc[df3['status'] == 'Aguardando Retorno', 'desvio'] = (
                (df3['qtde_horas'].dt.hour) * 60 + (df3['qtde_horas'].dt.minute))
    df3['status'] = df3['status'].fillna('Sem Solicitação')

    df3.loc[df3['status'] == 'Sem Solicitação', 'desvio'] = (
                (df3['qtde_horas'].dt.hour) * 60 + (df3['qtde_horas'].dt.minute))
    # novas colunas
    df3['quantide_horas_liberadas'] = ((df3['quantidade'].dt.hour) * 60 + (df3['quantidade'].dt.minute)) / 60
    df3['quantide_horas_executadas'] = ((df3['qtde_horas'].dt.hour) * 60 + (df3['qtde_horas'].dt.minute)) / 60
    df3['desvio_hora'] = df3['desvio'] / 60

    df3 = df3.merge(funcionarosdb, on=['nome_colaborador'], how='inner')

    df3['id_solicitação'] = df3['id_solicitação'].fillna(0)
    df3.loc[df3['id_solicitação'] == 0, 'lider'] = df3['lider_2']
    # dropar colunas desnecessárias

    df3.to_excel('bancomacro.xlsx', index=False)


@app.route('/painelhoraextra', methods=['GET', 'POST'])
def painelhoraextra():
    df3 = pd.read_excel('bancomacro.xlsx')
    graficos = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

    fig = go.Figure(layout={'template': 'plotly_dark'})
    fig.add_trace(go.Scatter(x=df3['lider'], y=df3['desvio_hora']))
    fig.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        margin=go.Margin(l=10, r=10, t=10, b=10),
        autosize=True,
        showlegend=False,

    )

    graficos.layout = dbc.Container(
        dbc.Row([
            html.Div([
                html.Img(id='logo', src=graficos.get_asset_url('foto_veman/Veman.png'), height=50),
                html.H5('Controle Hora Extra Adm')

            ]),
            dbc.Col([
                dcc.Graph(id='line-graph', figure=fig),

            ])
        ])
    )

    if __name__ == "__main__":
        graficos.run_server(debug=True)

    return render_template('painelhoraextra.html')

# definir que se o funcionário for removido, automaticamente o usuario tb é

import pandas as pd
from flask import Flask, redirect, render_template, url_for, jsonify, request, flash, session


MASTER = {
    'adm1': 'webhookteste',
}

dataset_login = pd.read_csv('base_dados/base_dados_logins.csv')
dataset_api = pd.read_csv('base_dados/base_dados_api.csv')

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def index():
    etiquetas = ['email', 'senha']
    return render_template('index.html', titulo='Webhooker', labels_forms=etiquetas, botao='Login')


@app.route('/cadastrar')
def cadastrar():
    etiquetas = ['email', 'senha', 'confirmar senha', 'token']
    return render_template('cadastrar.html', titulo='Webhooker - Cadastro', labels_forms=etiquetas, botao='Cadastrar')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global dataset_login

    if request.method == 'POST':
        usuario = request.form['email']
        senha = request.form['senha']
        try:
            user_existe = (dataset_login['email'].values == usuario)
            senha_valida = (dataset_login['senha'].values == senha)

        except:
            pass
        if usuario in MASTER and MASTER[usuario] == senha:
            return redirect(url_for('dadosapiwh'))
        if user_existe and senha_valida:
            return redirect(url_for('dadosapiwh'))
        else:
            # Credenciais inválidas, exibir mensagem de erro
            flash('Usuário ou senha inválidos', 'error')
            return render_template('resultado_login.html')
    return redirect('/')


@app.route('/validandocadastro', methods=['GET', 'POST'])
def validandocadastro():
    global dataset_login
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar senha']
        token = request.form['token']

        linhas_totais = len(dataset_login)

        if email != '' and (senha == confirmar_senha) and token == 'uhdfaAADF123':
            # Autenticação bem-sucedida, redirecionar para a página inicial
            nova_linha = {
                'email': [email],
                'senha': [senha],
                'confirmar_senha': [confirmar_senha],
                'token': [token]
            }
            linha = pd.DataFrame(nova_linha)
            linha.index = [linhas_totais]
            novo_dataset = pd.concat([dataset_login, linha], ignore_index=True)
            novo_dataset.to_csv('base_dados/base_dados_logins.csv', index=False)
            linhas_totais += 1

            return render_template('sucesso_cadastro.html', resultado='Cadastro efetuado com sucesso!', titulo='Webhook')

        else:
            # Credenciais inválidas, exibir mensagem de erro
            flash('Cadastro recusado! Tente novamente.', 'error')
            return render_template('resultado_login.html')
    return redirect('/')


@app.route('/resultado_login')
def resultado_login():
    return render_template('resultado_login.html', titulo='Resultado Login')


@app.route('/dadosapiwh')
def dadosapiwh():
    global dataset_api
    data_json = dataset_api.to_json(orient='records', force_ascii=False)
    return jsonify(data_json)


app.run(debug=True, host='0.0.0.0')
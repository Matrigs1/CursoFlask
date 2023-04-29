from flask import Flask, render_template, request, redirect, session, flash, url_for #dependências necessárias para a aplicação.

class Jogo: #classe para instanciar jogos para o site.
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3] #coloca os jogos instanciados em uma lista.

class Usuario: #classe para a autenticação de usuários.
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Mateus Rodrigues", "MR", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")

usuarios = { usuario1.nickname : usuario1, #jogando os usuários em um dict com o atributo nickname como chave.
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__) #passa o arquivo atual e instancia uma app Flask.
app.secret_key = 'alura' #secret_key para os cookies não sofrerem adulteração.

@app.route('/') #criação de endpoints.
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista) #renderiza arquivos html e manda para eles partes do código como atributos.

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: #checkando se o usuário não está logado.
        return redirect(url_for('login', proxima=url_for('novo'))) #se não estiver, redireciona para a página login novamente.
    return render_template('novo.html', titulo='Novo Jogo') #se estiver, renderiza o novo.

@app.route('/criar', methods=['POST',]) #categorizando método como POST.
def criar():
    nome = request.form['nome'] #informações do formulário serão passadas para as variáveis.
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console) #instancia um novo jogo com as infos pegas.
    lista.append(jogo) #adiciona o jogo a lista.
    return redirect(url_for('index')) #redireciona para o index (contém a lista dos jogos).

@app.route('/login')
def login():
    proxima = request.args.get('proxima') #pega os args da url.
    return render_template('login.html', proxima=proxima) #passa o arg para o template.

@app.route('/autenticar', methods=['POST',])
def autenticar(): #faz a autenticação do usuário (procura as informações nos objs).
    if request.form['usuario'] in usuarios: #se achar o usuário
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha: #se a senha bater
            session['usuario_logado'] = usuario.nickname #salva em usuários logados
            flash(usuario.nickname + ' logado com sucesso!') #exibe mensagem
            proxima_pagina = request.form['proxima'] 
            return redirect(proxima_pagina) #redireciona para a próxima página (novo).
    else: #se as infos não baterem
        flash('Usuário não logado.')
        return redirect(url_for('login')) #redireciona novamente para o login.

@app.route('/logout')
def logout(): #logout
    session['usuario_logado'] = None #reseta as informações dos usuários logados
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index')) #redireciona para o index.

app.run(debug=True) #auto refresh da app.
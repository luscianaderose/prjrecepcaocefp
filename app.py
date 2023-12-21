import os
from flask import Flask, request, redirect, send_from_directory

class Pessoa:
    def __init__(self, numero, nome, chamado=0, camara=None):
        self.nome = nome
        self.numero = numero
        self.chamado = chamado
        self.camara = camara

    def __str__(self):
        return self.nome
    
    def csv(self):
        return f'{self.numero},{self.nome},{self.chamado},{self.camara}'
    
    def nome_exibicao(self):
        if self.chamado == 1:
            return f'<s>{self.nome}</s> {self.camara}'
        else:
            return f'{self.nome}'

class Camara:
    def __init__(self, numero_camara, fila, nome_fila):
        self.numero_camara = numero_camara
        self.fila = fila
        self.nome_fila = nome_fila
        self.pessoa_em_atendimento = 'Nenhum'
        self.numero_de_atendimentos = 0

    def chamar_atendido(self):
        if self.numero_de_atendimentos >= 5:
            self.pessoa_em_atendimento = 'FECHADA'
            return 'CÂMARA FECHADA'
        for pessoa in self.fila:
            if not pessoa.chamado:
                self.pessoa_em_atendimento = pessoa
                self.pessoa_em_atendimento.camara = self.numero_camara
                break
        else:
            self.pessoa_em_atendimento = 'FECHADA'
            return 'CÂMARA FECHADA'
        self.pessoa_em_atendimento.chamado = 1
        self.numero_de_atendimentos += 1
        retorno = f'Câmara {self.numero_camara} chamando {self.pessoa_em_atendimento}.'
        if self.numero_de_atendimentos >= 5:
            retorno = retorno + f' Avisar que é o último atendido.{self.numero_camara}.'
        return retorno

    
    def bolinhas(self):
        bolinhas = []
        for bola in range(0, self.numero_de_atendimentos):
            bolinhas.append('&#9899;')
        for bola in range(0, 5 - self.numero_de_atendimentos):
            bolinhas.append('&#9898;')
        return ''.join(bolinhas)

def salvar_fila(fila, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for pessoa in fila:
            f.write(f'{pessoa.csv()}\n')

def ler_fila(nome_arquivo):
    lista_pessoas = []
    with open(nome_arquivo, 'r') as f:
        for linha in f.read().splitlines():
            if not linha:
                continue
            numero, nome, chamado, camara = linha.split(',')
            pessoa = Pessoa(int(numero), nome, int(chamado), camara)
            lista_pessoas.append(pessoa)
        return lista_pessoas

def salvar_camaras(dict_camaras, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for camara in dict_camaras.values():
            f.write(f'{camara.numero_camara},{camara.pessoa_em_atendimento},{camara.numero_de_atendimentos}\n')

def ler_camaras(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read().splitlines()

PASTA_ARQUIVOS = os.path.join(os.path.expanduser('~'), '.recepcao-camaras')
if not os.path.exists(PASTA_ARQUIVOS): 
    os.makedirs(PASTA_ARQUIVOS) 
ARQUIVO_FILA_VID = os.path.join(PASTA_ARQUIVOS, 'Fila-videncia.csv')
ARQUIVO_FILA_PRE = os.path.join(PASTA_ARQUIVOS, 'Fila-prece.csv')
ARQUIVO_CAMARAS = os.path.join(PASTA_ARQUIVOS, 'Camaras-info.csv')

for arquivo in [ARQUIVO_FILA_VID, ARQUIVO_FILA_PRE, ARQUIVO_CAMARAS]:
    with open(arquivo, 'a+'):
        pass

fila_videncia = ler_fila(ARQUIVO_FILA_VID)
fila_prece = ler_fila(ARQUIVO_FILA_PRE)

NOME_FILA_VIDENCIA = 'Vidência'
NOME_FILA_PRECE = 'Prece'

camara2 = Camara("2", fila_videncia, NOME_FILA_VIDENCIA)
camara4 = Camara("4", fila_videncia, NOME_FILA_VIDENCIA)
camara3 = Camara("3", fila_prece, NOME_FILA_PRECE)
camara3A = Camara("3A", fila_prece, NOME_FILA_PRECE)

dict_camaras = {
    '2':camara2,
    '4':camara4,
    '3':camara3,
    '3A':camara3A,
}

dados_camaras = ler_camaras(ARQUIVO_CAMARAS)

for linha in dados_camaras:
    numero_camara, pessoa_em_atendimento, numero_de_atendimentos = linha.split(',')
    camara = dict_camaras[numero_camara.strip()]
    camara.pessoa_em_atendimento = pessoa_em_atendimento.strip()
    camara.numero_de_atendimentos = int(numero_de_atendimentos.strip())

def registrar_pessoa(nome, fila):
    if fila == "prece":
        fila_prece.append(nome)
    elif fila == "videncia":
        fila_videncia.append(nome)

print(f"{fila_prece=}")
print(f"{fila_videncia=}")

camara_chamando = ''

app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def get_recepcao():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    tit_recep = '<h1>RECEPÇÃO DAS CÂMARAS</h1>'
    tit_adicionar = '<h5>ADICIONAR NOME NA FILA</h4>'
    form = f'''<form action="/adicionar_atendido">
        <input name="nome_atendido" type="text" placeholder="Digite o nome"><br>
        <div class="div-radio"> 
        <input class="radio" type="radio" id="videncia" name="nome_fila" value="videncia" required>
        <label class="label1" for="videncia"><div class="radio-txt">VIDÊNCIA</div></label><br>
        <input class="radio" type="radio" id="prece" name="nome_fila" value="prece">
        <label class="label2" for="prece"><div class="radio-txt">PRECE</div></label></div><br>          
        <button>ADICIONAR</button>
        </form>'''
    
    # CÂMARAS
    tit_vid = '<div class="tit-vid-pre"><div class="tit-vid"><h2>VIDÊNCIA</h2></div></div>'
    tit_pre = '<div class="tit-vid-pre"><div class="tit-pre"><h2>PRECE</h2></div></div>'
    html_camaras_vid = ''
    html_camaras_pre = ''
    for camara in dict_camaras.values():
        html_camara = f'''<div class='camara'><p><h3>CÂMARA {camara.numero_camara}</h3></p>
        <p>ATENDENDO<br><h4>{camara.pessoa_em_atendimento}</h4></p>
        <p>ATENDIMENTOS<br>
        <a href="/bolinhas?modo=subtracao&numero_camara={camara.numero_camara}">-</a>{camara.bolinhas()}
        <a href="/bolinhas?modo=adicao&numero_camara={camara.numero_camara}">+</a></p>
        <p><a href="/chamar_proximo/{camara.numero_camara}">Chamar próximo</a></p>
        <p><a href="/reabrir_camara/{camara.numero_camara}">Reabrir câmara</a></p></div>'''
        if camara.nome_fila == NOME_FILA_VIDENCIA:
            html_camaras_vid = html_camaras_vid + html_camara
        elif camara.nome_fila == NOME_FILA_PRECE:
            html_camaras_pre = html_camaras_pre + html_camara
    html_camaras_vid = '<div class="camara-vid">' + html_camaras_vid + '</div>'
    html_camaras_pre = '<div class="camara-pre">' + html_camaras_pre + '</div>'

    # LISTAS/FILAS
    tit_lista_fila_vid = '<h3>LISTA VIDÊNCIA</h3>'
    tit_lista_fila_pre = '<h3>LISTA PRECE</h3>'
    html_fila_vid = '<div class="lista-vid">' + tit_lista_fila_vid
    for index, pessoa in enumerate(fila_videncia):
        html_fila_vid = html_fila_vid + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a></p>'''
    html_fila_vid = html_fila_vid + '</div>'
    html_fila_pre = '<div class="lista-pre">' + tit_lista_fila_pre
    for index, pessoa in enumerate(fila_prece):
        html_fila_pre = html_fila_pre + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila=prece&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila=prece&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a></p>'''
    html_fila_pre = html_fila_pre + '</div>'

    tit_menu = '<h1>MENU</h1>'
    tv = '<a href="/tv">TV</a></p>'
    bt_reiniciar = '<a href="/reiniciar_tudo"><button>REINICAR TUDO</button></a>'

    return  head + '<body>' + tit_recep + tit_adicionar + form + tit_vid + html_camaras_vid + html_fila_vid + tit_pre + html_camaras_pre + html_fila_pre + tit_menu + tv + bt_reiniciar + '</body>'

@app.route('/tv')
def tv():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/tv.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    html_camaras = ''
    html_camaras_vid = ''
    html_camaras_pre = ''
    for camara in dict_camaras.values():
        html_camaras = f'''<div class='tv-camara'><p>CÂMARA {camara.nome_fila}<br><h1>{camara.numero_camara}</h1><br>CHAMA</p>
        <p><h2>{camara.pessoa_em_atendimento}</h2></p></div>'''.upper()
        if camara.nome_fila == NOME_FILA_VIDENCIA:
            html_camaras_vid = html_camaras_vid + html_camaras
        elif camara.nome_fila == NOME_FILA_PRECE:
            html_camaras_pre = html_camaras_pre + html_camaras
    html_camaras_vid = '<div class="tv-vid">' + html_camaras_vid + '</div>'
    html_camaras_pre = '<div class="tv-pre">' + html_camaras_pre + '</div>'
    voltar = '<a href="/">VOLTAR</a>'
    return head + '<body>' + html_camaras_vid + html_camaras_pre + voltar + '</body>'

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo_(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.chamar_atendido()
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    return redirect('/')

@app.route("/adicionar_atendido")
def adicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == 'prece':
        if fila_prece:
            numero = int(fila_prece[-1].numero) + 1
        else:
            numero = 1
        pessoa = Pessoa(numero, nome_atendido)
        fila_prece.append(pessoa)
        salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    elif nome_fila == 'videncia':
        if fila_videncia:
            numero = int(fila_videncia[-1].numero) + 1
        else:
            numero = 1
        pessoa = Pessoa(numero, nome_atendido)
        fila_videncia.append(pessoa)
        salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route('/reabrir_camara/<numero_camara>')
def reabrir_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.numero_de_atendimentos = 0
    camara.pessoa_em_atendimento = 'Nenhum'
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route('/reiniciar_tudo')
def reiniciar_tudo():
    return '''<p>Tem certeza que deseja deletar todas as informações?</p>
            <a href='/reiniciar_tudo_confirmado'>Sim</a><a href='/' style='margin-left:20px'>Cancelar</a>'''

@app.route('/reiniciar_tudo_confirmado')
def reiniciar_tudo_confirmado():
    for camara in dict_camaras.values():
        camara.numero_de_atendimentos = 0
        camara.pessoa_em_atendimento = 'Nenhum'
    fila_prece.clear()
    salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    fila_videncia.clear()
    salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/remover_atendido")
def remover_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == 'prece':
        for pessoa in fila_prece:
            if pessoa.numero == numero_atendido:
                fila_prece.remove(pessoa)
                break
        salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    elif nome_fila == 'videncia':
        for pessoa in fila_videncia:
            if pessoa.numero == numero_atendido:
                fila_videncia.remove(pessoa)
                break
        salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route("/editar_atendido")
def editar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == 'videncia':
        for pessoa in fila_videncia:
            if pessoa.numero == numero_atendido:
                return f'''<form action='/editar_atendido_confirmado'><input type='text' name='nome_atendido' value='{pessoa.nome}'>
                <input type='hidden' name='nome_fila' value='{nome_fila}'>
                <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
                <button type='submit'>Confirmar</button>
                </form>'''
    if nome_fila == 'prece':
        for pessoa in fila_prece:
            if pessoa.numero == numero_atendido:
                return f'''<form action='/editar_atendido_confirmado'><input type='text' name='nome_atendido' value='{pessoa.nome}'>
                <input type='hidden' name='nome_fila' value='{nome_fila}'>
                <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
                <button type='submit'>Confirmar</button>
                </form>'''
    return redirect('/')

@app.route('/editar_atendido_confirmado')
def editar_atendido_confirmado():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == 'videncia':
        for pessoa in fila_videncia:
            if pessoa.numero == numero_atendido:
                pessoa.nome = nome_atendido
                break
    elif nome_fila == 'prece':
        for pessoa in fila_prece:
            if pessoa.numero == numero_atendido:
                pessoa.nome = nome_atendido
                break
    return redirect('/')

@app.route('/bolinhas')
def bolinhas():
    modo = request.args.get('modo')
    numero_camara = request.args.get('numero_camara')
    camara = dict_camaras.get(numero_camara)
    if modo == 'adicao' and camara.numero_de_atendimentos < 5:
        camara.numero_de_atendimentos += 1
    elif modo == 'subtracao' and camara.numero_de_atendimentos > 0:
        camara.numero_de_atendimentos -= 1
    return redirect('/')


app.run(debug=True)

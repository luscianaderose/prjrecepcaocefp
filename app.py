from flask import Flask, request, redirect, send_from_directory

class Camara:
    def __init__(self, numero_camara, fila, nome_fila):
        self.numero_camara = numero_camara
        self.fila = fila
        self.nome_fila = nome_fila
        self.pessoa_em_atendimento = 'Nenhum'
        self.numero_de_atendimentos = 0

    def chamar_atendido(self):
        if len(self.fila) < 1 or self.numero_de_atendimentos >= 5:
            self.pessoa_em_atendimento = "Fechada"
            return "Câmara fechada"
        self.pessoa_em_atendimento = self.fila[0]
        self.fila.pop(0)
        self.numero_de_atendimentos += 1
        retorno = f"Câmara {self.numero_camara} chamando {self.pessoa_em_atendimento}."
        if len(self.fila) < 1 or self.numero_de_atendimentos >= 5:
            retorno = retorno + f" Avisar que é o último atendido.{self.numero_camara}."
        return retorno
    
    def bolinhas(self):
        bolinhas = []
        for bola in range(0,self.numero_de_atendimentos):
            bolinhas.append('&#11044;')
        for bola in range(0, 5 - self.numero_de_atendimentos):
            bolinhas.append('&#9711;')
        return ''.join(bolinhas)

def salvar_fila(fila, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        f.write('\n'.join(fila))

def ler_fila(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read().splitlines()

def salvar_camaras(dict_camaras, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for camara in dict_camaras.values():
            f.write(f'{camara.pessoa_em_atendimento}\n{camara.numero_de_atendimentos}\n')

def ler_camaras(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read().splitlines()

fila_prece = ler_fila('Fila-prece')
fila_videncia = ler_fila('Fila-videncia')

NOME_FILA_VIDENCIA = 'v'
NOME_FILA_PRECE = 'p'

camara2 = Camara("2", fila_videncia, NOME_FILA_VIDENCIA)
camara4 = Camara("4", fila_videncia, NOME_FILA_VIDENCIA)
camara3 = Camara("3", fila_prece, NOME_FILA_PRECE)
camara3A = Camara("3A", fila_prece, NOME_FILA_PRECE)

atendido_camara2, atendimentos_camara2, atendido_camara4, atendimentos_camara4, atendido_camara3, atendimentos_camara3, atendido_camara3A, atendimentos_camara3A = ler_camaras('Camaras-info')
camara2.pessoa_em_atendimento = atendido_camara2
camara2.numero_de_atendimentos = int(atendimentos_camara2)
camara4.pessoa_em_atendimento = atendido_camara4
camara4.numero_de_atendimentos = int(atendimentos_camara4)
camara3.pessoa_em_atendimento = atendido_camara3
camara3.numero_de_atendimentos = int(atendimentos_camara3)
camara3A.pessoa_em_atendimento = atendido_camara3A
camara3A.numero_de_atendimentos = int(atendimentos_camara3A)

def registrar_pessoa(nome, fila):
    if fila == "prece":
        fila_prece.append(nome)
    elif fila == "videncia":
        fila_videncia.append(nome)

print(f"{fila_prece=}")
print(f"{fila_videncia=}")

dict_camaras = {
    '2':camara2,
    '4':camara4,
    '3':camara3,
    '3A':camara3A,
}

camara_chamando = ""

app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route("/")
def get_recepcao():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    tit_recep = '<h1>Recepção das câmaras</h1>'
    tit_adicionar = '<h3>Adicionar nome na fila</h3>'
    form = f'''<form action="/adicionar_atendido">
        <input name="nome_atendido" type="text" placeholder="Digite o nome"><br>
        <div class="div-radio"> 
        <input class="radio" type="radio" id="videncia" name="nome_fila" value="videncia" required>
        <label class="label1" for="videncia"><div class="radio-txt">Vidência</div></label><br>
        <input class="radio" type="radio" id="prece" name="nome_fila" value="prece">
        <label class="label2" for="prece"><div class="radio-txt">Prece</div></label></div><br>          
        <button>Enviar</button>
        </form>'''
    tit_lista_fila_vid = 'Lista vidência'
    tit_lista_fila_pre = 'Lista prece'
    html_fila_vid = '<div class="lista">' + tit_lista_fila_vid
    for numero, nome in enumerate(fila_videncia):
        html_fila_vid = html_fila_vid + f'<p>{numero + 1}. {nome}<a class="link-remover" href="/remover_atendido?nome_fila=videncia&nome_atendido={nome}"><img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a></p>'
    html_fila_vid = html_fila_vid + '</div>'
    html_fila_pre = '<div class="lista">' + tit_lista_fila_pre
    for numero, nome in enumerate(fila_prece):
        html_fila_pre = html_fila_pre + f'<p>{numero + 1}. {nome}<a class="link-remover" href="/remover_atendido?nome_fila=prece&nome_atendido={nome}"><img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a></p>'
    html_fila_pre = html_fila_pre + '</div>'
    html_camaras_vid = '<div class="camaras-div">'
    html_camaras_pre = '<div class="camaras-div">'
    for camara in dict_camaras.values():
        html_camara = f'''<div class='camara'><p><h3>Câmara {camara.numero_camara}</h3></p>
        <p>Atendido<br>{camara.pessoa_em_atendimento}</p>
        <p>Atendimentos<br>{camara.bolinhas()}</p>
        <p><a href="/chamar_proximo/{camara.numero_camara}">Chamar próximo</a></p>
        <p><a href="/reabrir_camara/{camara.numero_camara}">Reabrir câmara</a></p></div>'''
        if camara.nome_fila == NOME_FILA_VIDENCIA:
            html_camaras_vid = html_camaras_vid + html_camara
        elif camara.nome_fila == NOME_FILA_PRECE:
            html_camaras_pre = html_camaras_pre + html_camara
    html_camaras_vid = html_camaras_vid + '</div>'
    html_camaras_pre = html_camaras_pre + '</div>'
    tit_menu = '<h1>Menu</h1>'
    tv = '<a href="/tv">TV</a></p>'
    bt_reiniciar = '<a href="/reiniciar_tudo"><button>Reiniciar tudo</button></a>'
    return  head + '<body>' + tit_recep + tit_adicionar + form + html_camaras_vid + html_fila_vid + html_camaras_pre + html_fila_pre + tit_menu + tv + bt_reiniciar + '</body>'

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo_(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.chamar_atendido()
    salvar_camaras(dict_camaras, 'Camaras-info')
    salvar_fila(fila_prece, 'Fila-prece')
    salvar_fila(fila_videncia, 'Fila-videncia')
    return redirect('/')

@app.route("/adicionar_atendido")
def adicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == 'prece':
        fila_prece.append(nome_atendido)
        salvar_fila(fila_prece, 'Fila-prece')
    elif nome_fila == 'videncia':
        fila_videncia.append(nome_atendido)
        salvar_fila(fila_videncia, 'Fila-videncia')
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route('/reabrir_camara/<numero_camara>')
def reabrir_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.numero_de_atendimentos = 0
    camara.pessoa_em_atendimento = 'Nenhum'
    salvar_camaras(dict_camaras, 'Camaras-info')
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
    salvar_fila(fila_prece, 'Fila-prece')
    fila_videncia.clear()
    salvar_fila(fila_videncia, 'Fila-videncia')
    salvar_camaras(dict_camaras, 'Camaras-info')
    return redirect('/')

@app.route('/tv')
def tv():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/tv.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    html_camaras = ''
    for camara in dict_camaras.values():
        html_camaras = html_camaras + f'''<p><h3>CÂMARA {camara.numero_camara} CHAMA</h3></p>
        <p><h1>{camara.pessoa_em_atendimento}</h1></p>'''.upper()
    voltar = '<a href="/">Voltar</a>'
    return head + '<body>' + html_camaras + voltar + '</body>'

@app.route("/remover_atendido")
def remover_atendido():
    nome_fila = request.args.get('nome_fila')
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == 'prece':
        fila_prece.remove(nome_atendido)
        salvar_fila(fila_prece, 'Fila-prece')
    elif nome_fila == 'videncia':
        fila_videncia.remove(nome_atendido)
        salvar_fila(fila_videncia, 'Fila-videncia')
    else: 
        return 'Fila incorreta!'
    return redirect('/')

app.run(debug=True)

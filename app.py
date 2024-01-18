import os
from flask import Flask, request, redirect, send_from_directory
from datetime import datetime, date
import calendar  
import locale

locale.setlocale(locale.LC_ALL,'pt_BR')
    


class Pessoa:
    def __init__(self, numero, nome, chamado=0, camara=None, dupla=None):
        self.nome = nome
        self.numero = numero
        self.chamado = chamado
        self.camara = camara
        self.dupla = dupla

    def __str__(self):
        return self.nome
    
    def csv(self):
        return f'{self.numero},{self.nome},{self.chamado},{self.camara}'
    
    def nome_exibicao(self):
        if self.chamado == 1:
            return f'<s>{self.nome}</s> - {self.camara}'
        else:
            return f'{self.nome}'
        
    def __repr__(self):
        return self.nome
    
class Fila():
    def __init__(self, atividade):
        self.atividade = atividade
        self.fila = {}
        self.proximo_numero = 1
    
    def __contains__(self, numero):
        return numero in self.fila
    
    def adicionar_pessoa(self, pessoa, numero):
        for p in self.fila.values():
            if p.nome == pessoa.nome:
                raise Exception('Não foi possível registrar porque o nome já existe.')
        if numero in self.fila:
            raise Exception('Não foi possível registrar porque o número já existe.')
        self.fila[numero] = pessoa
        self.proximo_numero += 1

    def remover_pessoa(self, numero):
        if numero not in self.fila:
            raise Exception('Não foi possível remover porque a pessoa não existe.')
        del self.fila[numero]

    def editar_pessoa(self, numero, nome):
        for p in self.fila.values():
            if p.nome == nome:
                raise Exception('Não foi possível registrar porque o nome já existe.')
        if numero not in self.fila:
            raise Exception('Não foi possível registrar porque o número não existe.')
        self.fila[numero].nome = nome

    def values(self):
        return sorted(self.fila.values(), key=lambda p: p.numero)
    
    def clear(self):
        self.fila.clear()

    def get(self, numero):
        if numero in self.fila:
            return self.fila[numero]
        return None
    
    def trocar_posicao(self, n1, n2):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível mover!')
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        pessoa1.numero = n2
        pessoa2.numero = n1
        self.fila[n1] = pessoa2
        self.fila[n2] = pessoa1

    def keys(self):
        return sorted(self.fila.keys())


class Dupla:
    def __init__(self, pessoa1, pessoa2):
        self.pessoa1 = pessoa1
        self.pessoa2 = pessoa2

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
        for pessoa in self.fila.values():
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

def salvar_fila(fila: Fila, nome_arquivo: str):
    with open(nome_arquivo, 'w') as f:
        for pessoa in fila.values():
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

# fila_videncia = ler_fila(ARQUIVO_FILA_VID)
# fila_prece = ler_fila(ARQUIVO_FILA_PRE)

NOME_FILA_VIDENCIA = 'Vidência'
NOME_FILA_PRECE = 'Prece'

fila_videncia = Fila(NOME_FILA_VIDENCIA)
fila_prece = Fila(NOME_FILA_PRECE)

for pessoa in ler_fila(ARQUIVO_FILA_VID):
    fila_videncia.adicionar_pessoa(pessoa, pessoa.numero)

for pessoa in ler_fila(ARQUIVO_FILA_PRE):
    fila_prece.adicionar_pessoa(pessoa, pessoa.numero)

if fila_videncia.fila:
    fila_videncia.proximo_numero = fila_videncia.values()[-1].numero + 1
if fila_prece.fila:
    fila_prece.proximo_numero = fila_prece.values()[-1].numero + 1

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


app = Flask(__name__)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# DATA E HORA
dia_semana = date.today().weekday()
#nomes = ("SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM")
#nomes = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
nomes = ("SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO")
data_e_hora_atuais = datetime.now()
dia_semana_usar = nomes[dia_semana]
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m %H:%M')
data = dia_semana_usar + ' ' + data_e_hora_em_texto

# CALENDARIO
ano = data_e_hora_atuais.year
mes = data_e_hora_atuais.month
calendario = '<div class="di-calendario"><pre>' + (calendar.calendar(ano, mes)) + '</pre></div>'

voltar = '<a href="/">VOLTAR</a>'

@app.route('/')
def get_recepcao():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    tit_recep = '<div class="div-cabecalho"><div class="dc-congrega"><img alt="CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA" src="/static/img/cefp.png"></div>' + '<div class="dc-tit-principal"><h1>RECEPÇÃO DAS CÂMARAS</h1></div>' + '<div class="dc-data">' + data + '</div></div>'
    tit_adicionar = '<div class="div-adicionar-nomes"><div class="dan-tit-form"><h5>ADICIONAR NOME NA FILA</h4></div>'
    form = f'''<div class="dan-form"><form action="/adicionar_atendido">
        <input name="nome_atendido" type="text" placeholder="Digite o nome"></div>
        <div class="dan-bt-vid-pre"><div class="bt-vid-pre-radio"> 
        <input class="radio" type="radio" id="videncia" name="nome_fila" value="videncia" required>
        <label class="label1" for="videncia"><div class="radio-txt">VIDÊNCIA</div></label>
        <input class="radio" type="radio" id="prece" name="nome_fila" value="prece">
        <label class="label2" for="prece"><div class="radio-txt">PRECE</div></label></div></div>          
        <div class="dan-bt-adicionar"><div class="dan-bt-adicionar-centro-vertical"><button>ADICIONAR</button></div></div>
        </form></div>'''
    
    espaco = '<div class="div-espaco"> </div>'
    
    # CÂMARAS
    tit_vid = '<div class="div-vid-pre"><div class="div-vid"><div class="tit-vid-pre"><div class="tit-vid"><h2>VIDÊNCIA</h2></div></div>'
    tit_pre = '<div class="div-pre"><div class="tit-vid-pre"><div class="tit-pre"><h2>PRECE</h2></div></div>'
    html_camaras_vid = ''
    html_camaras_pre = ''
    for camara in dict_camaras.values():
        html_camara = f'''<div class='camara'><p><h3>CÂMARA {camara.numero_camara}</h3></p>
        <p>ATENDENDO<br><h4>{camara.pessoa_em_atendimento}</h4></p>
        <p>ATENDIMENTOS<br>
        <a class="linkbolinhas" href="/bolinhas?modo=subtracao&numero_camara={camara.numero_camara}"><b>-</b></a>{camara.bolinhas()}
        <a class="linkbolinhas" href="/bolinhas?modo=adicao&numero_camara={camara.numero_camara}"><b>+</b></a></p>
        <p><button type="button"><a class="btcamara" href="/chamar_proximo/{camara.numero_camara}">Chamar próximo</a></button></p>
        <p><button type="button"><a class="btcamara" href="/reabrir_camara/{camara.numero_camara}">Reabrir câmara</a></button></p></div>'''
        if camara.nome_fila == NOME_FILA_VIDENCIA:
            html_camaras_vid = html_camaras_vid + html_camara
        elif camara.nome_fila == NOME_FILA_PRECE:
            html_camaras_pre = html_camaras_pre + html_camara
    html_camaras_vid = '<div class="camara-vid">' + html_camaras_vid + '</div>'
    html_camaras_pre = '<div class="camara-pre">' + html_camaras_pre + '</div>'


    # LISTAS/FILAS
    tit_lista_fila_vid = '<h3>FILA VIDÊNCIA</h3>Nome - câmara'
    tit_lista_fila_pre = '<h3>FILA PRECE</h3>Nome - câmara'
    html_fila_vid = '<div class="lista-vid">' + tit_lista_fila_vid
    for index, pessoa in enumerate(fila_videncia.values()):
        html_fila_vid = html_fila_vid + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}&moverpara=cima">
        <img alt="Reposicionar" src="/static/img/seta-cima.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila=videncia&numero_atendido={pessoa.numero}&moverpara=baixo">
        <img alt="Reposicionar" src="/static/img/seta-baixo.png" width="16" height="16"></a></p>'''
    html_fila_vid = html_fila_vid + '</div></div>' #tirei uma /div
    html_fila_pre = '<div class="lista-pre">' + tit_lista_fila_pre
    for index, pessoa in enumerate(fila_prece.values()):
        html_fila_pre = html_fila_pre + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila=prece&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila=prece&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila=prece&numero_atendido={pessoa.numero}&moverpara=cima">
        <img alt="Reposicionar" src="/static/img/seta-cima.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila=prece&numero_atendido={pessoa.numero}&moverpara=baixo">
        <img alt="Reposicionar" src="/static/img/seta-baixo.png" width="16" height="16"></a></p>'''
    html_fila_pre = html_fila_pre + '</div></div></div>'

    camaras = tit_vid + html_camaras_vid + html_fila_vid + espaco + tit_pre + html_camaras_pre + html_fila_pre

    # MENU
    tit_menu = '<div class="div-menu"><div class="dm-tit"><h3>MENU</h3></div>'
    tv = '<div class="dm-bt-tv"><div class="vertical-center"><a href="/tv"><button>TV</button></a></div></div>'
    bt_reiniciar = '<div class="dm-bt-reiniciar"><div class="vertical-center"><a href="/reiniciar_tudo"><button>REINICAR TUDO</button></a></div></div></div>'
    menu = tit_menu + tv + bt_reiniciar

    # INFO
    tit_info = '<div class="div-info"><div class=""><h3>INFORMAÇÕES</h3></div>'
    fim = '</div>'
    texto = '''1. Verificar no cartão da pessoa se data da marcação é a data de hoje.<br>
    2. Adicionar o nome na fila correspondente.<br>
    3. Carimbar o cartão.<br>
    4. Pedir para sentar no lugar correto.<br>
    5. Quando a câmara chamar, clicar em 'chamar próximo' e chamar o próximo nome. O nome é riscado, a câmara que chamou fica registrada, e uma bolinha branca fica preenchida, tudo automaticamente.<br>
    6. Quando atingir o limite de atendimentos das câmaras que é representado por cinco bolinhas cheias, avisar que a câmara fechou.<br><br><br>'''
    info = tit_info + texto + calendario + fim

    return  head + '<body>' + tit_recep + tit_adicionar + form + camaras + menu + info + '</body>' # + str(fila_videncia.fila) + str(fila_prece.fila)

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
    return head + '<body>' + html_camaras_vid + html_camaras_pre + '<div class="nobr">' + voltar + ' ' + data + '</div></body>' + calendario

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
    if nome_fila == 'videncia':
        numero = fila_videncia.proximo_numero
        pessoa = Pessoa(numero, nome_atendido)
        try:
            fila_videncia.adicionar_pessoa(pessoa, numero)
        except Exception as exc:
            return str(exc) + voltar
        salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    elif nome_fila == 'prece':
        numero = fila_prece.proximo_numero
        pessoa = Pessoa(numero, nome_atendido)
        try:
            fila_prece.adicionar_pessoa(pessoa, numero)
        except Exception as exc:
            return str(exc) + voltar
        salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    else: 
        return 'Fila incorreta!' + voltar
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
    return '''<p>Tem certeza que deseja deletar?</p>
            <a href='/remover_atendido_confirmado'>Sim</a><a href='/' style='margin-left:20px'>Cancelar</a>'''

@app.route("/remover_atendido_confirmado")
def remover_atendido_confirmado():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == 'videncia':
        fila_videncia.remover_pessoa(numero_atendido)
        salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    elif nome_fila == 'prece':
        fila_prece.remover_pessoa(numero_atendido)
        salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route("/reposicionar_atendido")
def reposicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    moverpara = request.args.get('moverpara')
    if nome_fila == 'videncia':
        keys = fila_videncia.keys()
        indice = keys.index(numero_atendido)
        if moverpara == 'cima':
            if indice == 0:
                return 'Não é possível subir a posição do primeiro nome da lista.' + voltar
            fila_videncia.trocar_posicao(numero_atendido, keys[indice - 1])
        elif moverpara == 'baixo':
            if indice == len(keys) - 1:
                return 'Não é possível descer a posição do último nome da lista.' + voltar
            fila_videncia.trocar_posicao(numero_atendido, keys[indice + 1])
        salvar_fila(fila_videncia, ARQUIVO_FILA_VID)
    elif nome_fila == 'prece':
        keys = fila_prece.keys()
        indice = keys.index(numero_atendido)
        if moverpara == 'cima':
            if indice == 0:
                return 'Não é possível subir a posição do primeiro nome da lista.' + voltar
            fila_prece.trocar_posicao(numero_atendido, keys[indice - 1])
        elif moverpara == 'baixo':
            if indice == len(keys) - 1:
                return 'Não é possível descer a posição do último nome da lista.' + voltar
            fila_prece.trocar_posicao(numero_atendido, keys[indice + 1])
        salvar_fila(fila_prece, ARQUIVO_FILA_PRE)
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route("/editar_atendido")
def editar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == 'videncia':
        if numero_atendido in fila_videncia:
            return f'''<form action='/editar_atendido_confirmado'>
            <input type='text' name='nome_atendido' value='{fila_videncia.get(numero_atendido)}'>
            <input type='hidden' name='nome_fila' value='{nome_fila}'>
            <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
            <button type='submit'>Confirmar</button>
            </form>'''
    if nome_fila == 'prece':
        if numero_atendido in fila_prece:
            return f'''<form action='/editar_atendido_confirmado'>
            <input type='text' name='nome_atendido' value='{fila_prece.get(numero_atendido)}'>
            <input type='hidden' name='nome_fila' value='{nome_fila}'>
            <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
            <button type='submit'>Confirmar</button>
            </form>'''
    cancelar = '<a href="/">CANCELAR</a>'
    return cancelar

@app.route('/editar_atendido_confirmado')
def editar_atendido_confirmado():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == 'videncia':
        fila_videncia.editar_pessoa(numero_atendido, nome_atendido)
    elif nome_fila == 'prece':
        fila_prece.editar_pessoa(numero_atendido, nome_atendido)
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

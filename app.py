import os
from flask import Flask, request, redirect, send_from_directory
from datetime import datetime, date
import calendar  
import locale

locale.setlocale(locale.LC_ALL,'pt_BR')
    


class Pessoa:
    def __init__(self, numero, nome, chamado=0, camara=None, dupla=-1, asterisco=0):
        self.nome = nome
        self.numero = numero
        self.chamado = chamado
        self.camara = camara
        self.dupla = dupla
        self.asterisco = asterisco

    def __str__(self):
        return self.nome
     
    def csv(self):
        return f'{self.numero},{self.nome},{self.chamado},{self.camara},{self.dupla},{self.asterisco}'
    
    def nome_exibicao(self):
        if self.chamado == 1:
            return f'<s>{self.nome}</s> - {self.camara}'
        else:
            return f'{self.nome}'
        
    def __repr__(self):
        return self.nome
    
class Fila():
    def __init__(self, atividade, nome_display):
        self.atividade = atividade
        self.nome_display = nome_display
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
        pessoa = self.fila[numero]
        if pessoa.dupla != - 1:
            self.fila[pessoa.dupla].dupla = -1
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
    
    def trocar_posicao(self, n1, n2, ignorar_duplas=False):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível mover!')
        if n2 < n1:
            return self.trocar_posicao(n2, n1, ignorar_duplas)
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if ignorar_duplas == False and pessoa1.dupla != n2:
            if pessoa1.dupla != -1 and pessoa2.dupla != -1: #p1+p2 tem dupla. Se tiver dupla e se for trocar com alguem que nao é a propria dupla
                self.trocar_posicao(n1, pessoa2.dupla, ignorar_duplas=True)
                self.trocar_posicao(pessoa1.dupla, n2, ignorar_duplas=True)
            elif pessoa1.dupla != -1: #somente a p1 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n1, pessoa1.dupla, ignorar_duplas=True)
            elif pessoa2.dupla != -1: #somente a p2 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n2, pessoa2.dupla, ignorar_duplas=True)
            return 
        if pessoa1.dupla != -1:
            dupla = self.fila[pessoa1.dupla]
            dupla.dupla = n2
        if pessoa2.dupla != -1:
            dupla = self.fila[pessoa2.dupla]
            dupla.dupla = n1
        pessoa1.numero = n2
        pessoa2.numero = n1
        self.fila[n1] = pessoa2
        self.fila[n2] = pessoa1

    def keys(self):
        return sorted(self.fila.keys())
    
    def criar_dupla(self, n1, n2):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível criar dupla!')
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if pessoa1.dupla != -1 or pessoa2.dupla != -1:
            raise Exception ('Não é possível criar dupla uma pessoa de outra dupla!')
        pessoa1.dupla = n2
        pessoa2.dupla = n1

    def cancelar_dupla(self, n1):
        if n1 not in self.fila:
            raise Exception ('Não foi possível cancelar a dupla!')
        pessoa1 = self.get(n1)
        pessoa2 = self.get(pessoa1.dupla)
        pessoa1.dupla = -1
        pessoa2.dupla = -1


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
                break
        else:
            self.pessoa_em_atendimento = 'FECHADA'
            return 'CÂMARA FECHADA'
        self.pessoa_em_atendimento = pessoa
        self.pessoa_em_atendimento.camara = self.numero_camara
        self.pessoa_em_atendimento.chamado = 1
        self.numero_de_atendimentos += 1
        if self.pessoa_em_atendimento.dupla != -1:
            dupla = self.fila.get(self.pessoa_em_atendimento.dupla)
            dupla.camara = self.numero_camara
            dupla.chamado = 1
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
            numero, nome, chamado, camara, dupla, asterisco = linha.split(',')
            pessoa = Pessoa(int(numero), nome, int(chamado), camara, int(dupla), int(asterisco))
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
ARQUIVO_FILA_VIDENCIA = os.path.join(PASTA_ARQUIVOS, 'Fila-videncia.csv')
ARQUIVO_FILA_PRECE = os.path.join(PASTA_ARQUIVOS, 'Fila-prece.csv')
ARQUIVO_CAMARAS = os.path.join(PASTA_ARQUIVOS, 'Camaras-info.csv')

for arquivo in [ARQUIVO_FILA_VIDENCIA, ARQUIVO_FILA_PRECE, ARQUIVO_CAMARAS]:
    with open(arquivo, 'a+'):
        pass

# fila_videncia = ler_fila(ARQUIVO_FILA_VIDENCIA)
# fila_prece = ler_fila(ARQUIVO_FILA_PRECE)

fila_videncia = Fila('videncia', 'Vidência')
fila_prece = Fila('prece', 'Prece')

for pessoa in ler_fila(ARQUIVO_FILA_VIDENCIA):
    fila_videncia.adicionar_pessoa(pessoa, pessoa.numero)

for pessoa in ler_fila(ARQUIVO_FILA_PRECE):
    fila_prece.adicionar_pessoa(pessoa, pessoa.numero)

if fila_videncia.fila:
    fila_videncia.proximo_numero = fila_videncia.values()[-1].numero + 1
if fila_prece.fila:
    fila_prece.proximo_numero = fila_prece.values()[-1].numero + 1

camara2 = Camara("2", fila_videncia, fila_videncia.atividade)
camara4 = Camara("4", fila_videncia, fila_videncia.atividade)
camara3 = Camara("3", fila_prece, fila_prece.atividade)
camara3A = Camara("3A", fila_prece, fila_prece.atividade)

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


def gerar_html_fila(fila, nome_fila, dupla,nome_fila_dupla, numero_dupla):
    tit_lista_fila = f'<h3>FILA {fila.nome_display.upper()}</h3><h6>nome - câmara - editar - remover - subir - descer - entrar juntos</h6>'#NOME - CÂMARA - EDITAR - REMOVER - SUBIR - DESCER - ENTRAR JUNTOS
    html_fila = f'<div class="lista-{nome_fila}">' + tit_lista_fila
    for index, pessoa in enumerate(fila.values()):
        html_fila = html_fila + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=cima">
        <img alt="Reposicionar" src="/static/img/seta-cima.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=baixo">
        <img alt="Reposicionar" src="/static/img/seta-baixo.png" width="16" height="16"></a>'''
        if pessoa.dupla != -1:
            html_fila = html_fila + f'''<a class="link-dupla" href="/cancelar_dupla?numero_atendido={pessoa.numero}&nome_fila={nome_fila}">
                <img alt="dupla" src="/static/img/dupla_cancelar.png" width="16" height="16"></a>'''
            if pessoa.numero < pessoa.dupla:
                html_fila = html_fila + f'<img alt="dupla de cima" src="/static/img/dupla_cima.png" width="16" height="16">'
            else:
                html_fila = html_fila + f'<img alt="dupla de baixo" src="/static/img/dupla_baixo.png" width="16" height="16">'
        elif dupla == '1' and nome_fila_dupla == nome_fila:
            if pessoa.numero == int(numero_dupla):
                html_fila = html_fila + '<a class="link-dupla" href="/"><img alt="dupla" src="/static/img/cancelar.png" width="16" height="16"></a>'
            else:
                html_fila = html_fila + f'''<a class="link-dupla" href="/criar_dupla?nome_fila_dupla={nome_fila}&numero_atendido={pessoa.numero}&numero_dupla={numero_dupla}">
                <img alt="dupla" src="/static/img/dupla.png" width="16" height="16"></a>'''
        else:
            html_fila = html_fila + f'''<a class="link-dupla" href="/?nome_fila_dupla={nome_fila}&numero_dupla={pessoa.numero}&dupla=1">
        <img alt="dupla" src="/static/img/dupla.png" width="16" height="16"></a>'''
        if pessoa.asterisco:
            html_fila = html_fila + f'''<a class="link-asterisco" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Asterisco" src="/static/img/asterisco-selecionado.png" width="16" height="16"></a>'''
        else:
            html_fila = html_fila + f'''<a class="link-asterisco" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Asterisco" src="/static/img/asterisco.png" width="16" height="16"></a>'''
        html_fila = html_fila + '</p>'
    html_fila = html_fila + '</div>'
    return html_fila

@app.route('/')
def get_recepcao():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    tit_recep = '<div class="div-cabecalho"><div class="dc-congrega"><img alt="CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA" src="/static/img/cefp.png"></div>' + '<div class="dc-tit-principal"><h1>RECEPÇÃO DAS CÂMARAS</h1></div>' + '<div class="dc-data">' + data + '</div></div>'
    tit_adicionar = '<div class="div-adicionar-nomes"><div class="dan-tit-form"><h5>ADICIONAR NOME NA FILA</h5></div>' #div-adicionar-nomes abrindo
    form = f'''<div class="dan-form"><form action="/adicionar_atendido">
        <div  class="dan-input-nome"><input name="nome_atendido" type="text" placeholder="Digite o nome"></div>
        <div class="dan-bt-videncia-prece"><div class="bt-videncia-prece-radio"> 
        <input class="radio" type="radio" id="videncia" name="nome_fila" value="videncia" required>
        <label class="label1" for="videncia"><div class="radio-txt">VIDÊNCIA</div></label>
        <input class="radio" type="radio" id="prece" name="nome_fila" value="prece">
        <label class="label2" for="prece"><div class="radio-txt">PRECE</div></label>
        <div class="dan-bt-adicionar"><div class="dan-bt-adicionar-centro-vertical"><button>ADICIONAR</button></div></div>
        </div></div>
        </form>
        </div></div>'''
    
    espaco = '<div class="div-espaco"> </div>'
    
    tit_videncia = '<div class="tit-videncia-prece"><div class="tit-videncia"><h2>VIDÊNCIA</h2></div></div>'
    tit_prece = '<div class="tit-videncia-prece"><div class="tit-prece"><h2>PRECE</h2></div></div>'

    # CÂMARAS
    html_camaras_videncia = ''
    html_camaras_prece = ''
    for camara in dict_camaras.values():
        nome_chamado = str(camara.pessoa_em_atendimento)
        if isinstance(camara.pessoa_em_atendimento, Pessoa) and camara.pessoa_em_atendimento.dupla != -1:
            nome_chamado = nome_chamado + ' & ' + camara.fila.get(camara.pessoa_em_atendimento.dupla).nome

        html_camara = f'''<div class='camara'><p><h3>CÂMARA {camara.numero_camara}</h3></p>
        <p>ATENDENDO<br><h4>{nome_chamado}</h4></p>
        <p>ATENDIMENTOS<br>
        <a class="linkbolinhas" href="/bolinhas?modo=subtracao&numero_camara={camara.numero_camara}"><b>-</b></a>{camara.bolinhas()}
        <a class="linkbolinhas" href="/bolinhas?modo=adicao&numero_camara={camara.numero_camara}"><b>+</b></a></p>
        <p><button type="button"><a class="btcamara" href="/chamar_proximo/{camara.numero_camara}">Chamar próximo</a></button></p>
        <p><button type="button"><a class="btcamara" href="/reabrir_camara/{camara.numero_camara}">Reabrir câmara</a></button></p>
        </div>'''
        if camara.nome_fila == fila_videncia.atividade:
            html_camaras_videncia = html_camaras_videncia + html_camara
        elif camara.nome_fila == fila_prece.atividade:
            html_camaras_prece = html_camaras_prece + html_camara
    html_camaras_videncia = '<div class="camara-videncia">' + html_camaras_videncia + '</div>'
    html_camaras_prece = '<div class="camara-prece">' + html_camaras_prece + '</div>'


    # LISTAS/FILAS
    dupla = request.args.get('dupla')
    nome_fila_dupla = request.args.get('nome_fila_dupla')
    numero_dupla = request.args.get('numero_dupla')

    html_fila_videncia = gerar_html_fila(fila_videncia, fila_videncia.atividade, dupla, nome_fila_dupla, numero_dupla)
    html_fila_prece = gerar_html_fila(fila_prece, fila_prece.atividade, dupla, nome_fila_dupla, numero_dupla)

    camaras = '<div class="div-videncia-prece">' + '<div class="div-videncia">' + tit_videncia + html_camaras_videncia + html_fila_videncia + '</div>' + espaco + '<div class="div-prece">' + tit_prece + html_camaras_prece + html_fila_prece + '</div></div>' #div-videncia-prece abrindo

    # MENU
    tit_menu = '<div class="dm-tit"><h3>MENU</h3></div>'
    tv = '<div class="dm-bt-tv"><div class="vertical-center"><a href="/tv"><button>TV</button></a></div></div>'
    bt_reiniciar = '<div class="dm-bt-reiniciar"><div class="vertical-center"><a href="/reiniciar_tudo"><button>REINICAR TUDO</button></a></div></div>'
    menu = '<div class="div-menu">' + tit_menu + tv + bt_reiniciar + '</div>'

    # INFO
    tit_info = '<div class=""><h3>INFORMAÇÕES</h3></div>'
    texto = '''1. Verificar no cartão da pessoa se data da marcação é a data de hoje.<br>
    2. Adicionar o nome na fila correspondente.<br>
    3. Carimbar o cartão.<br>
    4. Pedir para sentar no lugar correto.<br>
    5. Quando a câmara chamar, clicar em 'chamar próximo' e chamar o próximo nome. O nome é riscado, a câmara que chamou fica registrada, e uma bolinha branca fica preenchida, tudo automaticamente.<br>
    6. Quando atingir o limite de atendimentos das câmaras que é representado por cinco bolinhas cheias, avisar que a câmara fechou.<br><br><br>'''
    info = '<div class="div-info">' + tit_info + texto + calendario + '</div>'

    return  head + '<body>' + tit_recep + tit_adicionar + form + camaras + menu + info + '</body>' 

@app.route('/tv')
def tv():
    head = '<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/tv.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'
    html_camaras = ''
    html_camaras_videncia = ''
    html_camaras_prece = ''
    for camara in dict_camaras.values():
        nome_chamado = str(camara.pessoa_em_atendimento)
        if isinstance(camara.pessoa_em_atendimento, Pessoa) and camara.pessoa_em_atendimento.dupla != -1:
            nome_chamado = nome_chamado + ' & ' + camara.fila.get(camara.pessoa_em_atendimento.dupla).nome
        html_camaras = f'''<div class='tv-camara'><p>CÂMARA {camara.nome_fila}<br><h1>{camara.numero_camara}</h1><br>CHAMA</p>
        <p><h2>{nome_chamado}</h2></p></div>'''.upper()
        if camara.nome_fila == fila_videncia.atividade:
            html_camaras_videncia = html_camaras_videncia + html_camaras
        elif camara.nome_fila == fila_prece.atividade:
            html_camaras_prece = html_camaras_prece + html_camaras
    html_camaras_videncia = '<div class="tv-videncia">' + html_camaras_videncia + '</div>'
    html_camaras_prece = '<div class="tv-prece">' + html_camaras_prece + '</div>'
    voltar = '<a href="/">VOLTAR</a>'
    return head + '<body>' + html_camaras_videncia + html_camaras_prece + '<div class="nobr">' + voltar + ' ' + data + '</div></body>' + calendario

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo_(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.chamar_atendido()
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    salvar_fila(fila_videncia, ARQUIVO_FILA_VIDENCIA)
    salvar_fila(fila_prece, ARQUIVO_FILA_PRECE)
    return redirect('/')

@app.route("/adicionar_atendido")
def adicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == fila_videncia.atividade:
        numero = fila_videncia.proximo_numero
        pessoa = Pessoa(numero, nome_atendido)
        try:
            fila_videncia.adicionar_pessoa(pessoa, numero)
        except Exception as exc:
            return str(exc) + voltar
        salvar_fila(fila_videncia, ARQUIVO_FILA_VIDENCIA)
    elif nome_fila == fila_prece.atividade:
        numero = fila_prece.proximo_numero
        pessoa = Pessoa(numero, nome_atendido)
        try:
            fila_prece.adicionar_pessoa(pessoa, numero)
        except Exception as exc:
            return str(exc) + voltar
        salvar_fila(fila_prece, ARQUIVO_FILA_PRECE)
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
    salvar_fila(fila_prece, ARQUIVO_FILA_PRECE)
    fila_videncia.clear()
    salvar_fila(fila_videncia, ARQUIVO_FILA_VIDENCIA)
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/remover_atendido")
def remover_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    return f'''<p>Tem certeza que deseja deletar?</p>
            <a href='/remover_atendido_confirmado?nome_fila={nome_fila}&numero_atendido={numero_atendido}'>Sim</a><a href='/' style='margin-left:20px'>Cancelar</a>'''

@app.route("/remover_atendido_confirmado")
def remover_atendido_confirmado():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila_videncia.remover_pessoa(numero_atendido)
        salvar_fila(fila_videncia, ARQUIVO_FILA_VIDENCIA)
    elif nome_fila == fila_prece.atividade:
        fila_prece.remover_pessoa(numero_atendido)
        salvar_fila(fila_prece, ARQUIVO_FILA_PRECE)
    else: 
        return 'Fila incorreta!'
    return redirect('/')

@app.route("/reposicionar_atendido")
def reposicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    mover_para = request.args.get('mover_para')
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
        arquivo_fila = ARQUIVO_FILA_VIDENCIA
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
        arquivo_fila = ARQUIVO_FILA_PRECE
    else: 
        return 'Fila incorreta!'
    keys = fila.keys()
    indice = keys.index(numero_atendido)
    if mover_para == 'cima':
        if indice == 0:
            return 'Não é possível subir a posição do primeiro nome da lista.' + voltar
        fila.trocar_posicao(numero_atendido, keys[indice - 1])
    elif mover_para == 'baixo':
        if indice == len(keys) - 1:
            return 'Não é possível descer a posição do último nome da lista.' + voltar
        fila.trocar_posicao(numero_atendido, keys[indice + 1])
    salvar_fila(fila, arquivo_fila)
    return redirect('/')

@app.route("/editar_atendido")
def editar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        if numero_atendido in fila_videncia:
            return f'''<form action='/editar_atendido_confirmado'>
            <input type='text' name='nome_atendido' value='{fila_videncia.get(numero_atendido)}'>
            <input type='hidden' name='nome_fila' value='{nome_fila}'>
            <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
            <button type='submit'>Confirmar</button>
            </form>'''
    elif nome_fila == fila_prece.atividade:
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
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
        arquivo_fila = ARQUIVO_FILA_VIDENCIA
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
        arquivo_fila = ARQUIVO_FILA_PRECE
    fila.editar_pessoa(numero_atendido, nome_atendido)
    salvar_fila(fila, arquivo_fila)

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

@app.route('/criar_dupla')
def criar_dupla():
    nome_fila_dupla = request.args.get('nome_fila_dupla')
    numero_dupla = int(request.args.get('numero_dupla'))
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila_dupla == fila_videncia.atividade:
        fila = fila_videncia
        arquivo_fila = ARQUIVO_FILA_VIDENCIA
    elif nome_fila_dupla == fila_prece.atividade:
        fila = fila_prece
        arquivo_fila = ARQUIVO_FILA_PRECE
    keys = fila.keys()
    indice = keys.index(numero_atendido)
    indice_dupla = keys.index(numero_dupla)
    if not (indice_dupla == indice + 1 or indice_dupla == indice - 1):
        return 'Não é possível criar dupla.' + voltar
    fila.criar_dupla(numero_atendido, numero_dupla)
    salvar_fila(fila, arquivo_fila)
    return redirect('/')

@app.route('/cancelar_dupla')
def cancelar_dupla():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
        arquivo_fila = ARQUIVO_FILA_VIDENCIA
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
        arquivo_fila = ARQUIVO_FILA_PRECE
    fila.cancelar_dupla(numero_atendido)
    salvar_fila(fila, arquivo_fila)
    return redirect('/')

@app.route('/asterisco')
def asterisco():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
        arquivo_fila = ARQUIVO_FILA_VIDENCIA
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
        arquivo_fila = ARQUIVO_FILA_PRECE
    pessoa = fila.get(numero_atendido)
    pessoa.asterisco = 0 if pessoa.asterisco else 1
    salvar_fila(fila, arquivo_fila)
    return redirect('/')
   


app.run(debug=True)

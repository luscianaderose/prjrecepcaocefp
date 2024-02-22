import os
from flask import Flask, request, redirect, send_from_directory
from datetime import datetime, date
import calendar  
import locale
from classes import Pessoa, Fila, Camara, salvar_camaras, ler_camaras

locale.setlocale(locale.LC_ALL,'pt_BR')
    
vazio = '§'

set_audios_notificacoes = set()

PASTA_ARQUIVOS = os.path.join(os.path.expanduser('~'), '.recepcao-camaras')
if not os.path.exists(PASTA_ARQUIVOS): 
    os.makedirs(PASTA_ARQUIVOS) 
ARQUIVO_FILA_VIDENCIA = os.path.join(PASTA_ARQUIVOS, 'Fila-videncia.csv')
ARQUIVO_FILA_PRECE = os.path.join(PASTA_ARQUIVOS, 'Fila-prece.csv')
ARQUIVO_CAMARAS = os.path.join(PASTA_ARQUIVOS, 'Camaras-info.csv')

for arquivo in [ARQUIVO_FILA_VIDENCIA, ARQUIVO_FILA_PRECE, ARQUIVO_CAMARAS]:
    with open(arquivo, 'a+'):
        pass

fila_videncia = Fila('videncia', ARQUIVO_FILA_VIDENCIA, 'Vidência')
fila_prece = Fila('prece', ARQUIVO_FILA_PRECE, 'Prece')

fila_videncia.ler_fila()
fila_prece.ler_fila()

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
    numero_camara, pessoa_em_atendimento, numero_de_atendimentos, estado = linha.split(',')
    camara = dict_camaras[numero_camara.strip()]
    camara.pessoa_em_atendimento = pessoa_em_atendimento.strip()
    camara.numero_de_atendimentos = int(numero_de_atendimentos.strip())
    camara.estado = estado.strip()


app = Flask(__name__)


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
        # EDITAR / REMOVER / REPOSICIONAR P CIMA / REPOSICIONAR P BAIXO
        html_fila = html_fila + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/trash.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=cima">
        <img alt="Reposicionar" src="/static/img/seta-cima.png" width="16" height="16"></a>
        <a class="link-reposicionar" href="/reposicionar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&mover_para=baixo">
        <img alt="Reposicionar" src="/static/img/seta-baixo.png" width="16" height="16"></a>'''
        # DUPLA / CANCELAR DUPLA
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
        # ASTERISCO
        if pessoa.asterisco:
            html_fila = html_fila + f'''<a class="link-asterisco" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Asterisco" src="/static/img/asterisco-selecionado.png" width="16" height="16"></a>'''
        else:
            html_fila = html_fila + f'''<a class="link-asterisco" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Asterisco" src="/static/img/asterisco.png" width="16" height="16"></a>'''
        # OBSERVAÇÃO
        if pessoa.observacao == vazio:
            html_fila = html_fila + f'''<a class="link-observacao" href="/observacao?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Observação" src="/static/img/observacao-cancelar.png" width="16" height="16"></a>'''
        else:
            html_fila = html_fila + f'''<a class="link-observacao" href="/observacao?nome_fila={nome_fila}&numero_atendido={pessoa.numero}&observacao={vazio}">
        <img alt="Observação" src="/static/img/observacao.png" width="16" height="16"></a>'''

        html_fila = html_fila + '</p>'

        if pessoa.observacao:
            html_fila = html_fila + f'''<form action="/observacao">
            <input type="text" name="observacao" value="{pessoa.observacao if pessoa.observacao != vazio else ''}" placeholder="Digite a observação">
            <input type="hidden" name="numero_atendido" value="{pessoa.numero}">
            <input type="hidden" name="nome_fila" value="{nome_fila}">
            <button type="submit">OK</button></form>'''

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

        # BOTÃO ABRIR CÂMARA/CHAMAR PRÓXIMO
        if camara.estado == camara.atendendo and camara.numero_de_atendimentos < 5:
            bt_camara = f'''<p><button type="button"><a class="btcamara" href="/chamar_proximo/{camara.numero_camara}">
                            Chamar próximo</a></button></p>'''
        elif camara.estado == camara.avisar:
            bt_camara = f'''<p><button type="button"><a class="btcamara" href="/avisado/{camara.numero_camara}">
                            Avisei que é o último!</a></button></p>'''
        elif camara.estado == camara.fechada:
            bt_camara = f'''<p><button type="button"><a class="btcamara" href="/abrir_camara/{camara.numero_camara}">Câmara abriu</a></button></p>'''
        elif camara.estado == camara.avisado:
            bt_camara = f'''<p><button type="button"><a class="btcamara" href="/fechar_camara/{camara.numero_camara}">
                            Câmara fechou</a></button></p>'''
        else:
            return 'Erro'

        html_camara = f'''<div class='camara'><p><h3>CÂMARA {camara.numero_camara}</h3></p>
        <p>{camara.estado}<br><h4>{nome_chamado if nome_chamado != 'None' else 'Câmara vazia'}</h4></p>
        <p>ATENDIMENTOS<br>
        <a class="linkbolinhas" href="/bolinhas?modo=subtracao&numero_camara={camara.numero_camara}"><b>-</b></a>{camara.bolinhas()}
        <a class="linkbolinhas" href="/bolinhas?modo=adicao&numero_camara={camara.numero_camara}"><b>+</b></a></p>
        {bt_camara}
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
    js_audio_notificacoes = '''
    const sleep = (ms = 0) => new Promise(resolve => setTimeout(resolve, ms));
    async function tocarNotificacoes() {
    ''' + '\n'.join([f'var audio = new Audio("/static/audio/{camara.audio}");\naudio.play();\nawait sleep(5000);' for camara in set_audios_notificacoes]) + \
    '}'
    head = f'''<head>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/tv.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
    <script>
    {js_audio_notificacoes}
    tocarNotificacoes();
    const myTimeout = setTimeout(window.location.reload.bind(window.location), 10000);
    </script>
    </head>'''
    html_camaras = ''
    html_camaras_videncia = ''
    html_camaras_prece = ''
    for camara in dict_camaras.values():
        nome_chamado = str(camara.pessoa_em_atendimento)
        if isinstance(camara.pessoa_em_atendimento, Pessoa) and camara.pessoa_em_atendimento.dupla != -1:
            nome_chamado = nome_chamado + ' & ' + camara.fila.get(camara.pessoa_em_atendimento.dupla).nome
        html_camaras = f'''<div class='tv-camara'><p>CÂMARA {camara.nome_fila}<br><h1>{camara.numero_camara}</h1><br>CHAMA</p>
        <p><h2>{nome_chamado if nome_chamado != "None" else "CÂMARA VAZIA"}</h2></p></div>'''.upper()
        if camara.nome_fila == fila_videncia.atividade:
            html_camaras_videncia = html_camaras_videncia + html_camaras
        elif camara.nome_fila == fila_prece.atividade:
            html_camaras_prece = html_camaras_prece + html_camaras
    html_camaras_videncia = '<div class="tv-videncia">' + html_camaras_videncia + '</div>'
    html_camaras_prece = '<div class="tv-prece">' + html_camaras_prece + '</div>'
    voltar = '<a href="/">VOLTAR</a>'
    set_audios_notificacoes.clear()
    return head + '<body>' + html_camaras_videncia + html_camaras_prece + '<div class="nobr">' + voltar + ' ' + data + '</div></body>' + calendario

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo:
        camara.chamar_atendido()
        set_audios_notificacoes.add(camara)
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/avisado/<numero_camara>")
def avisado(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.avisar:
        camara.estado = camara.avisado
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/fechar_camara/<numero_camara>")
def fechar_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.avisado:
        camara.estado = camara.fechada
        camara.pessoa_em_atendimento = None
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/adicionar_atendido")
def adicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    nome_atendido = request.args.get('nome_atendido')
    if not nome_atendido:
        return 'Não é possível adicionar nome vazio!' + '<br><br>' + voltar
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    else: 
        return 'Fila incorreta!' + voltar
    numero = fila.proximo_numero
    pessoa = Pessoa(numero, nome_atendido)
    try:
        fila.adicionar_pessoa(pessoa, numero)
    except Exception as exc:
        return str(exc) + voltar
    return redirect('/')

@app.route('/abrir_camara/<numero_camara>')
def abrir_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.abrir()
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
        camara.fechar()
    fila_prece.clear()
    fila_videncia.clear()
    # pra criar pessoas automaticamente
    for nome in ['josé', 'maria', 'joão', 'cláudia', 'mário', 'beatriz', 'flávia']:
        numero = fila_videncia.proximo_numero
        pessoa = Pessoa(numero, nome)
        fila_videncia.adicionar_pessoa(pessoa, numero)
        numero = fila_prece.proximo_numero
        pessoa = Pessoa(numero, nome)
        fila_prece.adicionar_pessoa(pessoa, numero)
    # fim -> pra criar pessoas automaticamente
    fila_prece.salvar_fila()
    fila_videncia.salvar_fila()
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
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    else: 
        return 'Fila incorreta!'
    fila.remover_pessoa(numero_atendido)
    return redirect('/')

@app.route("/reposicionar_atendido")
def reposicionar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    mover_para = request.args.get('mover_para')
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
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
    return redirect('/')

@app.route("/editar_atendido")
def editar_atendido():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    if numero_atendido in fila:
        pessoa = fila.get(numero_atendido)
        return f'''<form action='/editar_atendido_confirmado'>
        <input type='text' name='nome_atendido' value='{pessoa}'>
        <input type='hidden' name='nome_fila' value='{nome_fila}'>
        <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
        <button type='submit'>Confirmar</button>
        </form>''' + (f'<br><br><a href="/desriscar?numero_atendido={numero_atendido}&nome_fila={nome_fila}">DESRISCAR</a>' if pessoa.chamado else '')
    cancelar = '<a href="/">CANCELAR</a>'
    return cancelar

@app.route('/desriscar')
def desriscar():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    if numero_atendido in fila:
        pessoa = fila.get(numero_atendido)
        pessoa.chamado = 0
        pessoa.camara = None
        fila.salvar_fila()
        return redirect('/')
    return 'Não foi possível desriscar esse nome! <br><br><a href="/">VOLTAR</a>'

@app.route('/editar_atendido_confirmado')
def editar_atendido_confirmado():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    nome_atendido = request.args.get('nome_atendido')
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    fila.editar_pessoa(numero_atendido, nome_atendido)
    return redirect('/')

@app.route('/bolinhas')
def bolinhas():
    modo = request.args.get('modo')
    numero_camara = request.args.get('numero_camara')
    camara = dict_camaras.get(numero_camara)
    if modo == 'adicao' and camara.numero_de_atendimentos < 5:
        camara.numero_de_atendimentos += 1
        if camara.numero_de_atendimentos >= 5:
            camara.estado = camara.avisar
    elif modo == 'subtracao' and camara.numero_de_atendimentos > 0:
        if camara.estado != camara.atendendo:
            camara.estado = camara.atendendo
        camara.numero_de_atendimentos -= 1
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route('/criar_dupla')
def criar_dupla():
    nome_fila_dupla = request.args.get('nome_fila_dupla')
    numero_dupla = int(request.args.get('numero_dupla'))
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila_dupla == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila_dupla == fila_prece.atividade:
        fila = fila_prece
    keys = fila.keys()
    indice = keys.index(numero_atendido)
    indice_dupla = keys.index(numero_dupla)
    if not (indice_dupla == indice + 1 or indice_dupla == indice - 1):
        return 'Não é possível criar dupla.' + voltar
    fila.criar_dupla(numero_atendido, numero_dupla)
    return redirect('/')

@app.route('/cancelar_dupla')
def cancelar_dupla():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    fila.cancelar_dupla(numero_atendido)
    return redirect('/')

@app.route('/asterisco')
def asterisco():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    fila.toggle_asterisco(numero_atendido)
    return redirect('/')
   
@app.route('/observacao')
def observacao():
    nome_fila = request.args.get('nome_fila')
    numero_atendido = int(request.args.get('numero_atendido'))
    observacao = request.args.get('observacao')
    if nome_fila == fila_videncia.atividade:
        fila = fila_videncia
    elif nome_fila == fila_prece.atividade:
        fila = fila_prece
    fila.adicionar_observacao(numero_atendido, observacao)
    return redirect('/')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


app.run(debug=True)

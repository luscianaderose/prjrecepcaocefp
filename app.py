import os
from flask import Flask, request, redirect, send_from_directory
from datetime import datetime, date, timedelta
import calendar  
import locale
from classes import Pessoa, Fila, Camara, salvar_camaras, ler_camaras
import random


locale.setlocale(locale.LC_ALL,'pt_BR')
    
vazio = '§'
set_camaras_chamando = set()
set_audios_notificacoes = set()
ultima_camara_chamada = None
lista_mensagens = []
with open('static/texto/frases.txt', encoding='utf8') as f:
    for line in f.read().splitlines():lista_mensagens.append(line)
random.shuffle(lista_mensagens)
mensagem = 0
data_ultima_mensagem = datetime.now()


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
    numero_camara, pessoa_em_atendimento, numero_de_atendimentos, estado, capacidade_maxima = linha.split(',')
    camara = dict_camaras[numero_camara.strip()]
    camara.capacidade_maxima = int(capacidade_maxima.strip())
    camara.pessoa_em_atendimento = camara.fila.get(int(pessoa_em_atendimento)) if pessoa_em_atendimento else None
    camara.numero_de_atendimentos = int(numero_de_atendimentos.strip())
    camara.estado = estado.strip()


app = Flask(__name__)


# DATA E HORA
#nomes = ("SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM")
#nomes = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
nomes = ("SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO")

def get_data_hora_atual():
    dia_semana = date.today().weekday()
    data_e_hora_atuais = datetime.utcnow() + timedelta(hours=-3)
    dia_semana_usar = nomes[dia_semana]
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d %B %H:%M').upper() #('%d/%m %H:%M')
    return dia_semana_usar + ' ' + data_e_hora_em_texto

# CALENDARIO
def get_calendario():
    data_e_hora_atuais = datetime.now()
    ano = data_e_hora_atuais.year
    mes = data_e_hora_atuais.month
    return '<div class="di-calendario cor-fundo3"><pre>' + (calendar.calendar(ano, mes)) + '</pre></div>'



voltar = '<a href="/"><button>VOLTAR</button></a>'
cancelar = '<a href="/"><button>CANCELAR</button></a>'

# def janela(texto, href1, href2, bt1, bt2):
#     head = f'''<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css">
#     <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'''
#     body_inicio = '<body>'
#     texto1 = f'''<p>{texto}</p>
#         <div class="bts-janela"><a href='{href1}'>
#         <button class="btj">{bt1}</button></a><a href='{href2}' '>
#         <button class="btj">{bt2}</button></a>
#         </div>'''
#     body_fim = '</body>'
#     return head + body_inicio + texto1 + body_fim




def gerar_html_fila(fila, nome_fila, dupla,nome_fila_dupla, numero_dupla):
    tit_lista_fila = f'<p class="txt-tit2">FILA {fila.nome_display.upper()}</p>'
    html_fila = f'<div class="dvp-lista cor-{nome_fila}">' + tit_lista_fila
    for index, pessoa in enumerate(fila.values()):
        # EDITAR / REMOVER / REPOSICIONAR P CIMA / REPOSICIONAR P BAIXO
        html_fila = html_fila + f'''<p>{index + 1}. {pessoa.nome_exibicao()}
        <a class="link-editar" href="/editar_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Editar" src="/static/img/editar.png" width="16" height="16"></a>
        <a class="link-remover" href="/remover_atendido?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        <img alt="Remover" src="/static/img/lixo.png" width="16" height="16"></a>
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
        # ASTERISCO - NÃO USANDO
        # if pessoa.asterisco:
        #     html_fila = html_fila + f'''<a class="link-icone" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        # <img alt="Asterisco" src="/static/img/asterisco-selecionado.png" width="16" height="16"></a>'''
        # else:
        #     html_fila = html_fila + f'''<a class="link-icone" href="/asterisco?nome_fila={nome_fila}&numero_atendido={pessoa.numero}">
        # <img alt="Asterisco" src="/static/img/asterisco.png" width="16" height="16"></a>'''
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
    head = '''<head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>'''

    barra_cabecalho = f'''<div class="div-cabecalho">
        <div class="dc-logo"><img alt="CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA" src="/static/img/cefp.png" height="50"></div>
        <div class="dc-tit txt-tit1">RECEPÇÃO DAS CÂMARAS</div>
        <div class="dc-data">{get_data_hora_atual()}</div>
    </div>'''

    # BARRA ADICIONAR NOMES
    barra_adicionar_nomes = f'''
    <div class="div-adicionar-nomes cor-fundo2">
        <div class="dan-tit txt-tit3">
        ADICIONAR NOME NA FILA
        </div>

        <form class="dan-form" action="/adicionar_atendido">
            <input name="nome_atendido" type="text" placeholder="Digite o nome aqui">

            <div class="dan-bt-videncia-prece">
                <div class="bt-videncia-prece"><input class="radio" type="radio" id="videncia" name="nome_fila" value="videncia" required>
                    <label class="label1" for="videncia">
                        <div class="radio-txt">VIDÊNCIA
                        </div>
                    </label><input class="radio" type="radio" id="prece" name="nome_fila" value="prece">
                    <label class="label2" for="prece">
                        <div class="radio-txt">PRECE
                        </div>
                    </label>
                </div>
            </div>
            <div class="dan-bt-adicionar">
                <button>ADICIONAR</button>
            </div>
        </form>
    </div>'''
    
    tit_videncia = '<div class="dvp-tit txt-tit2 cor-videncia">CÂMARAS VIDÊNCIA</div>'
    tit_prece = '<div class="dvp-tit txt-tit2 cor-prece">CÂMARAS PRECE</div>'

    # CÂMARAS
    html_camaras_videncia = ''
    html_camaras_prece = ''
    for camara in dict_camaras.values():
        nome_chamado = str(camara.pessoa_em_atendimento)
        if isinstance(camara.pessoa_em_atendimento, Pessoa) and camara.pessoa_em_atendimento.dupla != -1:
            nome_chamado = nome_chamado + ' & ' + camara.fila.get(camara.pessoa_em_atendimento.dupla).nome

        # BOTÃO ABRIR CÂMARA/CHAMAR PRÓXIMO
        if camara.estado == camara.atendendo and camara.numero_de_atendimentos < camara.capacidade_maxima:
            bt_camara = f'''<p><button type="button"><a class="btcamara a" href="/chamar_proximo/{camara.numero_camara}">
                            CHAMAR PRÓXIMO</a></button></p>'''
        elif camara.estado == camara.avisar:
            bt_camara = f'''<p><button type="button"><a class="btcamara a" href="/avisado/{camara.numero_camara}">
                            AVISEI QUE É O ÚLTIMO!</a></button></p>'''
        elif camara.estado == camara.fechada:
            bt_camara = f'''<p><button type="button"><a class="btcamara a" href="/abrir_camara/{camara.numero_camara}">ABRIR CÂMARA</a></button></p>'''
        elif camara.estado == camara.avisado:
            bt_camara = f'''<p><button type="button"><a class="btcamara a" href="/fechar_camara/{camara.numero_camara}">
                            FECHAR CÂMARA</a></button></p>'''
        else:
            return 'Erro'

        #PARA BOTÃO NÚMERO GRANDE
        if camara.estado == camara.atendendo and camara.numero_de_atendimentos < camara.capacidade_maxima:
            bt_camara_num_gde = f'''<a style="text-decoration:none" href="/chamar_proximo/{camara.numero_camara}">'''
        elif camara.estado == camara.avisar:
            bt_camara_num_gde = f'''<a style="text-decoration:none" href="/avisado/{camara.numero_camara}">'''
        elif camara.estado == camara.fechada:
            bt_camara_num_gde = f'''<a style="text-decoration:none" href="/abrir_camara/{camara.numero_camara}">'''
        elif camara.estado == camara.avisado:
            bt_camara_num_gde = f'''<a style="text-decoration:none" href="/fechar_camara/{camara.numero_camara}">'''
        else:
            return 'Erro'


        # CADA CÂMARA / BT CHAMAR NOVAMENTE 4 LINHAS ABAIXO
        html_camara = f'''
        <div class="dvp-camara-individual cor-fundo2{" camara-chamando" if camara == ultima_camara_chamada else ""}
                                                    {" camara-avisar" if camara.estado == camara.avisar else ""}
                                                    {" camara-avisado" if camara.estado == camara.avisado else ""}
                                                    {" camara-fechada" if camara.estado == camara.fechada else ""}">
            <p>
            <div class="dvp-bt-num-gde-com-bt-cham-nov">
                {bt_camara_num_gde}
                <div class="dvp-camara-numero-grande{" cor-videncia" if camara.nome_fila == fila_videncia.atividade else " cor-prece"}">{camara.numero_camara}
                </div>
                </a>
                
                <div class="dvp-bt-chamar-novamente">
                <a class="link-icone" href="/chamar_novamente/{camara.numero_camara}">
                <img alt="Som" src="/static/img/chamar-com-som.png" width="16" height="16"></a>
                <a class="link-icone" href="/chamar_novamente_sem_som/{camara.numero_camara}">
                <img alt="Sem som" src="/static/img/chamar-sem-som.png" width="16" height="16"></a>
                </div>
            </div>
            </p>
            
            {camara.estado}<br>
            <p class="txt-destaque">{nome_chamado if nome_chamado != "None" else "CÂMARA VAZIA"}
            </p>
            <p class="atendimentos txt-pequeno">ATENDIMENTOS</p>
            <a class="linkbolinhas a" href="/bolinhas?modo=subtracao&numero_camara={camara.numero_camara}"><b>-</b></a>{camara.bolinhas()}
            <a class="linkbolinhas a" href="/bolinhas?modo=adicao&numero_camara={camara.numero_camara}"><b>+</b></a>
            {bt_camara}
        </div>'''

        if camara.nome_fila == fila_videncia.atividade:
            html_camaras_videncia = html_camaras_videncia + html_camara
        elif camara.nome_fila == fila_prece.atividade:
            html_camaras_prece = html_camaras_prece + html_camara
    html_camaras_videncia = '<div class="dvp-camara-total cor-videncia">' + html_camaras_videncia + '</div>'
    html_camaras_prece = '<div class="dvp-camara-total cor-prece">' + html_camaras_prece + '</div>'

    # FILAS / LISTAS
    dupla = request.args.get('dupla')
    nome_fila_dupla = request.args.get('nome_fila_dupla')
    numero_dupla = request.args.get('numero_dupla')

    html_fila_videncia = gerar_html_fila(fila_videncia, fila_videncia.atividade, dupla, nome_fila_dupla, numero_dupla)
    html_fila_prece = gerar_html_fila(fila_prece, fila_prece.atividade, dupla, nome_fila_dupla, numero_dupla)
    
    espaco = '<div class="div-espaco"> </div>'
    camaras = '<div class="div-videncia-prece">' + '<div class="div-videncia">' + tit_videncia + html_camaras_videncia + html_fila_videncia + '</div>' + espaco + '<div class="div-prece">' + tit_prece + html_camaras_prece + html_fila_prece + '</div></div>' #div-videncia-prece abrindo

    barra_legenda = '''<div class="legenda cor-fundo2"><p class="txt-pequeno">
    LEGENDA: NOME - CÂMARA &nbsp;&nbsp;
    BOTÕES: &nbsp;
    EDITAR &nbsp;<img alt="Editar" src="/static/img/editar.png" width="12" height="12">&nbsp;&nbsp;
    REMOVER &nbsp;<img alt="Lixeira" src="/static/img/lixo.png" width="12" height="12">&nbsp;&nbsp;
    SUBIR POSIÇÃO &nbsp;<img alt="Editar" src="/static/img/seta-cima.png" width="12" height="12">&nbsp;&nbsp;
    DESCER POSIÇÃO &nbsp;<img alt="Editar" src="/static/img/seta-baixo.png" width="12" height="12">&nbsp;&nbsp;
    CRIAR DUPLA &nbsp;<img alt="Editar" src="/static/img/dupla.png" width="14" height="14">&nbsp;&nbsp;
    OBSERVAÇÃO &nbsp;<img alt="Editar" src="/static/img/observacao.png" width="12" height="12">&nbsp;&nbsp;
    </p></div>'''

    # MENU
    tit_menu = '<p class="txt-tit2">MENU</p>'
    bt_tv = '<a href="/tv"><button>TV</button></a>'
    bt_silencio = '<a href="/silencio"><button>PEDIR SILÊNCIO</button></a>'
    bt_reiniciar = '<a href="/reiniciar_tudo"><button>REINICAR TUDO</button></a>'
    menu_deschamar = f'''
        {''.join([f'<a href="/deschamar/{num}"><button>DESCHAMAR CAM {num}</button></a>' for num in dict_camaras])}
        '''
    menu_aumentar_capacidade = f'''
        {''.join([f'<a href="/aumentar_capacidade/{num}"><button>AUMENTAR CAM {num}</button></a>' for num in dict_camaras])}
        '''
    menu_diminuir_capacidade = f'''
        {''.join([f'<a href="/diminuir_capacidade/{num}"><button>DIMINUIR CAM {num}</button></a>' for num in dict_camaras])}
        '''
    menu1 = '<div class="div-menu cor-fundo2">' + bt_tv + bt_silencio +  bt_reiniciar + '</div>'
    menu2 = '<div class="div-menu cor-fundo2">' + menu_deschamar + '</div>'
    menu3 = '<div class="div-menu cor-fundo2">' + menu_aumentar_capacidade + '</div>'
    menu4 = '<div class="div-menu cor-fundo2">' + menu_diminuir_capacidade + '</div>'
    menu = '<div class="div-menu-todo cor-fundo2">' + tit_menu + menu1 + menu2 + menu3 + menu4 + '</div>'

    # INFO
    tit_info = '<p class="txt-tit2">INFORMAÇÕES</p>'
    texto = '''
    <p class="txt-tit3">ROTINA DA RECEPÇÃO DAS CÂMARAS</p><ol>
    <li>Verificar no comprovante de agendamento da pessoa se data da marcação é a data de hoje.</li>
    <li>Digitar o nome, escolher a fila correspondente (prece ou vidência) e clicar em 'ADICIONAR'.</li>
    <li>Carimbar o comprovante.</li>
    <li>Anotar o número da ordem de chegada no comprovante.</li>
    <li>Devolver o comprovante para a pessoa.</li>
    <li>Pedir para se sentar segurando o comprovante em mãos.</li>
    <li>Quando a câmara chamar, clicar no botão 'CHAMAR PRÓXIMO' ou na bola com número da câmara.</li>
    <li>Automaticamente o nome anterior é riscado na lista, a câmara que chamou fica registrada ao lado do nome na lista, uma bolinha vazia fica preenchida e um áudio é tocado avisando que a câmara está chamando.</li>
    <li>Chamar o próximo pelo nome da pessoa. Mostrar à pessoa onde é a câmara.</li>
    <li>Nas sextas-feiras, normalmente cada câmara atende 5 pessoas. Quando 5 bolinhas forem preenchidas, é hora de avisar a câmara que é a última.</li>
    <li>Se comparecerem menos de 10 pessoas em uma lista, tente dividir igualmente entre as câmaras. Por exemplo, se comparecerem apenas 8 pessoas para cada câmara de uma lista, direcione 4 para cada câmara para distribuir o trabalho igualmente.</li>
    <li>Ao entrar a última pessoa da câmara, avisar ao secretário da câmara que é a última pessoa a ser atendida para que a câmara possa fazer depois dela o processo de encerramento.</li>
    <li>Leia um trecho do Evangelho às 18:50. Falar a saudação da casa antes e depois (Graças a Deus, a Jesus e a Francisco de Paula). Se quiser pode rezar o Pai Nosso. Fale os seguintes avisos: silêncio, desligar os celulares, comprovante em mãos, pode pegar um livro do balcão para ler enquanto espera.</li></ol>

    <p class="txt-tit3">REPETIR CHAMADO COM OU SEM SOM</p><ul>
    <li>Clique em <img alt="chamar com som" src="/static/img/chamar-com-som.png" width="12" height="12"> para repetir o chamado com som.</li>
    <li>Clique em <img alt="chamar sem som" src="/static/img/chamar-sem-som.png" width="12" height="12"> para repetir o chamado sem som, fazendo apenas o destaque visual.</li></ul>
    
    <p class="txt-tit3">NOMES QUE ENTRAM JUNTOS NA CÂMARA – CRIAÇÃO DE DUPLA</p><ol>
    <li>Na lista de nomes da fila, clique no botão CRIAR DUPLA <img alt="dupla" src="/static/img/dupla.png" width="16" height="16"> ao lado do nome que formará dupla.</li>
    <li>Este ícone se tornará um <img alt="x" src="/static/img/cancelar.png" width="16" height="16">. Caso queira cancelar a ação, clique neste <img alt="dupla" src="/static/img/cancelar.png" width="16" height="16">.</li>
    <li>Agora clique no botão CRIAÇÃO DE DUPLA <img alt="dupla" src="/static/img/dupla.png" width="16" height="16"> ao lado do nome que entrará na câmara junto. Pronto!.</li>
    <li>Se quiser desfazer, clique no botão DESFAZER DUPLA <img alt="cancelar dupla" src="/static/img/dupla_cancelar.png" width="16" height="16">.</li></ol><br><br>'''

    info = '<div class="div-info cor-fundo2">' + tit_info + texto + get_calendario() + '</div>'

    # OUTROS
    tit_outros = '<div class="div-outros cor-fundo2"><p = class="txt-tit2">OUTROS</p>'
    bt_outros = '<a href="/outros"><button>OUTROS</button></a></div>'
    barra_outros = tit_outros + bt_outros

    return  head + '<body>' + barra_cabecalho + barra_adicionar_nomes + camaras + barra_legenda + menu + info + barra_outros + '</body>' 

@app.route('/tv')
def tv():
    js_audios_notificacoes = [f'var audio = new Audio("/static/audio/{camara.audio}");\naudio.play();\nawait sleep(5000);' for camara in set_camaras_chamando]
    if not js_audios_notificacoes:
        js_audios_notificacoes = [f'var audio = new Audio("/static/audio/{audio}");\naudio.play();\nawait sleep(7000);' for audio in set_audios_notificacoes]
    head = f'''<head>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/tv.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
    <script>
    const sleep = (ms = 0) => new Promise(resolve => setTimeout(resolve, ms));
    async function tocarNotificacoes() {{
    {' '.join(js_audios_notificacoes)}
    }}
    tocarNotificacoes();
    const myTimeout = setTimeout(window.location.reload.bind(window.location), {'2000' if not js_audios_notificacoes else '10000'});
    </script>
    </head>'''
    html_camaras = ''
    html_camaras_videncia = ''
    html_camaras_prece = ''

    # O QUE APARECE EM CADA CÂMARA NA TELA DA TV
    for camara in dict_camaras.values():
        nome_chamado = str(camara.pessoa_em_atendimento)
        if isinstance(camara.pessoa_em_atendimento, Pessoa) and camara.pessoa_em_atendimento.dupla != -1:
            nome_chamado = nome_chamado + ' & ' + camara.fila.get(camara.pessoa_em_atendimento.dupla).nome
        nome_atendido = f'{camara.fila.get_posicao(camara.pessoa_em_atendimento.numero)}. {nome_chamado} {"- " + camara.estado if camara.estado == camara.avisar else ""}' if nome_chamado != "None" else "FECHADA"
        html_camaras = f'''<div class='tv-camara{' camara-chamando' if camara == ultima_camara_chamada else ''}
            {" camara-avisar" if camara.estado == camara.avisar else ""}
            {" camara-avisado" if camara.estado == camara.avisado else ""}
            {" camara-fechada" if camara.estado == camara.fechada else ""}'><p>
        <div class="tv-camara-fonte-num-camara"><h1>{camara.numero_camara}</h1></div>
        <h2>CÂMARA {camara.fila.nome_display}<h2>
        <p><h2>{nome_atendido}</h2></p></div>'''.upper()
        if camara.nome_fila == fila_videncia.atividade:
            html_camaras_videncia = html_camaras_videncia + html_camaras
        elif camara.nome_fila == fila_prece.atividade:
            html_camaras_prece = html_camaras_prece + html_camaras
    # FIM: O QUE APARECE EM CADA CÂMARA NA TELA DA TV
            
    html_camaras_videncia = '<div class="tv-videncia">' + html_camaras_videncia + '</div>'
    html_camaras_prece = '<div class="tv-prece">' + html_camaras_prece + '</div>'
    set_camaras_chamando.clear()
    set_audios_notificacoes.clear()
    data = f'<div class="tv-data">{get_data_hora_atual()}</div>'
    barra_cabecalho = f'<div class="tv-cabecalho cor-fundo2">RECEPÇÃO DAS CÂMARAS {data}</div>'
    global mensagem
    global data_ultima_mensagem
    barra_mensagem = f'<div class="tv-mensagem"><p class="txt-3">{lista_mensagens[mensagem]}</p></div>'
    if datetime.now() >= data_ultima_mensagem + timedelta(minutes=1):
        data_ultima_mensagem = datetime.now()
        mensagem += 1
        if mensagem >= len(lista_mensagens):
            mensagem = 0
    divs_videncia_prece = f'<div class="tv-videncia-prece">{html_camaras_videncia + html_camaras_prece}</div>'
    avisos = f'''<div class="tv-avisos"> 1.SILÊNCIO! &nbsp2.COMPROVANTE EM MÃOS &nbsp3.DESLIGUEM OS CELULARES &nbsp4.LEIA UM LIVRO DO BALCÃO</div>'''
    return head + '<body>' + barra_cabecalho + barra_mensagem + divs_videncia_prece + avisos + '</body><br><br><br><br>' + voltar

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo:
        camara.chamar_atendido()
        set_camaras_chamando.add(camara)
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
        global ultima_camara_chamada
        ultima_camara_chamada = camara
    return redirect('/')

@app.route("/chamar_novamente/<numero_camara>")
def chamar_novamente(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo or camara.estado == camara.avisar:
        set_camaras_chamando.add(camara)
        global ultima_camara_chamada
        ultima_camara_chamada = camara
    return redirect('/')

@app.route("/chamar_novamente_sem_som/<numero_camara>")
def chamar_novamente_sem_som(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo or camara.estado == camara.avisar:
        global ultima_camara_chamada
        ultima_camara_chamada = camara
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
    nome_atendido = request.args.get('nome_atendido').upper()
    # if not nome_atendido:
    #     return 'Não é possível adicionar nome vazio!' + '<br><br>' + voltar
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
        camara.capacidade_maxima = 5
    fila_prece.clear()
    fila_videncia.clear()
    # pra criar pessoas automaticamente
    for nome in ['JOSÉ', 'MARIA', 'JOÃO', 'CLÁUDIA', 'MÁRIO', 'BEATRIZ', 'FLÁVIA']:
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
    ### JANELA ###
    return f'''
    <head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>
    <body>
    <p>Tem certeza que deseja deletar?</p>
        <div class="bts-janela"><a href='/remover_atendido_confirmado?nome_fila={nome_fila}&numero_atendido={numero_atendido}'><button class="btj">Sim</button></a><a href='/' '><button class="btj">Cancelar</button></a>
        </div>
    </body>'''


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
        ### JANELA ###
        return f'''
        <head><link rel="stylesheet" href="/static/css/style.css"><link rel="stylesheet" href="/static/css/recepcao.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto"></head>
        <body>
        <p>Deseja editar o nome?</p>
            <form action='/editar_atendido_confirmado'>
            <input type='text' name='nome_atendido' value='{pessoa}'>
            <input type='hidden' name='nome_fila' value='{nome_fila}'>
            <input type='hidden' name='numero_atendido' value='{numero_atendido}'>
            <button type='submit'>Confirmar</button>
            </form>''' + (f'''<br>
                            <p>Deseja desriscar o nome?</p>
                            <a href="/desriscar?numero_atendido={numero_atendido}&nome_fila={nome_fila}">
                            <button>DESRISCAR</button></a>''' if pessoa.estado == pessoa.riscado else '') + '</body>'
    return cancelar + voltar

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
        pessoa.estado = pessoa.aguardando
        pessoa.camara = None
        if pessoa.dupla != -1:
            dupla = fila.get(pessoa.dupla)
            dupla.estado = dupla.aguardando
            dupla.camara = None
        fila.salvar_fila()
        return redirect('/')
    ### JANELA ###
    return 'Não foi possível desriscar esse nome!<br><a href="/">' + voltar

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
    if modo == 'adicao' and camara.numero_de_atendimentos < camara.capacidade_maxima:
        camara.numero_de_atendimentos += 1
        if camara.numero_de_atendimentos >= camara.capacidade_maxima:
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
    try: fila.criar_dupla(numero_atendido, numero_dupla)
    except Exception as exc: return str(exc) + '<br><br>' + voltar
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

@app.route('/silencio')
def silencio():
    set_audios_notificacoes.add('celulares_silencio.mp3')
    return redirect('/')

@app.route("/deschamar/<numero_camara>")
def deschamar(numero_camara):
    camara = dict_camaras[numero_camara]
    if not camara.pessoa_em_atendimento:
        return f'A câmara {numero_camara} não está atendendo ninguém.'
    pessoa = camara.pessoa_em_atendimento
    pessoa.estado = pessoa.aguardando
    pessoa.camara = None
    if pessoa.dupla != -1:
        dupla = camara.fila.get(pessoa.dupla)
        dupla.estado = dupla.aguardando
        dupla.camara = None
    for pessoa in camara.fila.values()[::-1]:
        if pessoa.estado == pessoa.riscado and pessoa.camara == numero_camara:
            pessoa.estado = pessoa.atendendo
            if pessoa.dupla != -1:
                dupla = camara.fila.get(pessoa.dupla)
                dupla.estado = dupla.atendendo
            camara.pessoa_em_atendimento = pessoa
            break
    else:
        camara.pessoa_em_atendimento = None
    camara.numero_de_atendimentos -= 1
    camara.estado = camara.atendendo
    camara.fila.salvar_fila()
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/aumentar_capacidade/<numero_camara>")
def aumentar_capacidade(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.capacidade_maxima < 20:
        camara.capacidade_maxima += 1
        if camara.estado != camara.atendendo and camara.numero_de_atendimentos > 0:
            camara.estado = camara.atendendo
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route("/diminuir_capacidade/<numero_camara>")
def diminuir_capacidade(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.capacidade_maxima > 3:
        camara.capacidade_maxima -= 1
        if camara.estado == camara.atendendo and camara.numero_de_atendimentos >= camara.capacidade_maxima:
            camara.estado = camara.avisar
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return redirect('/')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/outros')
def outros():
    head = f'''<head>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/recepcao.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
    </head>'''
    data = f'{get_data_hora_atual()}'
    texto = '''
    <p class="txt-tit1">TÍTULO 1</p>
    <p class="txt-tit2">TÍTULO 2</p>
    <p class="txt-tit3">TÍTULO 3</p>
    <p class="txt-tit4">TÍTULO 4</p>
    <p class="txt-destaque">texto destaque texto texto texto texto</p>
    <p class="txt-normal">texto normal texto texto texto texto</p>
    <p class="txt-2">texto 2 texto texto texto texto</p>
    <p class="txt-pequeno">texto pequeno texto texto texto texto</p>

    '''
    return head + '<body>' + data + texto + voltar + '</body>'



app.run(debug=True, host='0.0.0.0')

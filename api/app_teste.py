import os
import random
import locale
import calendar  
from flask import Flask, request, redirect, send_from_directory, jsonify
from flask_cors import CORS
from datetime import datetime, date, timedelta
from pessoa import Pessoa
from fila import Fila
from camara import Camara, salvar_camaras, ler_camaras
from info import texto_recepcao


locale.setlocale(locale.LC_ALL,'pt_BR')


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

set_camaras_chamando = set()
set_audios_notificacoes = set()

# DATA E HORA
# nomes = ("SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM")
# nomes = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
nomes = ("SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO")

def get_data_hora_atual():
    dia_semana = date.today().weekday()
    data_e_hora_atuais = datetime.utcnow() + timedelta(hours=-3)
    dia_semana_usar = nomes[dia_semana]
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d %B %H:%M').upper() #('%d/%m %H:%M')
    return dia_semana_usar + ' ' + data_e_hora_em_texto

def get_calendario():
    data_e_hora_atuais = datetime.now()
    ano = data_e_hora_atuais.year
    mes = data_e_hora_atuais.month
    return calendar.calendar(ano, mes)


app=Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return {
        "mensagem": "página inicial"
    }

@app.route("/calendario")
def calendario():
    return {
        "data_e_hora": get_data_hora_atual(),
        "calendario": get_calendario()
    }

@app.route("/camaras")
def camaras():
    return jsonify([camara.to_dict() for camara in dict_camaras.values()])

# lista_de_camaras = [camara.to_dict() for camara in dict_camaras.values()]

# camaras = []

# print(camaras)

# for camara in dict_camaras.values():
#     camaras.append(camara.to_dict())
    # print(camara.to_dict())

# print(lista_de_camaras)

    # return {
    #     "camaras": jsonify([camara.to_dict() for camara in dict_camaras.values()])
    # }

# print(dict_camaras["3"].to_dict())

@app.route('/camara', methods=['POST'])
def apertou_botao():
    data = request.json
    numero_camara = data.get('numero')
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo:
        camara.chamar_atendido()
        # set_camaras_chamando.add(camara)
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
        global ultima_camara_chamada
        ultima_camara_chamada = camara
    return jsonify({'message': f'Camara: {numero_camara}'})

@app.route('/abrir_camara/<numero_camara>')
def abrir_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    camara.abrir()
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "camara aberta"

@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.atendendo:
        camara.chamar_atendido()
        set_camaras_chamando.add(camara)
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
        global ultima_camara_chamada
        ultima_camara_chamada = camara
    return "chamar próximo"

@app.route("/avisado/<numero_camara>")
def avisado(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.avisar:
        camara.estado = camara.avisado
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "avisado"

@app.route("/fechar_camara/<numero_camara>")
def fechar_camara(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.estado == camara.avisado:
        camara.estado = camara.fechada
        camara.pessoa_em_atendimento = None
        salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "fechar camara"

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
    return "bolinhas atualizadas"

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
    return "deschamado"

@app.route("/aumentar_capacidade/<numero_camara>")
def aumentar_capacidade(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.capacidade_maxima < 20:
        camara.capacidade_maxima += 1
        if camara.estado != camara.atendendo and camara.numero_de_atendimentos > 0:
            camara.estado = camara.atendendo
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "aumentando"

@app.route("/diminuir_capacidade/<numero_camara>")
def diminuir_capacidade(numero_camara):
    camara = dict_camaras[numero_camara]
    if camara.capacidade_maxima > 3:
        camara.capacidade_maxima -= 1
        if camara.estado == camara.atendendo and camara.numero_de_atendimentos >= camara.capacidade_maxima:
            camara.estado = camara.avisar
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "diminuindo"

@app.route('/reiniciar_tudo_confirmado')
def reiniciar_tudo_confirmado():
    for camara in dict_camaras.values():
        camara.numero_de_atendimentos = 0
        camara.fechar()
        camara.capacidade_maxima = 5
    fila_prece.clear()
    fila_videncia.clear()
    # # pra criar pessoas automaticamente
    # for nome in ['JOSÉ', 'MARIA', 'JOÃO', 'CLÁUDIA', 'MÁRIO', 'BEATRIZ', 'FLÁVIA']:
    #     numero = fila_videncia.proximo_numero
    #     pessoa = Pessoa(numero, nome)
    #     fila_videncia.adicionar_pessoa(pessoa, numero)
    #     numero = fila_prece.proximo_numero
    #     pessoa = Pessoa(numero, nome)
    #     fila_prece.adicionar_pessoa(pessoa, numero)
    # # fim -> pra criar pessoas automaticamente
    fila_prece.salvar_fila()
    fila_videncia.salvar_fila()
    salvar_camaras(dict_camaras, ARQUIVO_CAMARAS)
    return "reiniciado"


@app.route('/fila_videncia')
def fun_fila_videncia():
    return fila_videncia

print(fila_videncia)

# app.run(debug=True, host="0.0.0.0", port=5001)
from db import FilaModel, CamaraModel, PessoaModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship


engine = create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine)
session = Session()

fila_videncia = FilaModel(
    id=1,
    nome="Fila Vidência",
    atividade="videncia",
    proximo_numero=1,
)

fila_prece = FilaModel(
    id=2,
    nome="Fila Prece",
    atividade="prece",
    proximo_numero=1,
)

camara2 = CamaraModel(
    id=1,
    nome="Câmara 2",
    numero_de_atendimentos=0,
    estado="fechada",
    capacidade_maxima=5,
    fila=fila_videncia,
    pessoa_em_atendimento=None,
)

camara4 = CamaraModel(
    id=2,
    nome="Câmara 4",
    numero_de_atendimentos=0,
    estado="fechada",
    capacidade_maxima=5,
    fila=fila_videncia,
    pessoa_em_atendimento=None,
)

camara3 = CamaraModel(
    id=3,
    nome="Câmara 3",
    numero_de_atendimentos=0,
    estado="fechada",
    capacidade_maxima=5,
    fila=fila_prece,
    pessoa_em_atendimento=None,
)

camara3a = CamaraModel(
    id=4,
    nome="Câmara 3A",
    numero_de_atendimentos=0,
    estado="fechada",
    capacidade_maxima=5,
    fila=fila_prece,
    pessoa_em_atendimento=None,
)


session.add(fila_videncia)
session.add(fila_prece)
session.add(camara2)
session.add(camara4)
session.add(camara3)
session.add(camara3a)
for numero, nome in enumerate(['JOSÉ', 'MARIA', 'JOÃO', 'CLÁUDIA', 'MÁRIO', 'BEATRIZ', 'FLÁVIA']):
    pessoa = PessoaModel(
        id=numero,
        nome=nome,
        numero=numero,
        estado="aguardando",
        fila=fila_videncia,
        camara_id=None,
        dupla_id=None,
        observacao="",
    )
    session.add(pessoa)
session.commit()
session.close()


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FilaModel(Base):
    __tablename__='fila'
    id=Column(Integer, primary_key=True)
    nome=Column(String)
    atividade=Column(String)
    proximo_numero=Column(Integer)
    camara=relationship('CamaraModel', back_populates='fila')
    camara=relationship('PessoaModel', back_populates='fila')


class CamaraModel(Base):
    __tablename__='camara'
    id=Column(Integer, primary_key=True)
    nome=Column(String)
    numero_de_atendimentos=Column(Integer)
    estado=Column(String)
    capacidade_maxima=Column(Integer)
    fila_id=Column(Integer, ForeignKey('fila.id'))
    fila=relationship('FilaModel', back_populates='camara')
    pessoa_em_atendimento=Column(Integer, ForeignKey('pessoa.id'), unique=True)
    pessoa=relationship('PessoaModel', back_populates='camara', uselist=False)

class PessoaModel(Base):
    __tablename__='pessoa'
    id=Column(Integer, primary_key=True)
    nome=Column(String)
    numero=Column(Integer)
    estado=Column(String)
    fila_id=Column(Integer, ForeignKey('fila.id'))
    fila=relationship('FilaModel', back_populates='pessoa')
    camara_id=Column(Integer, ForeignKey('camara.id'))
    camara=relationship('CamaraModel', back_populates='pessoa')
    dupla_id=Column(Integer, ForeignKey('pessoa.id'))
    dupla=relationship('PessoaModel', remote_side=[id], backref='duplas')
    observacao=Column(String)


if __name__ == '__main__':
    engine = create_engine("sqlite:///db.sqlite3")
    FilaModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()
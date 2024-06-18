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
    camara=relationship('CamaraModel')
    pessoa=relationship('PessoaModel')

class CamaraModel(Base):
    __tablename__='camara'
    id=Column(Integer, primary_key=True)
    nome=Column(String)
    numero_de_atendimentos=Column(Integer)
    estado=Column(String)
    capacidade_maxima=Column(Integer)
    fila_id=Column(Integer, ForeignKey('fila.id'))
    pessoa_em_atendimento=Column(Integer, nullable=True)
    fila=relationship('FilaModel', back_populates='camara')
    pessoa=relationship('PessoaModel')

class PessoaModel(Base):
    __tablename__='pessoa'
    id=Column(Integer, primary_key=True)
    nome=Column(String)
    numero=Column(Integer)
    estado=Column(String)
    fila_id=Column(Integer, ForeignKey('fila.id'))
    camara_id=Column(Integer, ForeignKey('camara.id'), nullable=True)
    dupla_id=Column(Integer, ForeignKey('pessoa.id'), nullable=True)
    observacao=Column(String)
    fila=relationship('FilaModel', back_populates='pessoa')
    camara=relationship('CamaraModel', back_populates='pessoa')
    dupla=relationship('PessoaModel', remote_side=[id], backref='duplas')

if __name__ == '__main__':
    engine = create_engine("sqlite:///db.sqlite3")
    FilaModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()

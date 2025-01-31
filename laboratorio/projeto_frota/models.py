# models.py
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Equipamento(Base):
    __tablename__ = 'equipamento'
    
    id = Column(Integer, primary_key=True)
    modelo_versao = Column(String(100))
    usuario = Column(String(100))
    classe = Column(String(50))
    medidor = Column(String(10))  # H, KM/H ou IND
    data_registro = Column(DateTime, default=datetime.now)

    # Relacionamentos
    usos = relationship("FatoUso", back_populates="equipamento", cascade="all, delete-orphan")
    custos = relationship("FatoCustoOperacional", back_populates="equipamento", cascade="all, delete-orphan")
    combustiveis = relationship("FatoCombustivel", back_populates="equipamento", cascade="all, delete-orphan")
    manutencoes = relationship("FatoManutencao", back_populates="equipamento", cascade="all, delete-orphan")

class FatoUso(Base):
    __tablename__ = 'fato_uso'
    
    id = Column(Integer, primary_key=True)
    equipamento_id = Column(Integer, ForeignKey('equipamento.id'))
    uso_estimado = Column(Float)
    uso_realizado = Column(Float)
    uso_diferenca = Column(Float)
    data_registro = Column(DateTime, default=datetime.now)
    
    equipamento = relationship("Equipamento", back_populates="usos")

class FatoCustoOperacional(Base):
    __tablename__ = 'fato_custo_operacional'
    
    id = Column(Integer, primary_key=True)
    equipamento_id = Column(Integer, ForeignKey('equipamento.id'))
    custo_km_orcado = Column(Float)
    custo_km_realizado = Column(Float)
    custo_km_diferenca = Column(Float)
    total_orcado = Column(Float)
    total_realizado = Column(Float)
    total_diferenca = Column(Float)
    data_registro = Column(DateTime, default=datetime.now)
    
    equipamento = relationship("Equipamento", back_populates="custos")

class FatoCombustivel(Base):
    __tablename__ = 'fato_combustivel'
    
    id = Column(Integer, primary_key=True)
    equipamento_id = Column(Integer, ForeignKey('equipamento.id'))
    volume_orcado = Column(Float)
    volume_realizado = Column(Float)
    volume_diferenca = Column(Float)
    vu_orcado = Column(Float)
    vu_realizado = Column(Float)
    vu_diferenca = Column(Float)
    total_orcado = Column(Float)
    total_realizado = Column(Float)
    total_diferenca = Column(Float)
    data_registro = Column(DateTime, default=datetime.now)
    
    equipamento = relationship("Equipamento", back_populates="combustiveis")

class FatoManutencao(Base):
    __tablename__ = 'fato_manutencao'
    
    id = Column(Integer, primary_key=True)
    equipamento_id = Column(Integer, ForeignKey('equipamento.id'))
    lubrificantes_orcado = Column(Float)
    lubrificantes_realizado = Column(Float)
    lubrificantes_diferenca = Column(Float)
    filtros_orcado = Column(Float)
    filtros_realizado = Column(Float)
    filtros_diferenca = Column(Float)
    graxas_orcado = Column(Float)
    graxas_realizado = Column(Float)
    graxas_diferenca = Column(Float)
    pecas_servicos_orcado = Column(Float)
    pecas_servicos_realizado = Column(Float)
    pecas_servicos_diferenca = Column(Float)
    reforma_orcado = Column(Float)
    reforma_realizado = Column(Float)
    reforma_diferenca = Column(Float)
    data_registro = Column(DateTime, default=datetime.now)
    
    equipamento = relationship("Equipamento", back_populates="manutencoes")
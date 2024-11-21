from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP, Text
from app.api.database import Base

class Transaction(Base):
    __tablename__ = "transactions_sample"  # estava correto, é transactions_sample mesmo

    id = Column(Integer, primary_key=True)
    DataFatura = Column(TIMESTAMP)
    PrecoUnitario = Column(Numeric)
    IDCliente = Column(String)
    Pais = Column(String)
    CategoriaProduto = Column(String)
    CategoriaPreco = Column(String)
    ValorTotalFatura = Column(Numeric)
    FaturaUnica = Column(Boolean)
    Ano = Column(Integer)
    Mes = Column(Integer)
    Dia = Column(Integer)
    DiaSemana = Column(Integer)
    created_at = Column(TIMESTAMP)
    NumeroFatura = Column(String)
    CodigoProduto = Column(String)
    Descricao = Column(Text)
    Quantidade = Column(Integer)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    DataFatura: datetime
    PrecoUnitario: Decimal
    IDCliente: str
    Pais: str
    CategoriaProduto: str
    CategoriaPreco: str
    ValorTotalFatura: Decimal
    FaturaUnica: bool
    Ano: int
    Mes: int
    Dia: int
    DiaSemana: int
    NumeroFatura: str
    CodigoProduto: str
    Descricao: str
    Quantidade: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

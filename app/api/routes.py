from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Numeric
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.api.database import get_db
from app.api.models import Transaction
from app.api.schemas import (
    Transaction as TransactionSchema,
    SummaryResponse,
    CategorySummary,
    CountrySummary
)

router = APIRouter()

@router.get("/transactions/", response_model=List[TransactionSchema])
def read_transactions(
    skip: int = 0, 
    limit: int = 100,
    pais: Optional[str] = None,
    categoria: Optional[str] = None,
    data_inicio: date = Query(
        default=date(2011, 1, 4),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    data_fim: date = Query(
        default=date(2011, 12, 31),
        ge=date(2011, 1, 4),
        le=date(2011, 12, 31)
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if pais:
        query = query.filter(Transaction.Pais == pais)
    if categoria:
        query = query.filter(Transaction.CategoriaProduto == categoria)
    if data_inicio:
        query = query.filter(Transaction.DataFatura >= data_inicio)
    if data_fim:
        query = query.filter(Transaction.DataFatura <= data_fim)
    
    transactions = query.offset(skip).limit(limit).all()
    return transactions

@router.get("/transactions/summary", response_model=SummaryResponse)
def get_transactions_summary(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    result = db.query(
        func.count(Transaction.id).label('total_transactions'),
        func.sum(Transaction.ValorTotalFatura).label('total_value'),
        func.count(Transaction.IDCliente.distinct()).label('unique_customers'),
        func.sum(Transaction.Quantidade).label('total_quantity'),
        func.avg(Transaction.PrecoUnitario).label('average_unit_price'),
        func.count(Transaction.Pais.distinct()).label('unique_countries'),
        func.count(Transaction.CategoriaProduto.distinct()).label('unique_categories')
    ).filter(
        Transaction.DataFatura >= data_inicio,
        Transaction.DataFatura <= data_fim
    ).first()
    
    return {
        "total_transactions": result.total_transactions,
        "total_value": result.total_value or Decimal('0'),
        "unique_customers": result.unique_customers,
        "total_quantity": result.total_quantity,
        "average_unit_price": result.average_unit_price or Decimal('0'),
        "unique_countries": result.unique_countries,
        "unique_categories": result.unique_categories
    }

@router.get("/transactions/by-category", response_model=List[CategorySummary])
def get_transactions_by_category(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    categories = db.query(
        Transaction.CategoriaProduto.label('categoria'),
        func.count(Transaction.id).label('total_vendas'),
        func.sum(Transaction.ValorTotalFatura).label('valor_total'),
        func.sum(Transaction.Quantidade).label('quantidade_total'),
        (func.sum(Transaction.ValorTotalFatura) / 
         func.cast(func.count(Transaction.id), Numeric)).label('ticket_medio')
    ).filter(
        Transaction.DataFatura >= data_inicio,
        Transaction.DataFatura <= data_fim
    ).group_by(Transaction.CategoriaProduto).all()
    
    return categories

@router.get("/transactions/by-country", response_model=List[CountrySummary])
def get_transactions_by_country(
    data_inicio: date = Query(default=date(2011, 1, 4)),
    data_fim: date = Query(default=date(2011, 12, 31)),
    db: Session = Depends(get_db)
):
    countries = db.query(
        Transaction.Pais.label('pais'),
        func.count(Transaction.id).label('total_vendas'),
        func.sum(Transaction.ValorTotalFatura).label('valor_total'),
        func.count(Transaction.IDCliente.distinct()).label('quantidade_clientes'),
        (func.sum(Transaction.ValorTotalFatura) / 
         func.cast(func.count(Transaction.id), Numeric)).label('ticket_medio')
    ).filter(
        Transaction.DataFatura >= data_inicio,
        Transaction.DataFatura <= data_fim
    ).group_by(Transaction.Pais).all()
    
    return countries

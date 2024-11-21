from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Transações",
    description="API para análise de dados de transações comerciais",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API de Transações!",
        "docs": "/docs",
        "endpoints": {
            "transactions": "/api/transactions/",
            "summary": "/api/transactions/summary",
            "by_category": "/api/transactions/by-category",
            "by_country": "/api/transactions/by-country"
        }
    }

# Incluir as rotas
app.include_router(router, prefix="/api")

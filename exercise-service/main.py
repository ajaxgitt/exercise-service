from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from .router import problems

app = FastAPI(
    title="Exercice Service"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]

#hlii
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(problems)


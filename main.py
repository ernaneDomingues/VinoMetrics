from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter
from requests import Session
from modules import comercio, producao, processamento, importacao, exportacao
from modules.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_db

app = FastAPI(
    title="API EMBRAPA",
    description="API para gerenciar Produção, Processamento, Comercialização, Importação e Exportação.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Mount static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load routes
app.include_router(comercio.router, prefix="/comercio", tags=["Comércio"], dependencies=[Depends(oauth2_scheme)])
app.include_router(producao.router, prefix="/producao", tags=["Produção"])
app.include_router(processamento.router, prefix="/processamento", tags=["Processamento"])
app.include_router(importacao.router, prefix="/importacao", tags=["Importação"])
app.include_router(exportacao.router, prefix="/exportacao", tags=["Exportação"])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html") as file:
        return file.read()

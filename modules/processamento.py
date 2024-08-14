from fastapi import APIRouter, Depends
from datetime import datetime
from services.extraction import verify_url, extract_table_data, extract_table_all_data
import pandas as pd
from services.database import Database
import json


router = APIRouter()

URL_TEMPLATES = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_04",
]

TABLE_TEMPLATES = [
    "uvas_viniferas_processadas",
    "uvas_americanas_hibridas_processadas",
    "uvas_mesa_processadas",
    "uvas_sem_classificacao_processadas",
]

YEAR = datetime.now().year - 1

@router.get("/")
def get_processamento(index: int, start_year: int, end_year: int = None):
    """
    Retorna os dados de processamento de vinhos e derivados no Brasil.
    
    - **index**: Seleciona o tipo de exportação da consulta (obrigatório).
        - **0**: Processamento Uvas viníferas.
        - **1**: Processamento Uvas americanas e híbridas.
        - **2**: Processamento Uvas de mesa.
        - **3**: Processamento Uvas sem classificação.
    - **start_year**: Ano inicial da consulta (obrigatório).
    - **end_year**: Ano final da consulta (opcional, se não fornecido, retorna dados somente do ano inicial).
    """
    if end_year:
        if verify_url(URL_TEMPLATES[index].format(year=YEAR)):
            data = extract_table_all_data(URL_TEMPLATES[index],start_year, end_year)
            data = data.to_json(orient='records')
        else:
            with Database() as db:
                result = db.get_items_between_years(TABLE_TEMPLATES[index], start_year, end_year)
                data = json.dumps(result, default=str)
    else:
        if verify_url(URL_TEMPLATES[index].format(year=YEAR)):
            data = extract_table_data(URL_TEMPLATES[index],start_year)
            data = data.to_json(orient='records')
        else:
            with Database() as db:
                result = db.get_items_year(TABLE_TEMPLATES[index], start_year)
                data = json.dumps(result, default=str)
    return {"data": data}

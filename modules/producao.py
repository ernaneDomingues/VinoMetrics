from fastapi import APIRouter, Depends
from datetime import datetime
from services.extraction import verify_url, extract_table_data, extract_table_all_data
import pandas as pd
from services.database import Database
import json

router = APIRouter()

URL_TEMPLATE = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02",
]

TABLE_TEMPLATE = ['producao_vinhos_sucos_derivados']

YEAR = datetime.now().year - 1

@router.get("/")
def get_producao(start_year: int, end_year: int = None):
    """
    Retorna os dados de produção de vinhos e derivados no Brasil.
    
    - **start_year**: Ano inicial da consulta (obrigatório).
    - **end_year**: Ano final da consulta (opcional, se não fornecido, retorna dados somente do ano inicial).
    """
    if end_year:
        if verify_url(URL_TEMPLATE[0].format(year=YEAR)):
            data = extract_table_all_data(URL_TEMPLATE[0], start_year, end_year)
            data = data.to_json(orient='records')
        else:
            with Database() as db:
                result = db.get_items_between_years(TABLE_TEMPLATE[0], start_year, end_year)
                data = json.dumps(result, default=str)
    else:
        if verify_url(URL_TEMPLATE[0].format(year=YEAR)):
            data = extract_table_data(URL_TEMPLATE[0], start_year)
            data = data.to_json(orient='records')
        else:
            with Database() as db:
                result = db.get_items_year(TABLE_TEMPLATE[0], start_year)
                data = json.dumps(result, default=str)
    return {"data": data}

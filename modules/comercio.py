from fastapi import APIRouter, Depends
from datetime import datetime
from services.extraction import verify_url, extract_table_data, extract_table_all_data
import pandas as pd
from services.database import Database
import json

router = APIRouter()

URL_TEMPLATE = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04",
]

TABLE_TEMPLATE = ['comercializacao_vinhos_derivados']

YEAR = datetime.now().year - 1

@router.get("/")
def get_comercio(start_year: int, end_year: int = None):
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

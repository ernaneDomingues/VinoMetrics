import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os
import unicodedata

def verify_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def standardize_column_name(column):
    column = column.strip()  # Remove extra spaces
    column = column.lower()  # Convert to lowercase
    column = column.replace(' ', '_')  # Replace spaces with underscores
    column = column.replace('(', '')  # Remove parentheses
    column = column.replace(')', '')  # Remove parentheses
    column = column.replace('.', '')  # Remove periods
    column = column.replace('$', 'd')  # Replace $ with D
    
    # Remove accents
    column = unicodedata.normalize('NFKD', column).encode('ascii', 'ignore').decode('utf-8')
    
    return column

def parse_table_content_with_category(content):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', class_='tb_base tb_dados')
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []
    
    if 'Países' not in headers:
        headers.insert(0, 'Categoria')
        current_category = None

        for row in table.find_all('tr'):
            cells = row.find_all('td')

            if len(cells) == 2:
                product = cells[0].text.strip()
                quantity = cells[1].text.strip().replace('.', '').replace('-', '0')
                quantity = int(quantity) if quantity.isdigit() else 0

                if product.isupper() and not any(c.isdigit() for c in product):
                    current_category = product
                else:
                    rows.append([current_category, product, quantity])
    else:
        current_category = None

        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) == 2:
                product = cells[0].text.strip()
                quantity = cells[1].text.strip().replace('.', '').replace('-', '0')
                quantity = int(quantity) if quantity.isdigit() else 0

                if product.isupper() and not any(c.isdigit() for c in product):
                    current_category = product
                else:
                    rows.append([current_category, product, quantity])
            else:
                row_data = [cell.text.strip().replace('.', '').replace('-', '0') for cell in cells]
                rows.append(row_data)

    return headers, rows

def extract_table_data(url, year):
    try:
        content = fetch_page_content(url)
        headers, rows = parse_table_content_with_category(content)
        df = pd.DataFrame(rows, columns=headers)
        df['Ano'] = year
        df.columns = [standardize_column_name(col) for col in df.columns]
        return df
    except Exception as e:
        print(f"Erro ao extrair dados do ano {year}: {e}")
        return pd.DataFrame()

def extract_table_all_data(url_template, start_year, end_year):
    all_data = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        url = url_template.format(year=year)
        year_data = extract_table_data(url, year)
        if not year_data.empty:
            all_data = pd.concat([all_data, year_data], ignore_index=True)
    return all_data

if __name__=='__main__':    
    # Função principal para extrair dados de todos os URLs
    print('Oi')
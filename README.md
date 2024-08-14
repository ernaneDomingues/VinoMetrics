### **README.md**

```markdown
# Projeto de API para Distribuição de Dados Vitivinícolas

## Descrição

Este projeto desenvolve uma API utilizando FastAPI para fornecer dados detalhados sobre a produção, importação, exportação, comercialização e processamento de vinhos, sucos e derivados no Brasil. Os dados abrangem o período de 1970 até 2023, extraídos do site da Embrapa Uva e Vinho.

## Funcionalidades

- **Rotas modulares:** A API está organizada em módulos, cada um responsável por um tipo específico de dados.
- **Web Scraping:** Os dados são extraídos diretamente de tabelas disponíveis online utilizando técnicas de web scraping.
- **Persistência de Dados:** Dados extraídos são armazenados e recuperados de um banco de dados PostgreSQL.
- **Consultas Personalizadas:** Permite consultas por ano inicial e final, além de filtros específicos para diferentes categorias de produtos.

## Estrutura do Projeto

- **main.py:** Arquivo principal que inicia a API e carrega todas as rotas.
- **modules/**
  - **comercio.py:** Rota para dados de comercialização de vinhos e derivados.
  - **producao.py:** Rota para dados de produção de vinhos, sucos e derivados.
  - **processamento.py:** Rota para dados de processamento de uvas.
  - **importacao.py:** Rota para dados de importação.
  - **exportacao.py:** Rota para dados de exportação.
- **services/**
  - **database.py:** Classe para manipulação de operações com o banco de dados PostgreSQL.
  - **extraction.py:** Funções para extração e tratamento dos dados utilizando web scraping.
- **templates/**
  - **index.html:** Página HTML estática com informações sobre o projeto.

## Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
     ```
     HDATABASE=nome_do_banco
     HUSER=usuario_do_banco
     HPASSWORD=senha_do_banco
     HHOST=host_do_banco
     HPORT=porta_do_banco
     ```

5. **Execute a API:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Acesse a API:**
   - A API estará disponível em `http://127.0.0.1:8000`

## Rotas Disponíveis

- **GET /**: Retorna a página HTML com informações sobre o projeto.
- **GET /comercio/**: Dados de comercialização. Parâmetros: `start_year`, `end_year`.
- **GET /producao/**: Dados de produção. Parâmetros: `start_year`, `end_year`.
- **GET /processamento/**: Dados de processamento de uvas. Parâmetros: `index`, `start_year`, `end_year`.
- **GET /importacao/**: Dados de importação. Parâmetros: `index`, `start_year`, `end_year`.
- **GET /exportacao/**: Dados de exportação. Parâmetros: `index`, `start_year`, `end_year`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
```


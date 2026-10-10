# EcoMonitor Brasil

Plataforma Inteligente para Monitoramento de Indicadores Ambientais e Sustentabilidade.

O EcoMonitor Brasil é uma aplicação desenvolvida em Python com Streamlit para integrar, organizar, analisar e visualizar diferentes tipos de dados ambientais.

O projeto trabalha com dados climáticos, notícias ambientais, informações históricas de desmatamento e registros enviados pelo usuário, além de disponibilizar parte dos dados através de uma API desenvolvida com FastAPI.

O projeto está relacionado principalmente ao pilar **Environmental (E)** do ESG e aos seguintes Objetivos de Desenvolvimento Sustentável:

- ODS 13 — Ação Contra a Mudança Global do Clima;
- ODS 15 — Vida Terrestre.

---

## Funcionalidades

Atualmente, o EcoMonitor Brasil possui:

- aplicação Streamlit multipáginas;
- menu de navegação;
- dashboard climático;
- integração com Open-Meteo;
- WebScraping de notícias ambientais;
- análise textual;
- nuvem de palavras;
- upload de arquivos CSV;
- download de arquivos;
- cache;
- estado de sessão;
- dados históricos de desmatamento PRODES;
- coleta dinâmica com Selenium;
- API própria com FastAPI;
- endpoints GET;
- endpoint POST;
- integração entre Streamlit e FastAPI;
- preparação para futuras funcionalidades com LLM.

---

## Páginas da Aplicação

A aplicação está organizada nas seguintes páginas:

### Início

Apresenta uma visão geral do projeto, objetivos, ODS relacionados e acesso às principais funcionalidades.

### Dashboard Climático

Permite consultar dados meteorológicos por localidade.

Principais indicadores:

- temperatura máxima;
- temperatura mínima;
- precipitação.

Os dados são obtidos através da Open-Meteo.

### Radar Ambiental

Apresenta notícias ambientais coletadas do INPE.

Inclui:

- tabela de notícias;
- links;
- contagem de notícias;
- análise de palavras;
- nuvem de palavras.

### Desmatamento PRODES

Apresenta dados históricos de desmatamento do PRODES/INPE.

Inclui:

- filtro por UF;
- filtro por período;
- maior área desmatada;
- ano de maior desmatamento;
- média anual;
- série histórica;
- comparação entre estados.

### API EcoMonitor

Demonstra a integração da aplicação Streamlit com a API desenvolvida em FastAPI.

Permite:

- verificar o status da API;
- consultar dados PRODES;
- consultar notícias;
- enviar registros ambientais;
- visualizar registros armazenados.

### Base de Dados

Permite:

- upload de arquivos CSV;
- visualização dos dados;
- análise de tipos;
- identificação de valores nulos;
- estatísticas descritivas;
- download de arquivos.

### Sobre

Apresenta informações gerais sobre o projeto, tecnologias, ESG, ODS e próximas etapas.

---

## Fontes de Dados

### Open-Meteo

Utilizada para coleta de dados meteorológicos.

Principais informações:

- temperatura máxima;
- temperatura mínima;
- precipitação.

Método:

- API REST;
- Requests;
- Pandas.

---

### INPE

Utilizado como fonte de notícias ambientais.

Método:

- Requests;
- BeautifulSoup.

Arquivo gerado:

`data/processed/noticias_inpe.csv`

---

### PRODES / TerraBrasilis / INPE

Utilizado como fonte de dados históricos de desmatamento.

Principais campos:

- UF;
- Ano;
- Area_km2.

Como a página possui conteúdo carregado dinamicamente por JavaScript, a coleta utiliza Selenium.

Arquivo processado:

`data/processed/desmatamento_prodes.csv`

Snapshot do HTML renderizado:

`data/raw/terrabrasilis_prodes_renderizado.html`

---

## Coleta com Selenium

A coleta PRODES utiliza Selenium porque os dados não estão disponíveis diretamente no HTML inicial da página.

O processo utilizado é:

TerraBrasilis  
↓  
Selenium  
↓  
HTML renderizado  
↓  
BeautifulSoup  
↓  
Pandas  
↓  
CSV

O script está localizado em:

`src/data/coleta_prodes_selenium.py`

A coleta é executada separadamente da aplicação Streamlit.

---

## API EcoMonitor Brasil

O projeto possui uma API própria desenvolvida com FastAPI.

Arquivo principal:

`api/main.py`

Principais endpoints:

### GET /

Retorna informações sobre o status da API.

### GET /prodes

Consulta os dados históricos de desmatamento.

Permite filtros por:

- UF;
- ano.

### GET /noticias

Retorna as notícias ambientais coletadas.

### POST /registros

Permite inserir novos registros ambientais.

Campos:

- localidade;
- indicador;
- valor;
- unidade;
- fonte.

### GET /registros

Retorna os registros ambientais armazenados.

---

## Documentação da API

Com a API em execução, a documentação automática pode ser acessada em:

`http://127.0.0.1:8000/docs`

A interface permite testar os endpoints diretamente pelo navegador.

---

## Como Executar o Projeto

### 1. Criar o ambiente virtual

No PowerShell:

`python -m venv .venv`

---

### 2. Ativar o ambiente virtual

No Windows PowerShell:

`.venv\Scripts\Activate.ps1`

---

### 3. Instalar as dependências

`pip install -r requirements.txt`

---

## Executar a Aplicação Streamlit

Na raiz do projeto:

`streamlit run app/app.py`

A aplicação será aberta no navegador.

Normalmente, o endereço local será:

`http://localhost:8501`

---

## Executar a API FastAPI

Abra outro terminal com o ambiente virtual ativado.

Execute:

`uvicorn api.main:app --reload`

A API será disponibilizada em:

`http://127.0.0.1:8000`

A documentação estará disponível em:

`http://127.0.0.1:8000/docs`

---

## Executar Streamlit e FastAPI Juntos

Para utilizar a página API EcoMonitor corretamente, os dois serviços precisam estar ativos.

Terminal 1:

`streamlit run app/app.py`

Terminal 2:

`uvicorn api.main:app --reload`

Durante o desenvolvimento local, a página Streamlit utiliza:

`http://127.0.0.1:8000`

como endereço da API.

---

## Executar a Coleta PRODES

Para atualizar os dados de desmatamento:

`python src/data/coleta_prodes_selenium.py`

O script:

- abre o TerraBrasilis;
- aguarda o carregamento dos dados;
- captura o HTML renderizado;
- extrai os dados;
- trata os valores;
- salva o arquivo processado.

Arquivos gerados:

`data/raw/terrabrasilis_prodes_renderizado.html`

`data/processed/desmatamento_prodes.csv`

---

## Estrutura Principal do Projeto

ecomonitor-brasil/

- api/
  - main.py

- app/
  - app.py
  - paginas/
    - inicio.py
    - clima.py
    - radar_ambiental.py
    - desmatamento.py
    - api_ecomonitor.py
    - dados.py
    - sobre.py

- data/
  - raw/
  - processed/
  - external/

- docs/
  - project_charter.md
  - data_summary_report.md

- notebooks/
  - exploracao.ipynb

- src/
  - analysis/
  - data/
    - coleta_open_meteo.py
    - coleta_noticias_inpe.py
    - coleta_prodes_selenium.py
  - visualization/

- tests/

- README.md
- requirements.txt
- requirements-api.txt

---

## Principais Arquivos de Dados

### `noticias_inpe.csv`

Contém:

- título;
- URL.

Utilizado no Radar Ambiental e na API.

### `desmatamento_prodes.csv`

Contém:

- UF;
- Ano;
- Area_km2.

Utilizado na página Desmatamento PRODES e na API.

### `registros_ambientais.csv`

Contém os registros enviados através da API.

Campos:

- localidade;
- indicador;
- valor;
- unidade;
- fonte.

---

## Tecnologias Utilizadas

- Python;
- Streamlit;
- Pandas;
- Requests;
- BeautifulSoup;
- Selenium;
- Matplotlib;
- WordCloud;
- FastAPI;
- Uvicorn;
- Pydantic;
- Git;
- GitHub;
- Visual Studio Code.

---

## Metodologia

O projeto utiliza princípios das metodologias:

- CRISP-DM;
- TDSP.

As principais etapas envolvem:

1. entendimento do problema;
2. entendimento dos dados;
3. coleta;
4. preparação;
5. análise;
6. avaliação;
7. implantação.

---

## Preparação para LLM

A arquitetura atual prepara o EcoMonitor Brasil para futuras funcionalidades baseadas em Large Language Models.

Possíveis aplicações:

- resumo automático de notícias;
- classificação temática;
- análise de sentimento;
- perguntas e respostas;
- geração automática de relatórios;
- explicação de indicadores em linguagem natural.

Os cálculos continuarão sendo realizados em Python e Pandas.

O LLM poderá ser utilizado principalmente para interpretação e geração textual.

---

## Limitações Atuais

Algumas limitações do projeto são:

- dependência da disponibilidade das fontes externas;
- mudanças no HTML podem afetar o WebScraping;
- mudanças no TerraBrasilis podem exigir ajustes no Selenium;
- Selenium possui maior custo computacional;
- os registros da API são armazenados em CSV;
- a FastAPI é executada localmente durante o desenvolvimento;
- para integração online completa, a API deverá ser publicada separadamente.

---

## Documentação

A documentação do projeto está disponível em:

`docs/project_charter.md`

`docs/data_summary_report.md`

O Project Charter apresenta os objetivos, escopo e evolução do projeto.

O Data Summary Report apresenta as fontes, estruturas, tratamentos, validações e limitações dos dados.

---

## Status Atual

O projeto atualmente possui:

- aplicação Streamlit multipáginas;
- dashboard climático funcional;
- notícias ambientais coletadas;
- análise textual;
- dados históricos PRODES;
- coleta dinâmica com Selenium;
- FastAPI funcional;
- endpoints GET e POST;
- integração Streamlit/FastAPI;
- documentação atualizada;
- estrutura preparada para futuras funcionalidades com LLM.

---

## Próximas Etapas

As próximas evoluções podem incluir:

- integração efetiva com LLM;
- resumo de notícias;
- classificação ambiental;
- perguntas e respostas;
- geração automática de relatórios;
- novas fontes de dados;
- novos indicadores ambientais;
- publicação da FastAPI em ambiente externo.

---

## Autor

Projeto acadêmico desenvolvido para aplicação de conceitos de Ciência de Dados, Engenharia de Dados, WebScraping, APIs, visualização de dados e sustentabilidade.
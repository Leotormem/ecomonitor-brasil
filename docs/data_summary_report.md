# Data Summary Report — EcoMonitor Brasil

## Visão Geral

O EcoMonitor Brasil utiliza diferentes fontes de dados ambientais para reunir informações climáticas, notícias ambientais, dados de desmatamento e registros enviados pelo usuário.

O projeto combina:

- API pública;
- WebScraping com BeautifulSoup;
- coleta dinâmica com Selenium;
- arquivos CSV;
- FastAPI para consulta e envio de dados;
- Streamlit para visualização e interação.

Este relatório apresenta as principais fontes, estruturas, tratamentos, validações e limitações dos dados utilizados.

---

## 1. Fontes de Dados

As principais fontes utilizadas são:

| Fonte | Tipo | Método de Coleta | Dados |
|---|---|---|---|
| Open-Meteo | API | Requests | Temperatura e precipitação |
| INPE | Página web | Requests + BeautifulSoup | Notícias ambientais |
| TerraBrasilis / PRODES | Página dinâmica | Selenium + BeautifulSoup | Desmatamento por UF e ano |
| Usuário | Formulário/API | FastAPI POST | Registros ambientais |
| Usuário | Arquivo | Upload CSV | Dados complementares |

---

## 2. Open-Meteo

A Open-Meteo é utilizada para obtenção de dados meteorológicos.

Principais indicadores:

- temperatura máxima;
- temperatura mínima;
- precipitação.

A coleta é realizada por meio de requisições HTTP e os dados retornados em JSON são organizados em DataFrames com Pandas.

Fluxo:

Open-Meteo  
↓  
Requests  
↓  
JSON  
↓  
Pandas  
↓  
Streamlit

Os dados são utilizados principalmente na página Dashboard Climático.

### Limitações

A consulta depende da disponibilidade da API.

Os dados utilizados no projeto devem ser interpretados conforme o período e o tipo de informação retornados pela fonte.

---

## 3. Notícias Ambientais — INPE

O INPE é utilizado como fonte de notícias ambientais.

A coleta é realizada através de:

- Requests;
- BeautifulSoup;
- Pandas.

Os principais campos coletados são:

| Campo | Descrição |
|---|---|
| titulo | Título da notícia |
| url | Link da notícia |

Os dados são armazenados em:

`data/processed/noticias_inpe.csv`

O arquivo é utilizado na página Radar Ambiental para:

- exibição das notícias;
- contagem de registros;
- análise das palavras mais frequentes;
- geração de nuvem de palavras;
- acesso aos links originais.

### Tratamento

São aplicadas operações básicas como:

- remoção de espaços extras;
- eliminação de registros vazios;
- remoção de duplicidades;
- organização em DataFrame.

### Limitações

Mudanças na estrutura HTML do site podem exigir ajustes no script de coleta.

Atualmente, a base utiliza principalmente títulos e URLs, e não o conteúdo completo das notícias.

---

## 4. PRODES / TerraBrasilis

No TP3 foi incorporada uma nova fonte de dados através do PRODES/INPE, disponível no TerraBrasilis.

Os dados utilizados representam informações históricas de desmatamento.

Principais campos:

| Campo | Descrição |
|---|---|
| UF | Unidade federativa |
| Ano | Ano de referência |
| Area_km2 | Área desmatada em km² |

O arquivo processado é armazenado em:

`data/processed/desmatamento_prodes.csv`

---

## 5. Uso de Selenium

A página do TerraBrasilis carrega a tabela de dados dinamicamente através de JavaScript.

Por esse motivo, Requests e BeautifulSoup sozinhos não disponibilizam diretamente toda a tabela necessária.

O Selenium é utilizado para:

- abrir a página;
- executar o JavaScript;
- aguardar o carregamento dos dados;
- capturar o HTML renderizado.

Depois disso, o BeautifulSoup realiza a extração da tabela.

Fluxo:

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

O script utilizado está em:

`src/data/coleta_prodes_selenium.py`

---

## 6. Snapshot do TerraBrasilis

O HTML renderizado é salvo em:

`data/raw/terrabrasilis_prodes_renderizado.html`

Esse arquivo pode ser utilizado para:

- conferência da coleta;
- depuração;
- rastreabilidade;
- processamento posterior.

---

## 7. Tratamento dos Dados PRODES

Após a coleta, são realizadas etapas de limpeza e transformação.

Entre elas:

- identificação da UF;
- remoção de textos adicionais no nome da UF;
- tratamento do ano;
- remoção da unidade de medida;
- conversão de valores brasileiros para formato numérico;
- criação da coluna `Area_km2`.

Exemplo:

`1.234,56`

é convertido para:

`1234.56`

---

## 8. Validação dos Dados PRODES

Antes de salvar os dados processados, são realizadas verificações.

Entre elas:

- DataFrame não vazio;
- presença das unidades federativas esperadas;
- presença de linhas anuais;
- quantidade adequada de registros;
- conversão correta dos valores numéricos.

A coleta atual gerou aproximadamente:

- 342 registros;
- 9 unidades federativas.

A quantidade poderá mudar caso a fonte seja atualizada.

---

## 9. Uso dos Dados PRODES

Os dados são utilizados na página Desmatamento PRODES.

As análises incluem:

- filtro por UF;
- filtro por período;
- maior área desmatada;
- ano de maior desmatamento;
- média anual;
- série histórica;
- comparação entre estados.

Os mesmos dados também podem ser consultados através de:

`GET /prodes`

---

## 10. Registros Ambientais

No TP3 foi criada uma forma de entrada de dados através da FastAPI.

O usuário pode enviar registros contendo:

| Campo | Descrição |
|---|---|
| localidade | Local do registro |
| indicador | Indicador ambiental |
| valor | Valor numérico |
| unidade | Unidade de medida |
| fonte | Origem da informação |

Os dados são enviados através de:

`POST /registros`

e armazenados em:

`data/processed/registros_ambientais.csv`

---

## 11. Validação dos Registros

Os dados recebidos pela API são validados com Pydantic.

São verificadas informações como:

- campos obrigatórios;
- tamanho mínimo dos textos;
- tipo numérico do campo valor;
- estrutura correta da requisição.

Os registros armazenados podem ser consultados por:

`GET /registros`

---

## 12. Upload de CSV

A aplicação também permite o envio de arquivos CSV pelo usuário.

A página Base de Dados permite:

- carregar o arquivo;
- visualizar os dados;
- contar linhas e colunas;
- verificar tipos;
- verificar valores nulos;
- gerar estatísticas descritivas;
- fazer download dos dados.

---

## 13. Organização dos Arquivos

Os dados são organizados principalmente em:

### `data/raw/`

Utilizado para dados brutos e snapshots.

### `data/processed/`

Utilizado para dados tratados e prontos para análise.

Principais arquivos:

- `noticias_inpe.csv`;
- `desmatamento_prodes.csv`;
- `registros_ambientais.csv`.

### `data/external/`

Reservado para arquivos externos complementares.

---

## 14. Qualidade dos Dados

As validações variam de acordo com a fonte.

### Open-Meteo

- resposta válida;
- presença dos indicadores esperados;
- estrutura temporal adequada.

### Notícias INPE

- título não vazio;
- URL disponível;
- remoção de duplicidades.

### PRODES

- presença de dados;
- UFs esperadas;
- linhas anuais;
- conversão numérica;
- proteção contra coleta incompleta.

### Registros Ambientais

- validação Pydantic;
- campos obrigatórios;
- tipo correto dos dados.

---

## 15. Uso de Cache

A aplicação utiliza `st.cache_data` para evitar leituras e processamentos repetitivos.

O cache melhora:

- tempo de carregamento;
- desempenho;
- experiência do usuário.

---

## 16. Uso de Session State

O `st.session_state` é utilizado para preservar informações durante a interação do usuário com a aplicação.

Essa funcionalidade ajuda a manter dados entre diferentes ações realizadas na interface.

---

## 17. FastAPI

A FastAPI funciona como uma camada de acesso aos dados processados.

Principais endpoints:

- `GET /`
- `GET /prodes`
- `GET /noticias`
- `POST /registros`
- `GET /registros`

A API foi publicada no Render.

URL:

https://ecomonitor-api-7pvm.onrender.com

Documentação:

https://ecomonitor-api-7pvm.onrender.com/docs

---

## 18. Integração Streamlit e FastAPI

A página API EcoMonitor realiza requisições para a FastAPI publicada no Render.

A aplicação Streamlit está publicada em:

https://ecomonitor-brasil-wqhkx2ffy8cqvappehedvjy.streamlit.app/

A comunicação entre os dois serviços foi validada em ambiente online.

Fluxo de consulta:

Usuário  
↓  
Streamlit Community Cloud  
↓  
FastAPI no Render  
↓  
CSV  
↓  
JSON  
↓  
Streamlit

Fluxo de inclusão:

Usuário  
↓  
Formulário Streamlit  
↓  
POST  
↓  
FastAPI no Render  
↓  
CSV

---

## 19. Persistência

Atualmente, os dados enviados pela API são armazenados em arquivo CSV.

Essa solução é suficiente para o escopo acadêmico atual.

Entretanto, para cenários com maior volume ou múltiplos usuários simultâneos, uma evolução futura poderá utilizar banco de dados.

Possíveis opções:

- PostgreSQL;
- SQLite;
- outro sistema relacional.

---

## 20. Limitações

As principais limitações atuais são:

- dependência de fontes externas;
- mudanças em páginas podem afetar o WebScraping;
- Selenium depende da estrutura atual do TerraBrasilis;
- a coleta PRODES precisa ser executada novamente para atualização;
- os registros da API são armazenados em CSV;
- arquivos CSV não são ideais para alto volume ou escrita simultânea;
- serviços gratuitos de hospedagem podem apresentar maior tempo de resposta após períodos de inatividade;
- a base de notícias contém principalmente títulos e links.

---

## 21. Preparação para LLM

Os dados atuais já permitem preparar futuras funcionalidades baseadas em Large Language Models.

Possíveis aplicações:

- resumo de notícias;
- classificação temática;
- análise de sentimento;
- perguntas e respostas;
- geração automática de relatórios;
- interpretação dos resultados ambientais.

Os cálculos numéricos continuarão sendo realizados em Python e Pandas.

O LLM poderá ser utilizado principalmente para interpretar e apresentar os resultados em linguagem natural.

---

## 22. Fluxo Geral dos Dados

Open-Meteo  
↓  
Requests  
↓  
Dados Climáticos  
↓  
Dashboard Climático

INPE  
↓  
Requests + BeautifulSoup  
↓  
`noticias_inpe.csv`  
↓  
Radar Ambiental / FastAPI

TerraBrasilis  
↓  
Selenium + BeautifulSoup  
↓  
`desmatamento_prodes.csv`  
↓  
Desmatamento PRODES / FastAPI

Usuário  
↓  
Streamlit Cloud  
↓  
FastAPI no Render  
↓  
`registros_ambientais.csv`

---

## Conclusão

O EcoMonitor Brasil utiliza diferentes formas de aquisição de dados para construir uma visão integrada de informações ambientais.

A Open-Meteo fornece dados estruturados através de API.

O INPE fornece dados textuais coletados por WebScraping.

O TerraBrasilis fornece dados dinâmicos de desmatamento coletados com Selenium e BeautifulSoup.

A FastAPI permite consultar os dados processados e inserir novos registros.

A API foi publicada no Render e está integrada à aplicação Streamlit publicada no Streamlit Community Cloud.

O Streamlit concentra a visualização e a interação com o usuário.

A organização atual separa:

- aquisição;
- processamento;
- armazenamento;
- API;
- visualização.

Essa estrutura melhora a organização do projeto e prepara a aplicação para futuras funcionalidades baseadas em Inteligência Artificial e Large Language Models.
# Project Charter — EcoMonitor Brasil

## Nome do Projeto

**EcoMonitor Brasil — Plataforma Inteligente para Monitoramento de Indicadores Ambientais e Sustentabilidade**

---

## Problema de Negócio

Dados ambientais relevantes, como informações climáticas, notícias ambientais e dados de desmatamento, encontram-se distribuídos em diferentes fontes públicas.

Essa fragmentação dificulta a análise integrada das informações, o acompanhamento de tendências e a identificação de situações críticas.

O EcoMonitor Brasil busca centralizar essas informações em uma aplicação interativa, permitindo visualizar, analisar e consultar diferentes indicadores ambientais em um único ambiente.

No TP3, o projeto também passou a incorporar:

- arquitetura multipáginas;
- coleta de dados de páginas dinâmicas;
- integração com dados históricos de desmatamento;
- criação de uma API própria;
- integração entre Streamlit e FastAPI;
- publicação da API em ambiente web;
- integração online entre frontend e backend;
- preparação para futuras aplicações com LLM.

---

## Objetivo Geral

Desenvolver uma aplicação interativa em Python e Streamlit capaz de integrar, organizar, analisar e apresentar dados ambientais provenientes de diferentes fontes públicas, apoiando o acompanhamento de indicadores relacionados à sustentabilidade e às mudanças climáticas.

---

## Objetivos Específicos

- Integrar fontes públicas de dados ambientais.
- Realizar coleta de dados por APIs.
- Utilizar WebScraping com BeautifulSoup.
- Utilizar Selenium quando a página exigir execução de JavaScript.
- Armazenar os dados coletados em arquivos estruturados.
- Criar uma aplicação multipáginas em Streamlit.
- Disponibilizar métricas, gráficos e tabelas interativas.
- Permitir upload e download de arquivos CSV.
- Utilizar cache e estado de sessão.
- Integrar dados históricos do PRODES/INPE.
- Criar uma API própria com FastAPI.
- Implementar endpoints GET e POST.
- Integrar Streamlit e FastAPI.
- Publicar o Streamlit em ambiente web.
- Publicar a FastAPI em ambiente web.
- Garantir comunicação online entre Streamlit e FastAPI.
- Preparar o projeto para futuras funcionalidades com LLM.

---

## Pilar ESG

O projeto está relacionado principalmente ao pilar:

**Environmental (E) — Ambiental.**

A aplicação utiliza informações climáticas, ambientais e de desmatamento para facilitar o acompanhamento de indicadores relacionados à sustentabilidade.

---

## Objetivos de Desenvolvimento Sustentável

### ODS 13 — Ação Contra a Mudança Global do Clima

O projeto está relacionado ao ODS 13 por utilizar dados meteorológicos como:

- temperatura máxima;
- temperatura mínima;
- precipitação.

Essas informações ajudam no acompanhamento de condições climáticas e ambientais.

### ODS 15 — Vida Terrestre

O projeto também está alinhado ao ODS 15 por incorporar dados de desmatamento do PRODES/INPE e informações relacionadas ao monitoramento ambiental.

Os dados permitem analisar:

- evolução histórica do desmatamento;
- comparação entre estados;
- anos de maior desmatamento;
- tendências relacionadas à cobertura vegetal.

---

## Público-Alvo

O público-alvo inclui:

- gestores públicos;
- empresas interessadas em ESG;
- organizações ambientais;
- pesquisadores;
- instituições acadêmicas;
- estudantes;
- profissionais de análise de dados;
- cidadãos interessados em sustentabilidade.

---

## Stakeholders

Os principais stakeholders são:

- usuários da aplicação;
- gestores públicos;
- organizações ambientais;
- empresas interessadas em ESG;
- pesquisadores;
- instituições acadêmicas;
- desenvolvedor responsável pelo projeto;
- instituições responsáveis pelas fontes de dados.

---

## Escopo do Projeto

O projeto contempla:

- desenvolvimento em Python;
- aplicação Streamlit;
- arquitetura multipáginas;
- coleta de dados por API;
- WebScraping com BeautifulSoup;
- coleta dinâmica com Selenium;
- armazenamento em CSV;
- análise e visualização de dados;
- upload e download de arquivos;
- cache;
- estado de sessão;
- integração com dados PRODES;
- FastAPI;
- endpoints GET e POST;
- integração Streamlit/FastAPI;
- publicação do Streamlit;
- publicação da FastAPI;
- integração online entre os serviços;
- Git e GitHub;
- preparação para uso futuro de LLM.

---

## Arquitetura da Aplicação

No TP3, o EcoMonitor Brasil foi reorganizado em uma aplicação multipáginas.

A navegação utiliza:

- `st.navigation`;
- `st.Page`.

As páginas atuais são:

- Início;
- Dashboard Climático;
- Radar Ambiental;
- Desmatamento PRODES;
- API EcoMonitor;
- Base de Dados;
- Sobre.

Essa organização separa as funcionalidades e melhora a navegação do usuário.

---

## Fontes de Dados

### Open-Meteo

Utilizada para dados meteorológicos.

Principais indicadores:

- temperatura máxima;
- temperatura mínima;
- precipitação.

Método:

- API REST;
- Requests;
- Pandas.

---

### INPE — Notícias

Utilizado como fonte de notícias ambientais.

Método:

- Requests;
- BeautifulSoup.

Os dados são armazenados em:

`data/processed/noticias_inpe.csv`

Principais campos:

- título;
- URL.

---

### PRODES / TerraBrasilis

No TP3 foi incorporada uma nova fonte de dados históricos de desmatamento.

Principais campos:

- UF;
- ano;
- área desmatada em km².

Os dados são armazenados em:

`data/processed/desmatamento_prodes.csv`

---

## Uso de Selenium

A página do TerraBrasilis carrega os dados através de JavaScript.

Por isso, o Selenium foi utilizado para acessar o conteúdo renderizado da página.

O processo é:

TerraBrasilis  
↓  
Selenium  
↓  
HTML renderizado  
↓  
BeautifulSoup  
↓  
CSV

O HTML renderizado também é salvo em:

`data/raw/terrabrasilis_prodes_renderizado.html`

A coleta é executada separadamente da aplicação Streamlit.

---

## Funcionalidades Principais

A aplicação atualmente oferece:

- seleção de cidades;
- dados climáticos;
- gráficos;
- métricas;
- tabelas;
- notícias ambientais;
- análise de palavras;
- nuvem de palavras;
- upload de CSV;
- download de CSV;
- cache;
- estado de sessão;
- análise de desmatamento;
- filtros por UF e ano;
- comparação histórica;
- integração com FastAPI;
- consulta e envio de registros.

---

## API EcoMonitor Brasil

No TP3 foi criada uma API própria utilizando FastAPI.

A API permite consultar e enviar dados sem depender diretamente da interface visual.

Principais endpoints:

### GET /

Verifica o status da API.

### GET /prodes

Consulta dados de desmatamento.

Permite filtros por:

- UF;
- ano.

### GET /noticias

Retorna notícias ambientais coletadas do INPE.

### POST /registros

Permite inserir novos registros ambientais.

Campos:

- localidade;
- indicador;
- valor;
- unidade;
- fonte.

### GET /registros

Retorna os registros enviados anteriormente.

---

## Integração Streamlit e FastAPI

A página **API EcoMonitor** realiza requisições HTTP para a FastAPI.

A integração permite:

- verificar o status da API;
- consultar dados PRODES;
- consultar notícias;
- enviar novos registros;
- consultar registros armazenados.

Fluxo:

Usuário  
↓  
Streamlit  
↓  
FastAPI  
↓  
Dados processados

---

## Publicação da Aplicação

A aplicação Streamlit está publicada no Streamlit Community Cloud.

URL:

https://ecomonitor-brasil-wqhkx2ffy8cqvappehedvjy.streamlit.app/

---

## Publicação da FastAPI

A API EcoMonitor está publicada no Render.

URL:

https://ecomonitor-api-7pvm.onrender.com

Documentação Swagger:

https://ecomonitor-api-7pvm.onrender.com/docs

A aplicação Streamlit publicada utiliza a URL pública da API para realizar suas consultas.

Dessa forma, a integração Streamlit/FastAPI também funciona no ambiente online.

---

## Repositório

O código-fonte está versionado com Git e armazenado no GitHub.

Repositório:

https://github.com/Leotormem/ecomonitor-brasil

---

## Organização dos Dados

Os dados são organizados principalmente em:

### `data/raw/`

Contém dados brutos e snapshots.

### `data/processed/`

Contém dados tratados e utilizados pela aplicação.

Principais arquivos:

- `noticias_inpe.csv`;
- `desmatamento_prodes.csv`;
- `registros_ambientais.csv`.

### `data/external/`

Reservado para dados externos complementares.

---

## Metodologia

O projeto utiliza princípios das metodologias:

- CRISP-DM;
- TDSP.

As principais etapas são:

1. entendimento do problema;
2. entendimento dos dados;
3. coleta;
4. preparação;
5. análise;
6. avaliação;
7. implantação.

O TDSP também orienta a organização das pastas, separação entre coleta, processamento, interface e documentação.

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
- Streamlit Community Cloud;
- Render;
- Visual Studio Code.

---

## Principais Entregáveis

Os principais entregáveis atuais são:

- Project Charter;
- Data Summary Report;
- scripts de coleta;
- arquivos CSV;
- aplicação multipáginas;
- Dashboard Climático;
- Radar Ambiental;
- página Desmatamento PRODES;
- página Base de Dados;
- API FastAPI;
- integração Streamlit/FastAPI;
- API publicada;
- aplicação Streamlit publicada;
- integração online funcionando;
- repositório GitHub.

---

## Preparação para LLM

O TP3 também prepara o projeto para futuras aplicações com Large Language Models.

Possíveis usos:

- resumo de notícias;
- classificação temática;
- análise de sentimento;
- perguntas e respostas;
- geração de relatórios;
- interpretação de indicadores ambientais.

Os cálculos continuarão sendo realizados com Python e Pandas.

O LLM poderá ser utilizado principalmente para explicar, resumir e interpretar os resultados.

---

## Critérios de Sucesso

O projeto será considerado bem-sucedido quando:

- as fontes forem coletadas corretamente;
- os dados forem apresentados de forma clara;
- a navegação multipáginas funcionar;
- os filtros e controles funcionarem;
- o WebScraping gerar dados utilizáveis;
- o Selenium coletar corretamente os dados dinâmicos;
- os dados PRODES forem apresentados na aplicação;
- a FastAPI responder corretamente;
- os endpoints GET e POST funcionarem;
- o Streamlit consumir a API;
- os registros enviados forem armazenados;
- a aplicação Streamlit estiver publicada;
- a FastAPI estiver publicada;
- a integração online entre Streamlit e FastAPI funcionar;
- a documentação estiver atualizada;
- o projeto estiver preparado para integração futura com LLM.

---

## Riscos e Limitações

As principais limitações são:

- dependência de fontes externas;
- mudanças na estrutura HTML podem afetar o WebScraping;
- alterações no TerraBrasilis podem exigir ajustes no Selenium;
- Selenium possui maior custo computacional;
- arquivos CSV possuem limitações para alto volume e múltiplos usuários;
- serviços gratuitos de hospedagem podem apresentar maior tempo de resposta após períodos de inatividade;
- futuras respostas de LLM precisarão ser validadas.

---

## Status Atual

Ao final do TP2, o projeto já possuía:

- dados meteorológicos;
- WebScraping de notícias;
- visualizações;
- análise textual;
- upload e download;
- cache;
- estado de sessão;
- GitHub;
- deploy Streamlit.

No TP3 foram adicionados:

- aplicação multipáginas;
- menu de navegação;
- nova página PRODES;
- coleta com Selenium;
- dados históricos de desmatamento;
- FastAPI;
- endpoints GET e POST;
- integração Streamlit/FastAPI;
- publicação da FastAPI no Render;
- integração online com o Streamlit Community Cloud;
- preparação para uso de LLM.

---

## Próximas Etapas

As próximas evoluções possíveis incluem:

- integração com LLM;
- resumo automático de notícias;
- classificação textual;
- perguntas e respostas;
- geração de relatórios ambientais;
- novos indicadores;
- novas fontes de dados;
- migração de CSV para banco de dados.

---

## Conclusão

O EcoMonitor Brasil evoluiu de um dashboard ambiental para uma aplicação multipáginas capaz de integrar diferentes formas de aquisição e disponibilização de dados.

O projeto utiliza:

- API externa;
- WebScraping;
- Selenium;
- arquivos CSV;
- Streamlit;
- FastAPI.

Além da aplicação Streamlit publicada no Streamlit Community Cloud, a FastAPI também foi publicada no Render.

A comunicação entre os dois serviços foi validada em ambiente online, permitindo consultas e envio de dados através da aplicação publicada.

A arquitetura atual separa coleta, processamento, visualização e acesso aos dados, tornando o projeto mais organizado e preparado para futuras funcionalidades baseadas em Inteligência Artificial.
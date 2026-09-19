# EcoMonitor Brasil

## Descrição

O EcoMonitor Brasil é uma aplicação voltada ao monitoramento de indicadores ambientais e de sustentabilidade.

O projeto tem como objetivo integrar dados públicos provenientes de diferentes fontes e apresentá-los de forma clara e interativa, facilitando o acompanhamento de informações relacionadas ao clima, queimadas, desmatamento e outros indicadores ambientais.

O projeto está alinhado ao pilar Ambiental do ESG e aos Objetivos de Desenvolvimento Sustentável da Agenda 2030.

## ODS Relacionados

- ODS 13 — Ação Contra a Mudança Global do Clima
- ODS 15 — Vida Terrestre

## Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Requests

Nas próximas etapas, o projeto poderá incorporar:

- WebScraping
- APIs adicionais
- Machine Learning
- Inteligência Artificial Generativa
- LLMs

## Estrutura do Projeto

```text
ecomonitor-brasil/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── docs/
│   ├── project_charter.md
│   └── data_summary_report.md
│
├── notebooks/
│   └── exploracao.ipynb
│
├── src/
│   ├── data/
│   ├── analysis/
│   └── visualization/
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalação

Crie e ative um ambiente virtual.

No Windows:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\activate
```

Depois, instale as dependências do projeto:

```powershell
pip install -r requirements.txt
```

## Execução

Para executar a aplicação Streamlit, utilize:

```powershell
streamlit run app/app.py
```

## Fontes de Dados Planejadas

As principais fontes de dados previstas para o projeto são:

- Open-Meteo
- IBGE
- INPE
- Portal Brasileiro de Dados Abertos

## Metodologia

O desenvolvimento do EcoMonitor Brasil será orientado pelos métodos CRISP-DM e TDSP.

Essas metodologias serão utilizadas para organizar as etapas de:

- entendimento do problema de negócio;
- aquisição e compreensão dos dados;
- preparação dos dados;
- análise e modelagem;
- avaliação dos resultados;
- implantação da aplicação.

## Objetivo Final

Ao final do projeto, o EcoMonitor Brasil deverá disponibilizar um dashboard interativo desenvolvido em Python e Streamlit, integrando diferentes fontes de dados ambientais.

Nas etapas posteriores, o projeto também poderá utilizar WebScraping, APIs e modelos de linguagem de grande escala para gerar análises e apoiar a interpretação dos indicadores ambientais.
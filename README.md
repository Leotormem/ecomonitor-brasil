# EcoMonitor Brasil

Plataforma Inteligente para Monitoramento de Indicadores Ambientais e Sustentabilidade.

O EcoMonitor Brasil é uma aplicação desenvolvida em Python com Streamlit para integrar, organizar, analisar e visualizar diferentes tipos de dados ambientais.

O projeto trabalha com dados climáticos, notícias ambientais, informações históricas de desmatamento e registros enviados pelo usuário, além de disponibilizar parte dos dados através de uma API desenvolvida com FastAPI.

Na etapa atual, o projeto também integra um modelo de linguagem executado localmente para classificação temática de textos ambientais.

O projeto está relacionado principalmente ao pilar **Environmental (E)** do ESG e aos seguintes Objetivos de Desenvolvimento Sustentável:

- ODS 13 — Ação Contra a Mudança Global do Clima;
- ODS 15 — Vida Terrestre.

---

## Links do Projeto

### Repositório GitHub

https://github.com/Leotormem/ecomonitor-brasil

### Aplicação Streamlit

https://ecomonitor-brasil-wqhkx2ffy8cqvappehedvjy.streamlit.app/

### API EcoMonitor

https://ecomonitor-api-7pvm.onrender.com

### Documentação da API

https://ecomonitor-api-7pvm.onrender.com/docs

> A integração com o modelo de linguagem do TP4 foi desenvolvida e validada para execução local. A versão publicada no Render pode não executar o modelo local devido às limitações computacionais do plano gratuito.

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
- endpoints POST;
- integração entre Streamlit e FastAPI;
- API publicada no Render;
- Streamlit publicado no Streamlit Community Cloud;
- modelo de linguagem executado localmente;
- classificação temática de textos ambientais;
- endpoint `POST /processar_texto`;
- validação de entrada e saída com Pydantic;
- tratamento de erros HTTP;
- benchmark comparativo de modelos de linguagem.

---

# Páginas da Aplicação

## Início

Apresenta uma visão geral do projeto, objetivos, ODS relacionados e acesso às principais funcionalidades.

## Dashboard Climático

Permite consultar dados meteorológicos por localidade.

Principais indicadores:

- temperatura máxima;
- temperatura mínima;
- precipitação.

Os dados são obtidos através da Open-Meteo.

## Radar Ambiental

Apresenta notícias ambientais coletadas do INPE.

Inclui:

- tabela de notícias;
- links;
- contagem de notícias;
- análise de palavras;
- nuvem de palavras.

## Desmatamento PRODES

Apresenta dados históricos de desmatamento do PRODES/INPE.

Inclui:

- filtro por UF;
- filtro por período;
- maior área desmatada;
- ano de maior desmatamento;
- média anual;
- série histórica;
- comparação entre estados.

## API EcoMonitor

Demonstra a integração da aplicação Streamlit com a API desenvolvida em FastAPI.

Permite:

- verificar o status da API;
- consultar dados PRODES;
- consultar notícias;
- enviar registros ambientais;
- visualizar registros armazenados.

## Base de Dados

Permite:

- upload de arquivos CSV;
- visualização dos dados;
- análise de tipos;
- identificação de valores nulos;
- estatísticas descritivas;
- download de arquivos.

## Sobre

Apresenta informações gerais sobre o projeto, tecnologias, ESG, ODS e evolução da aplicação.

---

# Fontes de Dados

## Open-Meteo

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

## INPE

Utilizado como fonte de notícias ambientais.

Método:

- Requests;
- BeautifulSoup.

Arquivo gerado:

`data/processed/noticias_inpe.csv`

---

## PRODES / TerraBrasilis / INPE

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

# Coleta com Selenium

A coleta PRODES utiliza Selenium porque os dados não estão disponíveis diretamente no HTML inicial da página.

O fluxo utilizado é:

```text
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
```

O script está localizado em:

`src/data/coleta_prodes_selenium.py`

A coleta é executada separadamente da aplicação Streamlit.

---

# API EcoMonitor Brasil

O projeto possui uma API própria desenvolvida com FastAPI.

Arquivo principal:

`api/main.py`

A API está publicada no Render:

https://ecomonitor-api-7pvm.onrender.com

## GET /

Retorna informações sobre o status da API.

## GET /prodes

Consulta os dados históricos de desmatamento.

Permite filtros por:

- UF;
- ano.

## GET /noticias

Retorna as notícias ambientais coletadas.

## POST /registros

Permite inserir novos registros ambientais.

Campos:

- localidade;
- indicador;
- valor;
- unidade;
- fonte.

## GET /registros

Retorna os registros ambientais armazenados.

## POST /processar_texto

Endpoint desenvolvido no TP4 para classificação temática de textos ambientais utilizando modelo executado localmente.

Entrada esperada:

```json
{
  "texto": "Satélites registram aumento da área desmatada em região da Amazônia.",
  "tipo_analise": "classificacao"
}
```

Exemplo de resposta:

```json
{
  "tipo_analise": "classificacao",
  "texto": "Satélites registram aumento da área desmatada em região da Amazônia.",
  "categoria_sugerida": "desmatamento",
  "confianca": 0.7408,
  "pistas": [],
  "motor": "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
}
```

Categorias disponíveis:

- queimada;
- desmatamento;
- clima;
- biodiversidade;
- poluicao;
- monitoramento_ambiental.

---

# Modelo de Linguagem — TP4

A tarefa escolhida para integração com modelo de linguagem foi a **classificação temática de textos ambientais**.

O objetivo é receber um texto e classificá-lo em uma das categorias ambientais definidas pelo EcoMonitor Brasil.

## Modelo escolhido

O modelo selecionado foi:

`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`

O modelo utiliza classificação zero-shot e pode executar a tarefa sem treinamento adicional específico para o projeto.

---

# Avaliação dos Modelos

Foi criado um banco de provas com 30 textos ambientais rotulados manualmente antes da execução dos modelos.

Arquivo:

`data/analisador/banco_de_provas.csv`

As seis categorias possuem cinco exemplos cada.

## mDeBERTa multilingual zero-shot

Resultados:

- exemplos avaliados: 30;
- acertos: 24;
- erros: 6;
- acurácia: 80,00%;
- tempo médio por texto: 3,58 segundos;
- tempo de carregamento: 4,01 segundos.

## Qwen2.5-1.5B-Instruct

Modelo comparado:

`Qwen/Qwen2.5-1.5B-Instruct`

Resultados:

- exemplos avaliados: 30;
- acertos: 12;
- erros: 18;
- respostas sem categoria válida: 2;
- acurácia: 40,00%;
- tempo médio por texto: 6,39 segundos;
- tempo de carregamento: 5,58 segundos.

## Comparação

| Modelo | Acertos | Acurácia | Tempo médio | Carregamento |
|---|---:|---:|---:|---:|
| mDeBERTa multilingual zero-shot | 24/30 | 80,00% | 3,58 s | 4,01 s |
| Qwen2.5-1.5B-Instruct | 12/30 | 40,00% | 6,39 s | 5,58 s |

O mDeBERTa apresentou melhor desempenho e menor tempo médio de processamento para a tarefa escolhida.

---

# Custo Computacional do Modelo

O modelo mDeBERTa possui aproximadamente:

- 278.811.651 parâmetros;
- 531,79 MB de memória para armazenamento dos parâmetros;
- aproximadamente 0,52 GB.

Além disso:

- tempo médio de processamento: 3,58 segundos por texto;
- tempo de carregamento: 4,01 segundos.

A medição foi realizada localmente com PyTorch.

O resultado apresentou uma relação adequada entre desempenho e custo computacional para execução local no projeto.

---

# Justificativa da Escolha

A escolha do mDeBERTa considerou três critérios principais.

## Desempenho

O modelo alcançou 80,00% de acurácia no banco de provas próprio do EcoMonitor Brasil.

O Qwen2.5-1.5B-Instruct alcançou 40,00%.

## Custo Computacional

O mDeBERTa apresentou aproximadamente 0,52 GB de parâmetros e tempo médio de 3,58 segundos por classificação.

## Acessibilidade

O modelo pode ser obtido através da Hugging Face e executado localmente com Transformers e PyTorch.

Após o download, a aplicação utiliza:

`local_files_only=True`

Isso evita a necessidade de acessar serviços externos durante a inferência.

---

# Download Local do Modelo

O download é realizado separadamente da execução da API.

Script:

`src/baixar_modelo.py`

Para instalar as dependências:

```powershell
pip install -r requirements-llm.txt
```

Depois execute:

```powershell
python -m src.baixar_modelo
```

Resultado esperado:

```text
Baixando tokenizer...
Baixando modelo...
Modelo baixado e armazenado no cache local com sucesso.
```

Depois desse processo, o modelo fica disponível no cache local da Hugging Face.

---

# Carregamento do Modelo

O código responsável pelo modelo está em:

`src/analysis/analisador_llm.py`

O modelo é carregado pela API apenas uma vez durante a inicialização da aplicação.

A API utiliza o mecanismo `lifespan` do FastAPI.

Fluxo:

```text
Inicialização da FastAPI
        ↓
      lifespan
        ↓
carregar_modelo()
        ↓
modelo armazenado em memória
        ↓
requisições /processar_texto
        ↓
reutilização do mesmo modelo
```

Esse processo evita recarregar o modelo a cada requisição.

---

# Execução Local do TP4

## 1. Criar ambiente virtual

No PowerShell:

```powershell
python -m venv .venv
```

## 2. Ativar o ambiente

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Instalar dependências do modelo

```powershell
pip install -r requirements-llm.txt
```

O arquivo `requirements-llm.txt` inclui as dependências da API e também:

- transformers;
- torch;
- sentencepiece.

## 4. Baixar o modelo

```powershell
python -m src.baixar_modelo
```

## 5. Executar a API

```powershell
uvicorn api.main:app
```

A API ficará disponível em:

`http://127.0.0.1:8000`

Swagger:

`http://127.0.0.1:8000/docs`

---

# Validação com Pydantic

A rota `POST /processar_texto` utiliza modelos diferentes para entrada e saída.

## Entrada

Modelo:

`PedidoAnalise`

Regras principais:

- texto obrigatório;
- mínimo de 15 caracteres;
- máximo de 2000 caracteres;
- remoção automática de espaços nas extremidades;
- apenas o tipo `classificacao`;
- campos adicionais são proibidos.

## Saída

Modelo:

`ResultadoAnalise`

Campos:

- tipo_analise;
- texto;
- categoria_sugerida;
- confianca;
- pistas;
- motor.

A confiança é validada para permanecer entre 0 e 1.

---

# Tratamento de Erros

A integração implementa tratamento de erros HTTP.

## 422 — Entrada inválida

É retornado automaticamente pelo Pydantic em situações como:

- texto com menos de 15 caracteres;
- texto maior que o limite permitido;
- campo não reconhecido;
- tipo de análise inválido.

Exemplo testado:

```json
{
  "texto": "curto",
  "tipo_analise": "classificacao"
}
```

Resultado:

`422 Unprocessable Content`

Também foi validada a rejeição de campos adicionais através de:

`extra="forbid"`

## 503 — Modelo indisponível

Caso o modelo não esteja carregado, a API retorna:

`503 Service Unavailable`

Mensagem:

```text
Modelo de análise indisponível. Verifique se o modelo foi baixado e carregado corretamente.
```

## 500 — Erro interno de processamento

Caso ocorra uma falha inesperada durante a inferência do modelo, a API retorna:

`500 Internal Server Error`

com mensagem controlada para evitar exposição de detalhes internos da aplicação.

---

# Documentação da API

A documentação automática é gerada pelo FastAPI através do Swagger.

Localmente:

`http://127.0.0.1:8000/docs`

Na versão publicada:

https://ecomonitor-api-7pvm.onrender.com/docs

A interface permite:

- consultar endpoints;
- visualizar parâmetros;
- visualizar modelos de entrada;
- visualizar modelos de resposta;
- executar requisições;
- verificar status HTTP;
- visualizar respostas JSON.

---

# Como Executar o Projeto Localmente

## Aplicação Streamlit

Instale:

```powershell
pip install -r requirements.txt
```

Execute:

```powershell
streamlit run app/app.py
```

Endereço esperado:

`http://localhost:8501`

---

## API FastAPI sem LLM

Dependências básicas:

```powershell
pip install -r requirements-api.txt
```

---

## API FastAPI com LLM — TP4

Instale:

```powershell
pip install -r requirements-llm.txt
```

Baixe o modelo:

```powershell
python -m src.baixar_modelo
```

Execute:

```powershell
uvicorn api.main:app
```

Swagger:

`http://127.0.0.1:8000/docs`

---

# Executar a Coleta PRODES

Para instalar as dependências:

```powershell
pip install -r requirements-coleta.txt
```

Execute:

```powershell
python src/data/coleta_prodes_selenium.py
```

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

# Integração em Produção

A aplicação publicada no Streamlit Community Cloud se comunica com a API publicada no Render para as funcionalidades desenvolvidas anteriormente.

Fluxo:

```text
Usuário
  ↓
Streamlit Community Cloud
  ↓
FastAPI no Render
  ↓
Dados processados
```

Aplicação:

https://ecomonitor-brasil-wqhkx2ffy8cqvappehedvjy.streamlit.app/

API:

https://ecomonitor-api-7pvm.onrender.com

A funcionalidade de classificação com mDeBERTa do TP4 foi desenvolvida para execução local.

O modelo possui custo computacional superior às funções tradicionais da API e a publicação em serviços gratuitos pode ser limitada pela quantidade de memória, armazenamento e tempo de inicialização disponíveis.

---

# Estrutura Principal do Projeto

```text
ecomonitor-brasil/
│
├── api/
│   └── main.py
│
├── app/
│   ├── app.py
│   └── paginas/
│       ├── inicio.py
│       ├── clima.py
│       ├── radar_ambiental.py
│       ├── desmatamento.py
│       ├── api_ecomonitor.py
│       ├── dados.py
│       └── sobre.py
│
├── data/
│   ├── analisador/
│   │   ├── banco_de_provas.csv
│   │   ├── resultado_mdeberta.csv
│   │   └── resultado_qwen.csv
│   ├── external/
│   ├── processed/
│   │   ├── noticias_inpe.csv
│   │   ├── desmatamento_prodes.csv
│   │   └── registros_ambientais.csv
│   └── raw/
│       └── terrabrasilis_prodes_renderizado.html
│
├── docs/
│   ├── project_charter.md
│   ├── data_summary_report.md
│   └── escolha_do_modelo.md
│
├── notebooks/
│   └── exploracao.ipynb
│
├── src/
│   ├── baixar_modelo.py
│   ├── analysis/
│   │   ├── analisador_llm.py
│   │   ├── testar_modelo_zero_shot.py
│   │   ├── avaliar_modelo_zero_shot.py
│   │   ├── testar_qwen.py
│   │   ├── avaliar_qwen.py
│   │   └── medir_memoria_mdeberta.py
│   ├── data/
│   │   ├── coleta_open_meteo.py
│   │   ├── coleta_noticias_inpe.py
│   │   ├── coleta_prodes_selenium.py
│   │   └── validar_banco_provas.py
│   └── visualization/
│
├── tests/
│
├── README.md
├── requirements.txt
├── requirements-api.txt
├── requirements-coleta.txt
└── requirements-llm.txt
```

---

# Principais Arquivos de Dados

## noticias_inpe.csv

Contém:

- título;
- URL.

Utilizado no Radar Ambiental e na API.

## desmatamento_prodes.csv

Contém:

- UF;
- Ano;
- Area_km2.

Utilizado na página Desmatamento PRODES e na API.

## registros_ambientais.csv

Contém registros enviados através da API.

Campos:

- localidade;
- indicador;
- valor;
- unidade;
- fonte.

## banco_de_provas.csv

Contém os exemplos utilizados para avaliar os modelos de linguagem.

Possui:

- 30 textos;
- 6 categorias;
- 5 textos por categoria.

Os rótulos foram definidos antes da avaliação dos modelos.

## resultado_mdeberta.csv

Armazena os resultados individuais do benchmark do mDeBERTa.

## resultado_qwen.csv

Armazena os resultados individuais do benchmark do Qwen2.5-1.5B-Instruct.

---

# Tecnologias Utilizadas

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
- Transformers;
- Hugging Face;
- PyTorch;
- SentencePiece;
- Git;
- GitHub;
- Streamlit Community Cloud;
- Render;
- Visual Studio Code.

---

# Metodologia

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

No desenvolvimento do TP4 também foi aplicado um processo experimental para seleção do modelo:

1. definição da tarefa;
2. criação do banco de provas;
3. rotulação manual;
4. execução dos modelos;
5. medição de desempenho;
6. medição de tempo;
7. avaliação do custo computacional;
8. seleção do modelo;
9. integração com FastAPI;
10. validação da entrada e saída;
11. testes de erros HTTP.

---

# Escolha do Modelo

A documentação detalhada da avaliação dos modelos está disponível em:

`docs/escolha_do_modelo.md`

Esse documento apresenta:

- tarefa selecionada;
- critérios de avaliação;
- banco de provas;
- resultados do mDeBERTa;
- resultados do Qwen;
- custo computacional;
- comparação;
- justificativa da escolha;
- plano B.

---

# Limitações Atuais

Algumas limitações do projeto são:

- dependência da disponibilidade das fontes externas;
- mudanças no HTML podem afetar o WebScraping;
- mudanças no TerraBrasilis podem exigir ajustes no Selenium;
- Selenium possui maior custo computacional;
- os registros da API são armazenados em CSV;
- serviços gratuitos de hospedagem podem apresentar maior tempo de resposta após períodos de inatividade;
- arquivos CSV possuem limitações para cenários com grande volume de dados ou muitos usuários simultâneos;
- os registros enviados por `POST /registros` são armazenados atualmente em arquivo CSV no disco do serviço Render;
- no plano gratuito do Render, esse armazenamento é efêmero, portanto os dados podem ser perdidos após reinicializações, reconstruções ou novos deploys do serviço;
- o modelo mDeBERTa demanda mais memória e processamento do que os endpoints tradicionais da API;
- o tempo médio de classificação medido no ambiente de desenvolvimento foi de aproximadamente 3,58 segundos por texto;
- a execução do modelo em hospedagens gratuitas pode ser limitada pela memória disponível;
- a funcionalidade do modelo local depende do download prévio dos arquivos necessários.

---

# Documentação

A documentação principal do projeto está disponível em:

`docs/project_charter.md`

`docs/data_summary_report.md`

`docs/escolha_do_modelo.md`

O Project Charter apresenta os objetivos, escopo e evolução do projeto.

O Data Summary Report apresenta as fontes, estruturas, tratamentos, validações e limitações dos dados.

O documento de escolha do modelo registra a metodologia e os resultados utilizados para selecionar o modelo local do TP4.

---

# Status Atual

O projeto atualmente possui:

- aplicação Streamlit multipáginas;
- dashboard climático funcional;
- notícias ambientais coletadas;
- análise textual;
- dados históricos PRODES;
- coleta dinâmica com Selenium;
- FastAPI funcional;
- endpoints GET e POST;
- FastAPI publicada no Render;
- Streamlit publicado no Streamlit Community Cloud;
- integração online Streamlit/FastAPI;
- banco de provas para avaliação de modelos;
- comparação entre mDeBERTa e Qwen;
- modelo local selecionado;
- classificação ambiental com mDeBERTa;
- endpoint `POST /processar_texto`;
- request model;
- response model;
- validação Pydantic;
- tratamento de erros 422;
- tratamento de erro 503;
- tratamento de erro 500;
- download separado do modelo;
- carregamento único através de lifespan;
- execução local sem dependência de API externa de IA;
- documentação atualizada.

---

# Próximas Etapas

Possíveis evoluções futuras incluem:

- integrar a classificação com IA diretamente à interface Streamlit;
- classificação automática das notícias ambientais;
- resumo de notícias;
- perguntas e respostas;
- geração automática de relatórios;
- novas fontes de dados;
- novos indicadores ambientais;
- migração da persistência em CSV para banco de dados;
- avaliação de modelos adicionais;
- otimização ou quantização do modelo para reduzir consumo de memória;
- implantação do processamento de IA em infraestrutura compatível com o custo computacional do modelo.

---

# Autor

Projeto acadêmico desenvolvido para aplicação de conceitos de Ciência de Dados, Engenharia de Dados, WebScraping, APIs, modelos de linguagem, visualização de dados e sustentabilidade.
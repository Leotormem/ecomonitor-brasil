# Data Summary Report — EcoMonitor Brasil

## Objetivo

Este documento apresenta as fontes de dados utilizadas no EcoMonitor Brasil, os tipos de dados coletados, a forma de aquisição, o armazenamento e o objetivo de uso dessas informações dentro da aplicação.

O Data Summary Report foi atualizado no TP2 para refletir a evolução do projeto, que passou a integrar dados provenientes de API, WebScraping e arquivos enviados pelo usuário.

## Fontes de Dados

### 1. Open-Meteo

**Tipo de fonte:** API REST pública.

**Forma de coleta:** requisições HTTP utilizando a biblioteca `requests`.

**Dados coletados:**
- data;
- temperatura máxima;
- temperatura mínima;
- precipitação.

**Objetivo de uso:**
fornecer dados meteorológicos para diferentes cidades brasileiras e permitir a visualização de indicadores climáticos na aplicação.

**Formato dos dados:**
JSON convertido para DataFrame utilizando Pandas.

**Armazenamento:**
os dados coletados são salvos em arquivos CSV no diretório:

`data/raw/`

**Exemplo:**

`data/raw/open_meteo_cuiaba_mt.csv`

## 2. INPE — Notícias Ambientais

**Tipo de fonte:** página web pública.

**Forma de coleta:** WebScraping.

**Tecnologias utilizadas:**
- Requests;
- BeautifulSoup.

**Dados coletados:**
- título da notícia;
- URL da notícia.

**Objetivo de uso:**
complementar os indicadores ambientais com informações e notícias relacionadas a clima, meio ambiente, monitoramento ambiental e sustentabilidade.

Antes da coleta, é realizada a verificação das permissões de acesso por meio do arquivo `robots.txt`.

O código de WebScraping é executado separadamente da aplicação Streamlit.

**Armazenamento:**
os dados coletados são salvos em:

`data/processed/noticias_inpe.csv`

A aplicação Streamlit apenas lê o arquivo processado, evitando executar a raspagem durante a interação do usuário.

## 3. Arquivos CSV enviados pelo usuário

**Tipo de fonte:** arquivo externo fornecido pelo usuário.

**Forma de entrada:** upload realizado através da aplicação Streamlit utilizando `st.file_uploader`.

**Formato aceito:**
CSV.

**Objetivo de uso:**
permitir que o usuário complemente as informações existentes na aplicação com novos conjuntos de dados.

Os arquivos enviados são validados antes da utilização.

Após a leitura, os dados são exibidos em formato de tabela e podem ser novamente exportados em CSV.

## Tipos de Dados

Os dados utilizados no projeto incluem diferentes tipos de informação.

### Dados Numéricos

Exemplos:
- temperatura máxima;
- temperatura mínima;
- precipitação;
- quantidade de notícias;
- frequência de palavras;
- quantidade de linhas e colunas de arquivos enviados.

### Dados Temporais

Exemplo:
- datas associadas aos registros meteorológicos.

### Dados Textuais

Exemplos:
- títulos de notícias ambientais;
- palavras extraídas dos títulos.

Esses dados são utilizados para geração de estatísticas e nuvem de palavras.

### Dados Categóricos

Exemplos:
- cidade selecionada;
- indicador ambiental escolhido pelo usuário.

### Dados de Referência

Exemplos:
- URLs das notícias ambientais;
- identificação da fonte dos dados.

## Processamento dos Dados

Os dados passam por diferentes etapas antes de serem utilizados pela aplicação.

### Dados da Open-Meteo

Fluxo:

1. requisição à API;
2. recebimento dos dados em JSON;
3. conversão para DataFrame;
4. organização das colunas;
5. armazenamento em CSV;
6. visualização no Streamlit.

### Notícias do INPE

Fluxo:

1. verificação do `robots.txt`;
2. requisição da página;
3. processamento do HTML com BeautifulSoup;
4. identificação dos links e títulos das notícias;
5. remoção de duplicidades;
6. conversão para DataFrame;
7. armazenamento em CSV;
8. leitura do arquivo pela aplicação;
9. geração de estatísticas e nuvem de palavras.

### Arquivos enviados pelo usuário

Fluxo:

1. upload do CSV;
2. tentativa de leitura utilizando Pandas;
3. validação básica;
4. criação de DataFrame;
5. armazenamento temporário em estado de sessão;
6. visualização na interface;
7. disponibilização para download.

## Organização dos Diretórios

A organização dos dados segue a estrutura definida para o projeto.

```text
data/
├── raw/
│   └── dados coletados diretamente das APIs
│
├── processed/
│   └── noticias_inpe.csv
│
└── external/
    └── espaço destinado a fontes externas adicionais
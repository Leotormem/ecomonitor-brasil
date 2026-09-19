# Data Summary Report — EcoMonitor Brasil

## Objetivo

Este documento apresenta o primeiro levantamento das fontes de dados que poderão ser utilizadas no desenvolvimento do EcoMonitor Brasil.

As fontes foram selecionadas considerando a disponibilidade pública dos dados, a relação com os Objetivos de Desenvolvimento Sustentável e a possibilidade de integração com Python.

## Fontes de Dados

### Open-Meteo

**Tipo de fonte:** API REST pública.

**Dados disponíveis:** temperatura, precipitação, velocidade do vento, umidade e outras informações meteorológicas.

**Objetivo de uso:** fornecer dados climáticos que possam ser utilizados para acompanhar condições ambientais e analisar variações ao longo do tempo.

### IBGE

**Tipo de fonte:** API e bases públicas.

**Dados disponíveis:** informações sobre estados, municípios, regiões e outros dados geográficos e socioeconômicos.

**Objetivo de uso:** auxiliar na organização geográfica dos dados e permitir que os indicadores ambientais sejam relacionados a diferentes localidades brasileiras.

### INPE

**Tipo de fonte:** bases públicas e serviços de dados ambientais.

**Dados disponíveis:** informações relacionadas a queimadas, focos de calor, desmatamento e monitoramento ambiental.

**Objetivo de uso:** permitir o acompanhamento de eventos ambientais relacionados ao ODS 13 e ao ODS 15, especialmente queimadas e alterações na cobertura vegetal.

### Portal Brasileiro de Dados Abertos

**Tipo de fonte:** conjuntos de dados públicos disponibilizados por diferentes órgãos governamentais.

**Dados disponíveis:** informações ambientais, territoriais e relacionadas à sustentabilidade.

**Objetivo de uso:** complementar o projeto com novos indicadores e bases públicas relevantes durante as próximas etapas.

## Tipos de Dados Esperados

Os dados utilizados no projeto poderão incluir:

- dados numéricos, como temperatura, precipitação e quantidade de focos de calor;
- dados temporais, como data e horário dos registros;
- dados geográficos, como estado, município, latitude e longitude;
- dados categóricos relacionados aos diferentes tipos de indicadores ambientais.

## Forma de Utilização

Os dados serão inicialmente coletados por meio de APIs e bases públicas.

Em seguida, serão tratados e organizados utilizando Python.

Os dados originais serão armazenados na pasta:

`data/raw`

Os dados tratados e preparados para análise serão armazenados na pasta:

`data/processed`

Nas etapas seguintes do projeto, essas informações serão utilizadas para construir gráficos, indicadores e análises dentro do dashboard desenvolvido em Streamlit.

## Considerações Iniciais

As fontes apresentadas neste documento representam o planejamento inicial do projeto.

Durante o desenvolvimento dos próximos TPs, poderão ser adicionadas, substituídas ou ajustadas fontes de dados de acordo com a disponibilidade, qualidade e relevância das informações encontradas.
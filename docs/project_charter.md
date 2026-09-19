# Project Charter — EcoMonitor Brasil

## Nome do Projeto

**EcoMonitor Brasil — Plataforma Inteligente para Monitoramento de Indicadores Ambientais e Sustentabilidade**

## Problema de Negócio

Dados ambientais importantes, como informações relacionadas ao clima, queimadas, desmatamento e outros indicadores de sustentabilidade, encontram-se distribuídos em diferentes fontes públicas.

Essa fragmentação dificulta a análise conjunta das informações, o acompanhamento de tendências e a identificação de riscos e situações críticas.

O EcoMonitor Brasil busca resolver esse problema por meio de uma aplicação interativa capaz de reunir dados ambientais e informações externas em um único ambiente, facilitando a visualização, a análise e o acompanhamento de indicadores relacionados à sustentabilidade.

## Objetivo Geral

Desenvolver uma aplicação interativa em Python e Streamlit capaz de integrar, organizar, analisar e apresentar dados ambientais provenientes de diferentes fontes públicas, oferecendo suporte ao acompanhamento de indicadores relacionados à sustentabilidade e às mudanças climáticas.

## Objetivos Específicos

- Integrar fontes públicas de dados ambientais.
- Realizar coleta de dados por meio de APIs.
- Utilizar WebScraping para obter informações de páginas web.
- Organizar e armazenar os dados coletados em arquivos estruturados.
- Desenvolver uma interface interativa em Streamlit.
- Permitir ao usuário selecionar localidades e indicadores ambientais.
- Apresentar métricas, gráficos e tabelas de forma dinâmica.
- Exibir notícias ambientais coletadas por WebScraping.
- Gerar estatísticas básicas a partir dos dados coletados.
- Criar nuvens de palavras com base no conteúdo das notícias ambientais.
- Utilizar cache para melhorar o desempenho da aplicação.
- Utilizar estado de sessão para manter informações durante a interação do usuário.
- Permitir upload e download de arquivos CSV.
- Disponibilizar a aplicação por meio de deploy em ambiente web.
- Utilizar Git e GitHub para controle de versão do projeto.

## Pilar ESG

O projeto está relacionado principalmente ao pilar:

**Environmental (E) — Ambiental.**

A aplicação utiliza dados ambientais e climáticos com o objetivo de facilitar o acompanhamento de informações relacionadas à sustentabilidade e aos impactos ambientais.

## Objetivos de Desenvolvimento Sustentável

### ODS 13 — Ação Contra a Mudança Global do Clima

O EcoMonitor Brasil está diretamente alinhado ao ODS 13 ao permitir o acompanhamento de informações meteorológicas e ambientais, contribuindo para a observação de condições climáticas e para a conscientização sobre questões relacionadas às mudanças climáticas.

### ODS 15 — Vida Terrestre

O projeto também se relaciona ao ODS 15, principalmente por incorporar conteúdos e informações ambientais relacionadas a queimadas, desmatamento, ecossistemas terrestres e monitoramento ambiental.

## Público-Alvo

O público-alvo do EcoMonitor Brasil inclui:

- gestores públicos;
- empresas que desenvolvem ou acompanham iniciativas ESG;
- organizações ambientais;
- pesquisadores;
- instituições acadêmicas;
- estudantes;
- cidadãos interessados em sustentabilidade e monitoramento ambiental.

## Stakeholders

Os principais stakeholders do projeto são:

- usuários da aplicação;
- gestores públicos;
- organizações ambientais;
- empresas interessadas em ESG;
- pesquisadores e instituições acadêmicas;
- desenvolvedor responsável pelo projeto;
- instituições responsáveis pelas fontes públicas de dados utilizadas.

## Escopo do Projeto

O projeto contempla:

- desenvolvimento em Python;
- aplicação interativa utilizando Streamlit;
- coleta de dados por API;
- WebScraping com BeautifulSoup;
- armazenamento de dados em CSV;
- processamento e análise dos dados;
- criação de gráficos, métricas e tabelas;
- geração de nuvem de palavras;
- utilização de cache;
- utilização de estado de sessão;
- upload de arquivos CSV;
- download de dados processados;
- controle de versão com Git;
- armazenamento do código no GitHub;
- publicação da aplicação em ambiente web.

## Fontes Utilizadas

As principais fontes utilizadas até o TP2 são:

### Open-Meteo

Utilizada para coleta de dados meteorológicos, incluindo:

- temperatura máxima;
- temperatura mínima;
- precipitação.

A coleta é realizada por meio de API REST.

### INPE

Utilizado como fonte de informações ambientais e notícias.

As notícias são coletadas por meio de WebScraping utilizando:

- Requests;
- BeautifulSoup.

Os dados extraídos são armazenados em arquivo CSV antes de serem utilizados pela aplicação.

## Funcionalidades Implementadas

Até o TP2, foram implementadas as seguintes funcionalidades:

- seleção de cidades;
- escolha dos indicadores exibidos;
- exibição dinâmica de gráficos;
- exibição ou ocultação de tabelas;
- métricas de temperatura e precipitação;
- coleta de dados meteorológicos por API;
- coleta de notícias ambientais por WebScraping;
- armazenamento dos dados coletados em CSV;
- tabela com notícias ambientais e links;
- estatísticas básicas sobre os títulos das notícias;
- identificação das palavras mais frequentes;
- geração de nuvem de palavras;
- uso de cache com `st.cache_data`;
- uso de estado de sessão com `st.session_state`;
- upload de arquivos CSV;
- validação básica dos arquivos enviados;
- exibição de prévia dos dados enviados;
- download de arquivos CSV;
- controle de versão com Git;
- repositório remoto no GitHub;
- deploy da aplicação Streamlit.

## Estrutura Metodológica

O projeto utiliza os princípios das metodologias CRISP-DM e TDSP.

### CRISP-DM

As etapas aplicadas ao projeto incluem:

1. entendimento do negócio;
2. entendimento dos dados;
3. preparação dos dados;
4. análise e modelagem;
5. avaliação;
6. implantação.

### TDSP

O TDSP é utilizado principalmente para orientar:

- organização dos diretórios;
- aquisição e armazenamento de dados;
- separação entre coleta, processamento e interface;
- documentação do projeto;
- controle de versão;
- implantação da aplicação.

## Principais Entregáveis

Os principais entregáveis do projeto até o TP2 são:

- estrutura organizada de diretórios;
- Project Charter;
- Data Summary Report;
- scripts de coleta de dados;
- arquivos CSV com dados coletados;
- notebook de exploração;
- dashboard interativo em Streamlit;
- WebScraping com BeautifulSoup;
- estatísticas e nuvem de palavras;
- funcionalidade de upload e download;
- repositório Git/GitHub;
- aplicação publicada na web.

## Critérios de Sucesso

O projeto será considerado bem-sucedido quando:

- as fontes de dados forem coletadas corretamente;
- os dados forem apresentados de forma clara;
- os filtros e controles da aplicação funcionarem;
- o usuário puder interagir com os dados;
- a aplicação permitir integração de novos arquivos CSV;
- o WebScraping gerar dados utilizáveis;
- as informações externas forem incorporadas ao dashboard;
- a aplicação apresentar bom desempenho utilizando cache;
- o estado da sessão funcionar corretamente;
- o projeto estiver versionado e publicado;
- a aplicação puder ser acessada por meio de uma URL pública.

## Status Atual

Ao final do TP2, o EcoMonitor Brasil apresenta uma versão funcional e interativa, integrando dados meteorológicos via API, informações ambientais via WebScraping e dados complementares enviados pelo usuário.

A aplicação encontra-se organizada, versionada com Git, armazenada no GitHub e preparada para evolução nas próximas etapas do projeto.
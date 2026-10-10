import streamlit as st


# =========================================================
# CABEÇALHO
# =========================================================

st.title("🌎 Sobre o EcoMonitor Brasil")

st.caption(
    "Projeto voltado ao monitoramento ambiental, "
    "sustentabilidade e análise de dados públicos."
)

st.divider()


# =========================================================
# SOBRE O PROJETO
# =========================================================

col1, col2 = st.columns([1.4, 1])

with col1:

    with st.container(border=True):

        st.markdown("## 🎯 Sobre o Projeto")

        st.write(
            """
            O **EcoMonitor Brasil** é uma aplicação desenvolvida
            para integrar diferentes fontes de dados ambientais
            em uma única plataforma interativa.

            O projeto busca facilitar o acompanhamento de
            indicadores climáticos, notícias ambientais e
            informações relacionadas à sustentabilidade.

            A aplicação foi estruturada para evoluir de forma
            modular, permitindo a inclusão de novas fontes de dados,
            APIs próprias e, futuramente, recursos baseados em
            Inteligência Artificial.
            """
        )


with col2:

    with st.container(border=True):

        st.markdown("## 🌱 ESG e Agenda 2030")

        st.markdown(
            """
            **Pilar ESG principal**

            Ambiental — Environmental

            ---

            **ODS 13**

            Ação Contra a Mudança Global do Clima

            ---

            **ODS 15**

            Vida Terrestre
            """
        )


# =========================================================
# OBJETIVOS
# =========================================================

st.markdown("## 📌 Objetivos")

with st.container(border=True):

    st.markdown(
        """
        - Integrar fontes públicas de dados ambientais;
        - Facilitar a visualização de indicadores;
        - Permitir interação com diferentes conjuntos de dados;
        - Apoiar análises relacionadas à sustentabilidade;
        - Evoluir a aplicação para uma arquitetura multipáginas;
        - Integrar uma API própria utilizando FastAPI;
        - Preparar os dados para futuras aplicações com LLMs.
        """
    )


# =========================================================
# FONTES DE DADOS
# =========================================================

st.markdown("## 🔗 Fontes de Dados")

fonte1, fonte2 = st.columns(2)

with fonte1:

    with st.container(border=True):

        st.markdown("### 🌤️ Open-Meteo")

        st.write(
            """
            Utilizada para obtenção de dados meteorológicos,
            incluindo temperatura máxima, temperatura mínima
            e precipitação.
            """
        )

        st.markdown(
            "[Acessar Open-Meteo](https://open-meteo.com/)"
        )


with fonte2:

    with st.container(border=True):

        st.markdown("### 📰 INPE")

        st.write(
            """
            Utilizado como fonte de notícias ambientais
            coletadas por meio de Web Scraping.
            """
        )

        st.markdown(
            "[Acessar INPE](https://www.gov.br/inpe/)"
        )


# =========================================================
# TECNOLOGIAS
# =========================================================

st.markdown("## 🛠️ Tecnologias Utilizadas")

t1, t2, t3 = st.columns(3)

with t1:

    with st.container(border=True):

        st.markdown("### 💻 Aplicação")

        st.markdown(
            """
            - Python
            - Streamlit
            - Pandas
            - Matplotlib
            - WordCloud
            """
        )


with t2:

    with st.container(border=True):

        st.markdown("### 🌐 Coleta")

        st.markdown(
            """
            - Requests
            - BeautifulSoup
            - APIs públicas
            """
        )


with t3:

    with st.container(border=True):

        st.markdown("### 🔧 Desenvolvimento")

        st.markdown(
            """
            - Git
            - GitHub
            - VS Code
            - Streamlit Cloud
            """
        )


# =========================================================
# ARQUITETURA ATUAL
# =========================================================

st.markdown("## 🧭 Estrutura Atual da Aplicação")

with st.container(border=True):

    st.code(
        """
EcoMonitor Brasil
│
├── Início
├── Dashboard Climático
├── Radar Ambiental
├── Base de Dados
└── Sobre
        """,
        language="text",
    )

    st.write(
        """
        Cada página possui uma finalidade específica,
        permitindo uma navegação mais organizada e
        facilitando a evolução do projeto.
        """
    )


# =========================================================
# PRÓXIMAS ETAPAS
# =========================================================

st.markdown("## 🚀 Próximas Evoluções")

with st.container(border=True):

    st.markdown(
        """
        A próxima evolução do EcoMonitor Brasil incluirá:

        - integração com novas fontes de dados;
        - avaliação da necessidade de Selenium;
        - desenvolvimento de uma API com FastAPI;
        - integração entre Streamlit e FastAPI;
        - preparação dos dados para uso com LLMs;
        - geração automática de análises e insights ambientais.
        """
    )


# =========================================================
# NAVEGAÇÃO
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "paginas/inicio.py",
        label="← Voltar para o Início",
        icon="🏠",
    )

with col2:

    st.page_link(
        "paginas/dados.py",
        label="Ir para Base de Dados",
        icon="📂",
    )


# =========================================================
# RODAPÉ
# =========================================================

st.divider()

st.caption(
    "🌱 EcoMonitor Brasil • "
    "Dados, tecnologia e sustentabilidade."
)
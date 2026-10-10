import streamlit as st


# =========================================================
# PÁGINA INICIAL
# =========================================================

st.title("🌱 EcoMonitor Brasil")

st.markdown(
    "### Inteligência de dados aplicada ao monitoramento ambiental"
)

st.caption(
    "Clima • Sustentabilidade • Notícias ambientais • Agenda 2030"
)

st.divider()


# =========================================================
# APRESENTAÇÃO
# =========================================================

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):

        st.markdown("## 🌎 Sobre a Plataforma")

        st.write(
            """
            O **EcoMonitor Brasil** é uma plataforma interativa
            desenvolvida para reunir, organizar e visualizar
            dados ambientais provenientes de diferentes fontes.

            O projeto utiliza dados meteorológicos, informações
            ambientais e notícias públicas para facilitar
            o acompanhamento de indicadores relacionados
            à sustentabilidade.
            """
        )

with col2:
    with st.container(border=True):

        st.markdown("## 🎯 Foco ESG")

        st.markdown(
            """
            **Pilar principal**

            🌱 Ambiental — Environmental

            **ODS 13**

            Ação Contra a Mudança Global do Clima

            **ODS 15**

            Vida Terrestre
            """
        )


# =========================================================
# FUNCIONALIDADES
# =========================================================

st.markdown("## 📊 Funcionalidades")

f1, f2, f3 = st.columns(3)

with f1:
    with st.container(border=True):

        st.markdown("### 🌤️ Clima")

        st.write(
            """
            Consulte dados meteorológicos
            e acompanhe indicadores como
            temperatura e precipitação.
            """
        )

        st.page_link(
            "paginas/clima.py",
            label="Acessar Monitoramento Climático",
            icon="🌤️",
        )

with f2:
    with st.container(border=True):

        st.markdown("### 📰 Radar Ambiental")

        st.write(
            """
            Explore notícias ambientais
            coletadas de fontes públicas
            e análises textuais.
            """
        )

        st.page_link(
            "paginas/radar_ambiental.py",
            label="Acessar Radar Ambiental",
            icon="📰",
        )

with f3:
    with st.container(border=True):

        st.markdown("### 📂 Dados")

        st.write(
            """
            Envie arquivos CSV,
            visualize dados e exporte
            informações processadas.
            """
        )

        st.page_link(
            "paginas/dados.py",
            label="Acessar Base de Dados",
            icon="📂",
        )


# =========================================================
# FONTES
# =========================================================

st.markdown("## 🔗 Fontes Integradas")

fonte1, fonte2 = st.columns(2)

with fonte1:
    st.metric(
        "🌤️ Open-Meteo",
        "Dados Climáticos"
    )

with fonte2:
    st.metric(
        "📰 INPE",
        "Notícias Ambientais"
    )


# =========================================================
# PRÓXIMA EVOLUÇÃO
# =========================================================

with st.container(border=True):

    st.markdown("## 🚀 Evolução do Projeto")

    st.write(
        """
        Nesta nova etapa, o EcoMonitor Brasil está sendo
        evoluído para uma aplicação multipáginas,
        permitindo que cada funcionalidade possua
        seu próprio espaço de navegação.

        Nas próximas fases, o projeto também será
        integrado com APIs próprias e preparado para
        recursos de Inteligência Artificial.
        """
    )


# =========================================================
# RODAPÉ
# =========================================================

st.divider()

st.caption(
    "🌱 EcoMonitor Brasil • "
    "Dados e tecnologia para sustentabilidade"
)
import streamlit as st


# =========================================================
# CONFIGURAÇÃO GERAL
# =========================================================

st.set_page_config(
    page_title="EcoMonitor Brasil",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# NAVEGAÇÃO
# =========================================================

pagina = st.navigation(
    {
        "EcoMonitor Brasil": [
            st.Page(
                "paginas/inicio.py",
                title="Início",
                icon="🏠",
                default=True,
            ),
            st.Page(
                "paginas/clima.py",
                title="Dashboard Climático",
                icon="📊",
            ),
            st.Page(
                "paginas/radar_ambiental.py",
                title="Radar Ambiental",
                icon="📰",
            ),
            st.Page(
                "paginas/dados.py",
                title="Base de Dados",
                icon="📂",
            ),
        ],

        "Projeto": [
            st.Page(
                "paginas/sobre.py",
                title="Sobre",
                icon="🌎",
            ),
        ],
    }
)


# =========================================================
# EXECUTA A PÁGINA SELECIONADA
# =========================================================

pagina.run()
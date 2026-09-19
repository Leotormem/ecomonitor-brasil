import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# CONFIGURAÇÃO DO CAMINHO DO PROJETO
# ---------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.coleta_open_meteo import (
    CIDADES,
    coletar_dados_meteorologicos,
)


# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------

st.set_page_config(
    page_title="EcoMonitor Brasil",
    page_icon="🌱",
    layout="wide"
)


# ---------------------------------------------------------
# BARRA LATERAL
# ---------------------------------------------------------

st.sidebar.header("Configurações")

cidade_selecionada = st.sidebar.selectbox(
    "Selecione uma cidade:",
    options=list(CIDADES.keys())
)

indicadores = st.sidebar.multiselect(
    "Indicadores para exibir no gráfico:",
    options=[
        "Temperatura Máxima (°C)",
        "Temperatura Mínima (°C)",
        "Precipitação (mm)"
    ],
    default=[
        "Temperatura Máxima (°C)",
        "Temperatura Mínima (°C)"
    ]
)

mostrar_tabela = st.sidebar.checkbox(
    "Exibir tabela de dados",
    value=True
)


# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------

st.title("🌱 EcoMonitor Brasil")

st.subheader(
    "Plataforma Inteligente para Monitoramento de "
    "Indicadores Ambientais e Sustentabilidade"
)


# ---------------------------------------------------------
# PROBLEMA DE NEGÓCIO
# ---------------------------------------------------------

st.markdown("""
### Problema de Negócio

Dados ambientais importantes, como informações sobre clima,
queimadas, desmatamento e outros indicadores de sustentabilidade,
estão distribuídos em diferentes fontes públicas.

Essa fragmentação dificulta o acompanhamento conjunto dessas
informações e torna mais trabalhosa a identificação de tendências,
riscos e situações críticas.

O EcoMonitor Brasil pretende reunir esses dados em uma única
aplicação interativa, facilitando sua visualização e análise.
""")


# ---------------------------------------------------------
# OBJETIVOS
# ---------------------------------------------------------

st.markdown("""
### Objetivos do Projeto

- Integrar diferentes fontes públicas de dados ambientais.
- Organizar e tratar os dados utilizando Python.
- Apresentar indicadores ambientais em um dashboard interativo.
- Facilitar o acompanhamento de informações relacionadas à sustentabilidade.
- Incorporar recursos de inteligência artificial nas próximas etapas do projeto.
""")


# ---------------------------------------------------------
# ODS
# ---------------------------------------------------------

st.markdown("""
### Objetivos de Desenvolvimento Sustentável

**ODS 13 — Ação Contra a Mudança Global do Clima**

**ODS 15 — Vida Terrestre**
""")


# ---------------------------------------------------------
# LINKS ÚTEIS
# ---------------------------------------------------------

st.markdown("""
### Links Úteis

- [Agenda 2030 — ONU](https://brasil.un.org/pt-br/sdgs)
- [Open-Meteo](https://open-meteo.com/)
- [IBGE](https://www.ibge.gov.br/)
- [INPE](https://www.gov.br/inpe/)
""")


# ---------------------------------------------------------
# DADOS AMBIENTAIS
# ---------------------------------------------------------

st.markdown(f"### Dados Ambientais — {cidade_selecionada}")

try:
    df = coletar_dados_meteorologicos(cidade_selecionada)

    # -----------------------------------------------------
    # INDICADORES PRINCIPAIS
    # -----------------------------------------------------

    temperatura_maxima = df["Temperatura Máxima (°C)"].max()
    temperatura_minima = df["Temperatura Mínima (°C)"].min()
    precipitacao_total = df["Precipitação (mm)"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🌡️ Temperatura Máxima",
            value=f"{temperatura_maxima:.1f} °C"
        )

    with col2:
        st.metric(
            label="❄️ Temperatura Mínima",
            value=f"{temperatura_minima:.1f} °C"
        )

    with col3:
        st.metric(
            label="🌧️ Precipitação Total",
            value=f"{precipitacao_total:.1f} mm"
        )

    # -----------------------------------------------------
    # GRÁFICO
    # -----------------------------------------------------

    st.markdown("### Evolução dos Indicadores")

    if indicadores:
        df_grafico = df.copy()

        df_grafico["Data"] = pd.to_datetime(df_grafico["Data"])

        df_grafico = df_grafico.set_index("Data")

        st.line_chart(
            df_grafico[indicadores]
        )

    else:
        st.info(
            "Selecione pelo menos um indicador na barra lateral "
            "para visualizar o gráfico."
        )

    # -----------------------------------------------------
    # TABELA
    # -----------------------------------------------------

    if mostrar_tabela:
        st.markdown("### Dados Coletados")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        f"Fonte: Open-Meteo API — dados meteorológicos para "
        f"{cidade_selecionada}."
    )

except Exception as erro:

    st.error(
        "Não foi possível carregar os dados da Open-Meteo."
    )

    with st.expander("Detalhes do erro"):
        st.code(str(erro))
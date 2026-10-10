import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CAMINHO DO PROJETO
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.coleta_open_meteo import (
    CIDADES,
    coletar_dados_meteorologicos,
)


# =========================================================
# TÍTULO
# =========================================================

st.title("🌤️ Monitoramento Climático")

st.caption(
    "Consulte indicadores meteorológicos de diferentes cidades "
    "utilizando dados da Open-Meteo API."
)

st.divider()


# =========================================================
# FILTROS
# =========================================================

with st.container(border=True):

    st.markdown("### ⚙️ Filtros")

    col1, col2 = st.columns([1, 2])

    with col1:

        cidade_selecionada = st.selectbox(
            "📍 Localidade",
            options=list(CIDADES.keys()),
            key="cidade_clima",
        )

    with col2:

        indicadores = st.multiselect(
            "📊 Indicadores climáticos",
            options=[
                "Temperatura Máxima (°C)",
                "Temperatura Mínima (°C)",
                "Precipitação (mm)",
            ],
            default=[
                "Temperatura Máxima (°C)",
                "Temperatura Mínima (°C)",
            ],
            key="indicadores_clima",
        )


# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================

try:

    df = coletar_dados_meteorologicos(
        cidade_selecionada
    )

    temperatura_maxima = (
        df["Temperatura Máxima (°C)"].max()
    )

    temperatura_minima = (
        df["Temperatura Mínima (°C)"].min()
    )

    precipitacao_total = (
        df["Precipitação (mm)"].sum()
    )


    # =====================================================
    # MÉTRICAS
    # =====================================================

    st.markdown(
        f"## 📍 {cidade_selecionada}"
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "🌡️ Temperatura Máxima",
            f"{temperatura_maxima:.1f} °C",
        )

    with m2:

        st.metric(
            "❄️ Temperatura Mínima",
            f"{temperatura_minima:.1f} °C",
        )

    with m3:

        st.metric(
            "🌧️ Precipitação Total",
            f"{precipitacao_total:.1f} mm",
        )

    with m4:

        st.metric(
            "📅 Dias Analisados",
            len(df),
        )


    # =====================================================
    # GRÁFICO
    # =====================================================

    st.markdown("## 📈 Evolução dos Indicadores")

    with st.container(border=True):

        if indicadores:

            df_grafico = df.copy()

            df_grafico["Data"] = pd.to_datetime(
                df_grafico["Data"]
            )

            df_grafico = df_grafico.set_index(
                "Data"
            )

            st.line_chart(
                df_grafico[indicadores],
                height=430,
            )

        else:

            st.info(
                "Selecione pelo menos um indicador."
            )


    # =====================================================
    # TABELA
    # =====================================================

    with st.expander(
        "📋 Visualizar dados meteorológicos completos"
    ):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )


    # =====================================================
    # FONTE
    # =====================================================

    st.caption(
        f"Fonte: Open-Meteo API • {cidade_selecionada}"
    )


except Exception as erro:

    st.error(
        "Não foi possível carregar os dados meteorológicos."
    )

    with st.expander(
        "Detalhes técnicos"
    ):

        st.code(
            str(erro)
        )


# =========================================================
# NAVEGAÇÃO
# =========================================================

st.divider()

col_voltar, col_radar = st.columns(2)

with col_voltar:

    st.page_link(
        "paginas/inicio.py",
        label="← Voltar para o Início",
        icon="🏠",
    )

with col_radar:

    st.page_link(
        "paginas/radar_ambiental.py",
        label="Ir para Radar Ambiental",
        icon="📰",
    )
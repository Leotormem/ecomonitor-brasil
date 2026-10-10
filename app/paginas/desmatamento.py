from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CAMINHOS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

PRODES_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "desmatamento_prodes.csv"
)


# =========================================================
# CACHE
# =========================================================

@st.cache_data(ttl=600)
def carregar_prodes():
    return pd.read_csv(PRODES_PATH)


# =========================================================
# CABEÇALHO
# =========================================================

st.title("🌳 Desmatamento PRODES")

st.caption(
    "Análise da taxa anual de desmatamento "
    "na Amazônia Legal com dados do PRODES/INPE."
)

st.divider()


# =========================================================
# VERIFICAÇÃO DO ARQUIVO
# =========================================================

if not PRODES_PATH.exists():

    st.warning(
        "O arquivo `desmatamento_prodes.csv` "
        "ainda não foi encontrado."
    )

    st.info(
        "Execute primeiro a coleta com Selenium:\n\n"
        "`python src/data/coleta_prodes_selenium.py`"
    )

else:

    try:

        # =================================================
        # CARREGAMENTO
        # =================================================

        df = carregar_prodes()

        df["Ano"] = pd.to_numeric(
            df["Ano"],
            errors="coerce"
        )

        df["Area_km2"] = pd.to_numeric(
            df["Area_km2"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "UF",
                "Ano",
                "Area_km2",
            ]
        )

        df["Ano"] = df["Ano"].astype(int)


        # =================================================
        # MÉTRICAS GERAIS
        # =================================================

        ano_inicial = int(
            df["Ano"].min()
        )

        ano_final = int(
            df["Ano"].max()
        )

        total_ufs = (
            df["UF"]
            .nunique()
        )

        total_registros = len(df)


        st.markdown("## 📊 Visão Geral")

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "🌎 Estados monitorados",
                total_ufs,
            )

        with m2:

            st.metric(
                "📅 Ano inicial",
                ano_inicial,
            )

        with m3:

            st.metric(
                "📅 Ano mais recente",
                ano_final,
            )

        with m4:

            st.metric(
                "📄 Registros",
                total_registros,
            )


        # =================================================
        # FILTROS
        # =================================================

        st.markdown("## ⚙️ Filtros")

        with st.container(border=True):

            f1, f2 = st.columns([1.2, 2])

            with f1:

                uf_selecionada = st.selectbox(
                    "🌳 Estado",
                    options=sorted(
                        df["UF"]
                        .dropna()
                        .unique()
                    ),
                )

            with f2:

                intervalo_anos = st.slider(
                    "📅 Intervalo de anos",
                    min_value=ano_inicial,
                    max_value=ano_final,
                    value=(
                        ano_inicial,
                        ano_final,
                    ),
                )


        # =================================================
        # FILTRAGEM
        # =================================================

        df_filtrado = df[
            (
                df["UF"]
                == uf_selecionada
            )
            &
            (
                df["Ano"]
                >= intervalo_anos[0]
            )
            &
            (
                df["Ano"]
                <= intervalo_anos[1]
            )
        ].copy()


        # =================================================
        # MÉTRICAS DO ESTADO
        # =================================================

        if not df_filtrado.empty:

            maior_area = (
                df_filtrado[
                    "Area_km2"
                ].max()
            )

            ano_maior = int(
                df_filtrado.loc[
                    df_filtrado[
                        "Area_km2"
                    ].idxmax(),
                    "Ano"
                ]
            )

            media_area = (
                df_filtrado[
                    "Area_km2"
                ].mean()
            )


            st.markdown(
                f"## 📍 {uf_selecionada}"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "🔥 Maior área desmatada",
                    f"{maior_area:,.1f} km²",
                )

            with c2:

                st.metric(
                    "📅 Ano de maior desmatamento",
                    ano_maior,
                )

            with c3:

                st.metric(
                    "📊 Média anual",
                    f"{media_area:,.1f} km²",
                )


            # =================================================
            # GRÁFICO
            # =================================================

            st.markdown(
                "## 📈 Evolução do Desmatamento"
            )

            with st.container(border=True):

                df_grafico = (
                    df_filtrado[
                        [
                            "Ano",
                            "Area_km2",
                        ]
                    ]
                    .sort_values(
                        "Ano"
                    )
                    .set_index(
                        "Ano"
                    )
                )

                st.line_chart(
                    df_grafico,
                    height=430,
                )


            # =================================================
            # TABELA
            # =================================================

            with st.expander(
                "📋 Visualizar dados completos"
            ):

                st.dataframe(
                    df_filtrado[
                        [
                            "UF",
                            "Ano",
                            "Area_km2",
                        ]
                    ]
                    .sort_values(
                        "Ano",
                        ascending=False,
                    ),
                    width="stretch",
                    hide_index=True,
                )


        else:

            st.warning(
                "Não existem dados para "
                "os filtros selecionados."
            )


        # =================================================
        # COMPARAÇÃO ENTRE ESTADOS
        # =================================================

        st.markdown(
            "## 🗺️ Comparação entre Estados"
        )

        ano_comparacao = st.selectbox(
            "Selecione o ano para comparar",
            options=sorted(
                df["Ano"]
                .unique(),
                reverse=True,
            ),
        )

        df_comparacao = (
            df[
                df["Ano"]
                == ano_comparacao
            ]
            [
                [
                    "UF",
                    "Area_km2",
                ]
            ]
            .sort_values(
                "Area_km2",
                ascending=False,
            )
            .set_index(
                "UF"
            )
        )

        with st.container(border=True):

            st.bar_chart(
                df_comparacao,
                height=420,
            )


        # =================================================
        # INFORMAÇÕES SOBRE A COLETA
        # =================================================

        with st.expander(
            "ℹ️ Sobre a coleta dos dados"
        ):

            st.write(
                """
                Os dados desta página são provenientes
                do painel PRODES/INPE no TerraBrasilis.

                Como o conteúdo da tabela é carregado
                dinamicamente por JavaScript, a coleta
                foi realizada com Selenium.

                O navegador automatizado executa a página,
                aguarda o carregamento dos dados e salva
                o resultado em um arquivo CSV dentro de
                `data/processed/`.

                A aplicação Streamlit não executa Selenium
                diretamente: ela apenas lê o arquivo
                previamente coletado.
                """
            )


        # =================================================
        # FONTE
        # =================================================

        st.caption(
            "Fonte: PRODES / Instituto Nacional "
            "de Pesquisas Espaciais — INPE."
        )


    except Exception as erro:

        st.error(
            "Não foi possível carregar "
            "os dados do PRODES."
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

n1, n2 = st.columns(2)

with n1:

    st.page_link(
        "paginas/radar_ambiental.py",
        label="← Radar Ambiental",
        icon="📰",
    )

with n2:

    st.page_link(
        "paginas/dados.py",
        label="Ir para Base de Dados",
        icon="📂",
    )
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud


# =========================================================
# CAMINHOS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

NOTICIAS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "noticias_inpe.csv"
)


# =========================================================
# CACHE
# =========================================================

@st.cache_data(ttl=600)
def carregar_noticias():
    return pd.read_csv(NOTICIAS_PATH)


# =========================================================
# CABEÇALHO
# =========================================================

st.title("📰 Radar Ambiental")

st.caption(
    "Monitoramento e análise de notícias ambientais "
    "coletadas do portal do INPE."
)

st.divider()


# =========================================================
# VERIFICAÇÃO DO ARQUIVO
# =========================================================

if not NOTICIAS_PATH.exists():

    st.warning(
        "O arquivo de notícias ainda não foi encontrado em "
        "`data/processed/noticias_inpe.csv`."
    )

else:

    try:

        # =================================================
        # CARREGAMENTO
        # =================================================

        df_noticias = carregar_noticias()

        df_noticias["tamanho_titulo"] = (
            df_noticias["titulo"]
            .astype(str)
            .str.len()
        )

        total_noticias = len(df_noticias)

        media_titulo = (
            df_noticias["tamanho_titulo"]
            .mean()
        )

        texto_titulos = " ".join(
            df_noticias["titulo"]
            .dropna()
            .astype(str)
            .tolist()
        )


        # =================================================
        # LIMPEZA DOS TERMOS
        # =================================================

        stopwords_pt = {
            "para",
            "sobre",
            "como",
            "mais",
            "com",
            "dos",
            "das",
            "uma",
            "uns",
            "nas",
            "nos",
            "pela",
            "pelo",
            "pelos",
            "pelas",
            "entre",
            "brasil",
            "recebe",
            "dados",
            "estudo",
            "painel",
            "inpe",
            "2025",
            "2026",
            "2027",
            "será",
            "são",
            "tem",
            "seu",
            "sua",
            "que",
            "por",
            "aos",
            "ainda",
            "novo",
            "nova",
        }

        palavras = [
            palavra
            .strip(".,:;!?()[]{}\"'")
            .lower()
            for palavra
            in texto_titulos.split()
        ]

        palavras = [
            palavra
            for palavra
            in palavras
            if (
                len(palavra) > 3
                and palavra not in stopwords_pt
                and not palavra.isnumeric()
            )
        ]

        contagem_palavras = Counter(
            palavras
        )

        palavras_mais_frequentes = (
            contagem_palavras
            .most_common(10)
        )


        # =================================================
        # MÉTRICAS
        # =================================================

        st.markdown("## 📊 Visão Geral")

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "📰 Notícias Coletadas",
                total_noticias,
            )

        with m2:

            st.metric(
                "✍️ Média dos Títulos",
                f"{media_titulo:.0f} caracteres",
            )

        with m3:

            st.metric(
                "🔎 Termos Analisados",
                len(palavras),
            )


        # =================================================
        # ABAS INTERNAS
        # =================================================

        st.markdown("## 🔎 Análise das Notícias")

        aba_analise, aba_noticias = st.tabs(
            [
                "📊 Análise Textual",
                "🗞️ Notícias Coletadas",
            ]
        )


        # =================================================
        # ANÁLISE TEXTUAL
        # =================================================

        with aba_analise:

            col1, col2 = st.columns(
                [1, 2]
            )

            with col1:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🔎 Termos em Destaque"
                    )

                    df_palavras = pd.DataFrame(
                        palavras_mais_frequentes,
                        columns=[
                            "Palavra",
                            "Frequência",
                        ],
                    )

                    st.dataframe(
                        df_palavras,
                        width="stretch",
                        hide_index=True,
                    )


            with col2:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### ☁️ Nuvem de Palavras"
                    )

                    if palavras:

                        texto_nuvem = " ".join(
                            palavras
                        )

                        wordcloud = WordCloud(
                            width=1200,
                            height=500,
                            background_color="#151C26",
                            colormap="Greens",
                            collocations=False,
                        ).generate(
                            texto_nuvem
                        )

                        fig, ax = plt.subplots(
                            figsize=(12, 5)
                        )

                        ax.imshow(
                            wordcloud,
                            interpolation="bilinear",
                        )

                        ax.axis("off")

                        st.pyplot(fig)

                        plt.close(fig)

                    else:

                        st.info(
                            "Não há conteúdo suficiente "
                            "para gerar a nuvem de palavras."
                        )


        # =================================================
        # LISTA DE NOTÍCIAS
        # =================================================

        with aba_noticias:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🗞️ Notícias Monitoradas"
                )

                st.dataframe(
                    df_noticias[
                        [
                            "titulo",
                            "url",
                        ]
                    ],
                    width="stretch",
                    hide_index=True,
                    column_config={
                        "titulo":
                            st.column_config.TextColumn(
                                "Título"
                            ),

                        "url":
                            st.column_config.LinkColumn(
                                "Acessar",
                                display_text="Abrir notícia",
                            ),
                    },
                )


        # =================================================
        # FONTE
        # =================================================

        st.caption(
            "Fonte: Instituto Nacional de Pesquisas "
            "Espaciais — INPE."
        )


    except Exception as erro:

        st.error(
            "Não foi possível carregar "
            "ou analisar as notícias."
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

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "paginas/clima.py",
        label="← Dashboard Climático",
        icon="📊",
    )

with col2:

    st.page_link(
        "paginas/dados.py",
        label="Ir para Base de Dados",
        icon="📂",
    )
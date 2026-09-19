import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud


# =========================================================
# CAMINHOS DO PROJETO
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.data.coleta_open_meteo import (
    CIDADES,
    coletar_dados_meteorologicos,
)

NOTICIAS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "noticias_inpe.csv"
)


# =========================================================
# FUNÇÕES
# =========================================================

@st.cache_data(ttl=600)
def carregar_noticias():
    return pd.read_csv(NOTICIAS_PATH)


def validar_csv(uploaded_file):
    try:
        df_upload = pd.read_csv(uploaded_file)

        if df_upload.empty:
            return None, "O arquivo CSV está vazio."

        return df_upload, None

    except Exception as erro:
        return None, f"Erro ao ler o arquivo: {erro}"


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="EcoMonitor Brasil",
    page_icon="🌱",
    layout="wide",
)


# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown(
    """
    <style>

    /* ---------------------------------------------
       ÁREA PRINCIPAL
    --------------------------------------------- */

    .block-container {
        max-width: 1380px;
        padding-top: 1.6rem;
        padding-bottom: 4rem;
    }


    /* ---------------------------------------------
       TÍTULOS
    --------------------------------------------- */

    h1 {
        letter-spacing: -0.035em;
        font-weight: 800 !important;
    }

    h2 {
        letter-spacing: -0.025em;
        font-weight: 750 !important;
    }

    h3 {
        letter-spacing: -0.015em;
    }


    /* ---------------------------------------------
       CARDS / MÉTRICAS
    --------------------------------------------- */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.040),
                rgba(255,255,255,0.012)
            );

        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;

        padding: 19px 20px;

        box-shadow:
            0 8px 24px rgba(0,0,0,0.20);

        transition:
            transform 0.15s ease,
            border-color 0.15s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(52,211,153,0.30);
    }


    /* ---------------------------------------------
       CONTAINERS COM BORDA
    --------------------------------------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;

        border:
            1px solid rgba(255,255,255,0.085) !important;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.022),
                rgba(255,255,255,0.008)
            );

        box-shadow:
            0 8px 24px rgba(0,0,0,0.12);
    }


    /* ---------------------------------------------
       SELECT / MULTISELECT
    --------------------------------------------- */

    div[data-baseweb="select"] > div {
        min-height: 48px;

        border-radius: 12px !important;

        background:
            rgba(255,255,255,0.035) !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color:
            rgba(52,211,153,0.45) !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color:
            rgba(52,211,153,0.65) !important;

        box-shadow:
            0 0 0 2px rgba(52,211,153,0.08);
    }


    /* ---------------------------------------------
       CHIPS DO MULTISELECT
    --------------------------------------------- */

    span[data-baseweb="tag"] {
        border-radius: 999px !important;

        background:
            rgba(52,211,153,0.15) !important;

        color:
            #D1FAE5 !important;

        border:
            1px solid rgba(52,211,153,0.25) !important;

        font-weight: 600;
    }


    /* ---------------------------------------------
       ABAS
    --------------------------------------------- */

    div[data-baseweb="tab-list"] {
        gap: 7px;
    }

    button[data-baseweb="tab"] {
        border-radius: 11px 11px 0 0;

        padding:
            10px 17px;

        font-size:
            0.96rem;

        font-weight:
            650;

        transition:
            background 0.15s ease,
            color 0.15s ease;
    }

    button[data-baseweb="tab"]:hover {
        background:
            rgba(255,255,255,0.035);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color:
            #34D399 !important;

        background:
            rgba(52,211,153,0.08);

        border-bottom:
            2px solid #34D399 !important;
    }


    /* ---------------------------------------------
       BOTÕES
    --------------------------------------------- */

    .stButton button,
    .stDownloadButton button {
        min-height: 44px;

        border-radius:
            12px;

        font-weight:
            650;

        border:
            1px solid rgba(255,255,255,0.10);

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.040),
                rgba(255,255,255,0.015)
            );

        transition:
            border-color 0.15s ease,
            color 0.15s ease,
            transform 0.15s ease;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        border-color:
            rgba(52,211,153,0.45);

        color:
            #34D399;

        transform:
            translateY(-1px);
    }


    /* ---------------------------------------------
       FILE UPLOADER
    --------------------------------------------- */

    section[data-testid="stFileUploaderDropzone"] {
        border-radius:
            14px;

        border:
            1px dashed rgba(52,211,153,0.32);

        background:
            rgba(52,211,153,0.025);
    }


    /* ---------------------------------------------
       TABELAS
    --------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius:
            13px;

        overflow:
            hidden;

        border:
            1px solid rgba(255,255,255,0.06);
    }


    /* ---------------------------------------------
       EXPANDERS
    --------------------------------------------- */

    details {
        border-radius:
            12px !important;
    }


    /* ---------------------------------------------
       ALERTAS
    --------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius:
            13px;
    }


    /* ---------------------------------------------
       DIVISORES
    --------------------------------------------- */

    hr {
        border-color:
            rgba(255,255,255,0.075);
    }


    /* ---------------------------------------------
       LEGENDA / TEXTO SECUNDÁRIO
    --------------------------------------------- */

    [data-testid="stCaptionContainer"] {
        opacity:
            0.78;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CABEÇALHO
# =========================================================

titulo, status = st.columns(
    [4.3, 1]
)

with titulo:

    st.title(
        "🌱 EcoMonitor Brasil"
    )

    st.markdown(
        "### Inteligência de dados aplicada "
        "ao monitoramento ambiental"
    )

    st.caption(
        "Clima • Sustentabilidade • "
        "Notícias ambientais • Agenda 2030"
    )


with status:

    st.write("")
    st.write("")

    with st.container(
        border=True
    ):

        st.caption(
            "STATUS DA PLATAFORMA"
        )

        st.success(
            "● Sistema online"
        )


st.divider()


# =========================================================
# FILTROS GERAIS
# =========================================================

with st.container(
    border=True
):

    st.markdown(
        "### ⚙️ Filtros do Dashboard"
    )

    filtro1, filtro2 = st.columns(
        [1, 2]
    )

    with filtro1:

        cidade_selecionada = (
            st.selectbox(
                "📍 Localidade",
                options=list(
                    CIDADES.keys()
                ),
            )
        )


    with filtro2:

        indicadores = (
            st.multiselect(
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
            )
        )


# =========================================================
# ESTADO DE SESSÃO
# =========================================================

if (
    "ultima_cidade"
    not in st.session_state
):

    st.session_state.ultima_cidade = (
        cidade_selecionada
    )


if (
    st.session_state.ultima_cidade
    != cidade_selecionada
):

    st.toast(
        "📍 Localidade alterada para "
        f"{cidade_selecionada}"
    )

    st.session_state.ultima_cidade = (
        cidade_selecionada
    )


# =========================================================
# COLETA CLIMÁTICA
# =========================================================

df = None


try:

    df = (
        coletar_dados_meteorologicos(
            cidade_selecionada
        )
    )


except Exception as erro:

    st.error(
        "Não foi possível carregar "
        "os dados meteorológicos."
    )

    with st.expander(
        "Detalhes técnicos"
    ):

        st.code(
            str(erro)
        )


# =========================================================
# NAVEGAÇÃO PRINCIPAL
# =========================================================

aba_dashboard, aba_noticias, aba_dados, aba_sobre = (
    st.tabs(
        [
            "📊 Dashboard",
            "📰 Radar Ambiental",
            "📂 Base de Dados",
            "🌎 Sobre",
        ]
    )
)


# =========================================================
# ABA 1 — DASHBOARD
# =========================================================

with aba_dashboard:

    st.write("")

    st.subheader(
        f"Visão climática — "
        f"{cidade_selecionada}"
    )

    st.caption(
        "Indicadores meteorológicos obtidos "
        "através da Open-Meteo API."
    )


    if df is not None:

        temperatura_maxima = (
            df[
                "Temperatura Máxima (°C)"
            ]
            .max()
        )

        temperatura_minima = (
            df[
                "Temperatura Mínima (°C)"
            ]
            .min()
        )

        precipitacao_total = (
            df[
                "Precipitação (mm)"
            ]
            .sum()
        )


        # -------------------------------------------------
        # CARDS CLIMÁTICOS
        # -------------------------------------------------

        m1, m2, m3, m4 = (
            st.columns(4)
        )


        with m1:

            st.metric(
                "🌡️ Temperatura máxima",
                f"{temperatura_maxima:.1f} °C",
            )


        with m2:

            st.metric(
                "❄️ Temperatura mínima",
                f"{temperatura_minima:.1f} °C",
            )


        with m3:

            st.metric(
                "🌧️ Precipitação",
                f"{precipitacao_total:.1f} mm",
            )


        with m4:

            st.metric(
                "📅 Dias analisados",
                len(df),
            )


        st.write("")


        # -------------------------------------------------
        # GRÁFICO + RESUMO
        # -------------------------------------------------

        esquerda, direita = (
            st.columns(
                [2.3, 1]
            )
        )


        with esquerda:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 📈 Evolução dos indicadores"
                )

                if indicadores:

                    df_grafico = (
                        df.copy()
                    )

                    df_grafico[
                        "Data"
                    ] = pd.to_datetime(
                        df_grafico[
                            "Data"
                        ]
                    )

                    df_grafico = (
                        df_grafico
                        .set_index(
                            "Data"
                        )
                    )

                    st.line_chart(
                        df_grafico[
                            indicadores
                        ],
                        height=430,
                    )

                else:

                    st.info(
                        "Selecione pelo menos "
                        "um indicador."
                    )


        with direita:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 📋 Resumo"
                )

                st.markdown(
                    f"""
                    **📍 Localidade**

                    {cidade_selecionada}

                    **🔗 Fonte**

                    Open-Meteo

                    **📊 Indicadores ativos**

                    {len(indicadores)}

                    **🌎 ODS relacionado**

                    ODS 13 — Ação Climática
                    """
                )


        st.write("")


        # -------------------------------------------------
        # TABELA
        # -------------------------------------------------

        with st.expander(
            "📑 Consultar dados "
            "meteorológicos completos"
        ):

            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
            )


        st.caption(
            "Fonte: Open-Meteo API • "
            f"{cidade_selecionada}"
        )


# =========================================================
# ABA 2 — RADAR AMBIENTAL
# =========================================================

with aba_noticias:

    st.write("")

    st.subheader(
        "📰 Radar Ambiental"
    )

    st.caption(
        "Notícias ambientais coletadas "
        "do portal do INPE via "
        "WebScraping com BeautifulSoup."
    )


    if not NOTICIAS_PATH.exists():

        st.warning(
            "O arquivo de notícias "
            "ainda não foi gerado."
        )


    else:

        try:

            df_noticias = (
                carregar_noticias()
            )


            df_noticias[
                "tamanho_titulo"
            ] = (
                df_noticias[
                    "titulo"
                ]
                .astype(str)
                .str.len()
            )


            total_noticias = (
                len(
                    df_noticias
                )
            )


            media_titulo = (
                df_noticias[
                    "tamanho_titulo"
                ]
                .mean()
            )


            texto = " ".join(
                df_noticias[
                    "titulo"
                ]
                .dropna()
                .astype(str)
                .tolist()
            )


            # ---------------------------------------------
            # STOPWORDS
            # ---------------------------------------------

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
                .strip(
                    ".,:;!?()[]{}\"'"
                )
                .lower()
                for palavra
                in texto.split()
            ]


            palavras = [
                palavra
                for palavra
                in palavras
                if (
                    len(
                        palavra
                    ) > 3
                    and palavra
                    not in stopwords_pt
                    and not
                    palavra.isnumeric()
                )
            ]


            contagem = Counter(
                palavras
            )


            frequentes = (
                contagem
                .most_common(10)
            )


            # ---------------------------------------------
            # MÉTRICAS
            # ---------------------------------------------

            n1, n2, n3 = (
                st.columns(3)
            )


            with n1:

                st.metric(
                    "📰 Notícias monitoradas",
                    total_noticias,
                )


            with n2:

                st.metric(
                    "✍️ Média dos títulos",
                    f"{media_titulo:.0f} caracteres",
                )


            with n3:

                st.metric(
                    "🔎 Termos analisados",
                    len(
                        palavras
                    ),
                )


            st.write("")


            # ---------------------------------------------
            # SUB-ABAS
            # ---------------------------------------------

            analise, lista = (
                st.tabs(
                    [
                        "📊 Análise textual",
                        "🗞️ Todas as notícias",
                    ]
                )
            )


            with analise:

                col_palavras, col_nuvem = (
                    st.columns(
                        [1, 2]
                    )
                )


                with col_palavras:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### 🔎 Termos em destaque"
                        )

                        df_palavras = (
                            pd.DataFrame(
                                frequentes,
                                columns=[
                                    "Palavra",
                                    "Frequência",
                                ],
                            )
                        )

                        st.dataframe(
                            df_palavras,
                            width="stretch",
                            hide_index=True,
                        )


                with col_nuvem:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### ☁️ Nuvem de palavras"
                        )

                        if palavras:

                            texto_nuvem = (
                                " ".join(
                                    palavras
                                )
                            )

                            wordcloud = (
                                WordCloud(
                                    width=1200,
                                    height=500,
                                    background_color=(
                                        "#151C26"
                                    ),
                                    colormap=(
                                        "Greens"
                                    ),
                                    collocations=False,
                                )
                                .generate(
                                    texto_nuvem
                                )
                            )

                            fig, ax = (
                                plt.subplots(
                                    figsize=(
                                        12,
                                        5,
                                    )
                                )
                            )

                            ax.imshow(
                                wordcloud,
                                interpolation=(
                                    "bilinear"
                                ),
                            )

                            ax.axis(
                                "off"
                            )

                            st.pyplot(
                                fig
                            )

                            plt.close(
                                fig
                            )


            with lista:

                with st.container(
                    border=True
                ):

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
                                st.column_config
                                .TextColumn(
                                    "Título"
                                ),

                            "url":
                                st.column_config
                                .LinkColumn(
                                    "Acessar",
                                    display_text=(
                                        "Abrir notícia"
                                    ),
                                ),
                        },
                    )


            st.caption(
                "Fonte: Instituto Nacional "
                "de Pesquisas Espaciais — INPE."
            )


        except Exception as erro:

            st.error(
                "Não foi possível carregar "
                "as notícias."
            )

            with st.expander(
                "Detalhes técnicos"
            ):

                st.code(
                    str(erro)
                )


# =========================================================
# ABA 3 — BASE DE DADOS
# =========================================================

with aba_dados:

    st.write("")

    st.subheader(
        "📂 Dados Complementares"
    )

    st.caption(
        "Importe arquivos CSV para complementar "
        "as informações do EcoMonitor."
    )


    upload, informacao = (
        st.columns(
            [1.4, 1]
        )
    )


    with upload:

        with st.container(
            border=True
        ):

            st.markdown(
                "### ⬆️ Importar CSV"
            )

            arquivo_enviado = (
                st.file_uploader(
                    "Arraste ou selecione "
                    "um arquivo CSV",
                    type=[
                        "csv"
                    ],
                )
            )


    with informacao:

        with st.container(
            border=True
        ):

            st.markdown(
                "### ℹ️ Como funciona"
            )

            st.markdown(
                """
                **1.** Envie um arquivo CSV.

                **2.** O sistema valida o conteúdo.

                **3.** Os dados são exibidos no painel.

                **4.** Você pode exportar o resultado.
                """
            )


    if arquivo_enviado is not None:

        df_upload, erro_upload = (
            validar_csv(
                arquivo_enviado
            )
        )


        if erro_upload:

            st.error(
                erro_upload
            )


        else:

            st.success(
                "Arquivo carregado e validado."
            )


            d1, d2 = (
                st.columns(2)
            )


            with d1:

                st.metric(
                    "📄 Linhas",
                    len(
                        df_upload
                    ),
                )


            with d2:

                st.metric(
                    "📊 Colunas",
                    len(
                        df_upload.columns
                    ),
                )


            with st.container(
                border=True
            ):

                st.markdown(
                    "### 👀 Prévia dos dados"
                )

                st.dataframe(
                    df_upload,
                    width="stretch",
                    hide_index=True,
                )


            st.session_state[
                "dados_upload"
            ] = df_upload


            csv_download = (
                df_upload
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8-sig"
                )
            )


            st.download_button(
                "⬇️ Baixar CSV processado",
                data=csv_download,
                file_name=(
                    "dados_ecomonitor.csv"
                ),
                mime=(
                    "text/csv"
                ),
            )


# =========================================================
# ABA 4 — SOBRE
# =========================================================

with aba_sobre:

    st.write("")

    st.subheader(
        "🌎 EcoMonitor Brasil "
        "e Agenda 2030"
    )


    sobre, agenda = (
        st.columns(
            [1.4, 1]
        )
    )


    with sobre:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 Sobre o Projeto"
            )

            st.write(
                """
                O **EcoMonitor Brasil** integra
                dados ambientais, meteorológicos
                e informações públicas relacionadas
                à sustentabilidade.

                A solução utiliza Python,
                Streamlit, APIs públicas e
                WebScraping para transformar
                diferentes fontes de dados em
                informações acessíveis e interativas.
                """
            )


            st.markdown(
                "#### Objetivos"
            )

            st.markdown(
                """
                - Integrar fontes ambientais públicas.
                - Facilitar a análise de indicadores.
                - Permitir interação com os dados.
                - Apoiar iniciativas relacionadas a ESG.
                - Evoluir para recursos de IA.
                """
            )


    with agenda:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🌱 Agenda 2030"
            )

            st.markdown(
                """
                #### ODS 13

                **Ação Contra a Mudança Global do Clima**

                Monitoramento de condições
                climáticas e informações
                relacionadas ao meio ambiente.

                ---

                #### ODS 15

                **Vida Terrestre**

                Monitoramento de temas ligados
                a ecossistemas, queimadas,
                desmatamento e biodiversidade.
                """
            )


    st.write("")


    fontes, tecnologias = (
        st.columns(2)
    )


    with fontes:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🔗 Fontes"
            )

            st.markdown(
                """
                - [Open-Meteo](https://open-meteo.com/)
                - [INPE](https://www.gov.br/inpe/)
                - [IBGE](https://www.ibge.gov.br/)
                - [Agenda 2030 — ONU](https://brasil.un.org/pt-br/sdgs)
                """
            )


    with tecnologias:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🛠️ Tecnologias"
            )

            st.markdown(
                """
                `Python`

                `Streamlit`

                `Pandas`

                `BeautifulSoup`

                `Requests`

                `Matplotlib`

                `Git`

                `GitHub`
                """
            )


# =========================================================
# RODAPÉ
# =========================================================

st.divider()


footer1, footer2 = (
    st.columns(
        [3, 1]
    )
)


with footer1:

    st.caption(
        "🌱 EcoMonitor Brasil • "
        "Dados e tecnologia para sustentabilidade"
    )


with footer2:

    st.caption(
        "ODS 13 • ODS 15"
    )
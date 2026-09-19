import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud


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
# CAMINHOS DOS ARQUIVOS
# ---------------------------------------------------------

NOTICIAS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "noticias_inpe.csv"
)


# ---------------------------------------------------------
# CACHE
# ---------------------------------------------------------

@st.cache_data(ttl=600)
def carregar_noticias():
    """
    Carrega o arquivo CSV de notícias do INPE.

    O cache permanece válido por 10 minutos.
    """
    return pd.read_csv(NOTICIAS_PATH)


# ---------------------------------------------------------
# FUNÇÃO PARA VALIDAR CSV ENVIADO
# ---------------------------------------------------------

def validar_csv(uploaded_file):
    """
    Valida um arquivo CSV enviado pelo usuário.

    Retorna:
        dataframe, erro
    """

    try:
        df_upload = pd.read_csv(uploaded_file)

        if df_upload.empty:
            return None, "O arquivo CSV está vazio."

        return df_upload, None

    except Exception as erro:
        return None, f"Erro ao ler o arquivo: {erro}"


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


# ---------------------------------------------------------
# ESTADO DE SESSÃO
# ---------------------------------------------------------

if "ultima_cidade" not in st.session_state:
    st.session_state.ultima_cidade = cidade_selecionada

if st.session_state.ultima_cidade != cidade_selecionada:

    st.sidebar.success(
        f"Cidade alterada para {cidade_selecionada}"
    )

    st.session_state.ultima_cidade = cidade_selecionada


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

mostrar_noticias = st.sidebar.checkbox(
    "Exibir notícias ambientais",
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
# DADOS METEOROLÓGICOS
# ---------------------------------------------------------

st.markdown(
    f"### Dados Ambientais — {cidade_selecionada}"
)

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

    st.markdown(
        "### Evolução dos Indicadores"
    )

    if indicadores:

        df_grafico = df.copy()

        df_grafico["Data"] = pd.to_datetime(
            df_grafico["Data"]
        )

        df_grafico = df_grafico.set_index(
            "Data"
        )

        st.line_chart(
            df_grafico[indicadores]
        )

    else:

        st.info(
            "Selecione pelo menos um indicador "
            "na barra lateral."
        )

    if mostrar_tabela:

        st.markdown(
            "### Dados Coletados"
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    st.caption(
        f"Fonte: Open-Meteo API — dados "
        f"meteorológicos para "
        f"{cidade_selecionada}."
    )

except Exception as erro:

    st.error(
        "Não foi possível carregar os "
        "dados da Open-Meteo."
    )

    with st.expander(
        "Detalhes do erro"
    ):
        st.code(str(erro))


# ---------------------------------------------------------
# NOTÍCIAS AMBIENTAIS DO INPE
# ---------------------------------------------------------

if mostrar_noticias:

    st.divider()

    st.markdown(
        "## 📰 Notícias Ambientais — INPE"
    )

    try:

        if not NOTICIAS_PATH.exists():

            st.warning(
                "O arquivo de notícias ainda "
                "não foi gerado."
            )

        else:

            df_noticias = carregar_noticias()

            # ---------------------------------------------
            # ESTATÍSTICAS BÁSICAS
            # ---------------------------------------------

            df_noticias["tamanho_titulo"] = (
                df_noticias["titulo"]
                .astype(str)
                .str.len()
            )

            media_tamanho_titulo = (
                df_noticias[
                    "tamanho_titulo"
                ].mean()
            )

            total_noticias = len(
                df_noticias
            )

            texto_titulos = " ".join(
                df_noticias["titulo"]
                .dropna()
                .astype(str)
                .tolist()
            )

            palavras = [
                palavra
                .strip(".,:;!?()[]{}\"'")
                .lower()
                for palavra in texto_titulos.split()
                if len(palavra) > 3
            ]

            contagem_palavras = Counter(
                palavras
            )

            palavras_mais_frequentes = (
                contagem_palavras.most_common(10)
            )

            col_n1, col_n2 = st.columns(2)

            with col_n1:

                st.metric(
                    label="📰 Quantidade de notícias",
                    value=total_noticias
                )

            with col_n2:

                st.metric(
                    label="📏 Tamanho médio dos títulos",
                    value=(
                        f"{media_tamanho_titulo:.1f} "
                        "caracteres"
                    )
                )

            # ---------------------------------------------
            # PALAVRAS MAIS FREQUENTES
            # ---------------------------------------------

            st.markdown(
                "### Palavras mais frequentes"
            )

            df_palavras = pd.DataFrame(
                palavras_mais_frequentes,
                columns=[
                    "Palavra",
                    "Frequência"
                ]
            )

            st.dataframe(
                df_palavras,
                width="stretch",
                hide_index=True
            )

            # ---------------------------------------------
            # NUVEM DE PALAVRAS
            # ---------------------------------------------

            st.markdown(
                "### ☁️ Nuvem de Palavras"
            )

            if texto_titulos.strip():

                wordcloud = WordCloud(
                    width=1200,
                    height=500,
                    background_color="white",
                    collocations=False
                ).generate(
                    texto_titulos
                )

                fig, ax = plt.subplots(
                    figsize=(12, 5)
                )

                ax.imshow(
                    wordcloud,
                    interpolation="bilinear"
                )

                ax.axis("off")

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)

            else:

                st.info(
                    "Não há conteúdo suficiente "
                    "para gerar a nuvem de palavras."
                )

            # ---------------------------------------------
            # TABELA DE NOTÍCIAS
            # ---------------------------------------------

            st.markdown(
                "### Últimas notícias coletadas"
            )

            st.dataframe(
                df_noticias[
                    [
                        "titulo",
                        "url"
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
                            "Link da notícia",
                            display_text="Abrir notícia"
                        )
                }
            )

            st.caption(
                "Fonte: INPE — conteúdo coletado "
                "por WebScraping com BeautifulSoup."
            )

    except Exception as erro:

        st.error(
            "Não foi possível carregar "
            "as notícias do INPE."
        )

        with st.expander(
            "Detalhes do erro"
        ):
            st.code(str(erro))


# ---------------------------------------------------------
# UPLOAD E DOWNLOAD DE CSV
# ---------------------------------------------------------

st.divider()

st.markdown(
    "## 📁 Dados Complementares"
)

st.write(
    "Envie um arquivo CSV para complementar "
    "as informações exibidas pelo EcoMonitor Brasil."
)

arquivo_enviado = st.file_uploader(
    "Selecione um arquivo CSV",
    type=["csv"]
)


if arquivo_enviado is not None:

    df_upload, erro_upload = validar_csv(
        arquivo_enviado
    )

    if erro_upload:

        st.error(
            erro_upload
        )

    else:

        st.success(
            "Arquivo CSV carregado com sucesso."
        )

        # ---------------------------------------------
        # INFORMAÇÕES DO ARQUIVO
        # ---------------------------------------------

        col_u1, col_u2 = st.columns(2)

        with col_u1:

            st.metric(
                label="Linhas",
                value=len(df_upload)
            )

        with col_u2:

            st.metric(
                label="Colunas",
                value=len(
                    df_upload.columns
                )
            )

        # ---------------------------------------------
        # VISUALIZAÇÃO
        # ---------------------------------------------

        st.markdown(
            "### Prévia dos dados enviados"
        )

        st.dataframe(
            df_upload,
            width="stretch",
            hide_index=True
        )

        # ---------------------------------------------
        # ESTADO DE SESSÃO
        # ---------------------------------------------

        st.session_state["dados_upload"] = (
            df_upload
        )

        # ---------------------------------------------
        # DOWNLOAD
        # ---------------------------------------------

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
            label="⬇️ Baixar dados em CSV",
            data=csv_download,
            file_name="dados_ecomonitor.csv",
            mime="text/csv"
        )


# ---------------------------------------------------------
# DADOS MANTIDOS NA SESSÃO
# ---------------------------------------------------------

if "dados_upload" in st.session_state:

    st.caption(
        "Os dados enviados permanecem disponíveis "
        "durante esta sessão da aplicação."
    )
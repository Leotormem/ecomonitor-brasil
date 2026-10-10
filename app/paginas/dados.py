import pandas as pd
import streamlit as st


# =========================================================
# FUNÇÃO DE VALIDAÇÃO
# =========================================================

def validar_csv(uploaded_file):
    try:
        df_upload = pd.read_csv(uploaded_file)

        if df_upload.empty:
            return None, "O arquivo CSV está vazio."

        return df_upload, None

    except Exception as erro:
        return None, f"Erro ao ler o arquivo: {erro}"


# =========================================================
# CABEÇALHO
# =========================================================

st.title("📂 Base de Dados")

st.caption(
    "Importe, visualize e exporte arquivos CSV "
    "para complementar as análises do EcoMonitor Brasil."
)

st.divider()


# =========================================================
# INFORMAÇÕES
# =========================================================

col1, col2 = st.columns([1.4, 1])

with col1:

    with st.container(border=True):

        st.markdown("## ⬆️ Importar Arquivo")

        arquivo_enviado = st.file_uploader(
            "Arraste ou selecione um arquivo CSV",
            type=["csv"],
        )


with col2:

    with st.container(border=True):

        st.markdown("## ℹ️ Como Funciona")

        st.markdown(
            """
            **1.** Envie um arquivo CSV.

            **2.** O sistema valida o conteúdo.

            **3.** Os dados são exibidos na aplicação.

            **4.** O arquivo pode ser exportado novamente.
            """
        )


# =========================================================
# PROCESSAMENTO DO ARQUIVO
# =========================================================

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


        # =================================================
        # MÉTRICAS
        # =================================================

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "📄 Linhas",
                len(df_upload),
            )

        with m2:

            st.metric(
                "📊 Colunas",
                len(df_upload.columns),
            )

        with m3:

            st.metric(
                "💾 Tamanho",
                f"{arquivo_enviado.size / 1024:.1f} KB",
            )


        # =================================================
        # SESSION STATE
        # =================================================

        st.session_state["dados_upload"] = (
            df_upload
        )


        # =================================================
        # VISUALIZAÇÃO
        # =================================================

        st.markdown(
            "## 👀 Prévia dos Dados"
        )

        with st.container(
            border=True
        ):

            st.dataframe(
                df_upload,
                width="stretch",
                hide_index=True,
            )


        # =================================================
        # INFORMAÇÕES DAS COLUNAS
        # =================================================

        st.markdown(
            "## 🔎 Estrutura do Arquivo"
        )

        df_estrutura = pd.DataFrame(
            {
                "Coluna": df_upload.columns,
                "Tipo": [
                    str(tipo)
                    for tipo
                    in df_upload.dtypes
                ],
                "Valores nulos": [
                    int(
                        df_upload[coluna]
                        .isna()
                        .sum()
                    )
                    for coluna
                    in df_upload.columns
                ],
            }
        )

        st.dataframe(
            df_estrutura,
            width="stretch",
            hide_index=True,
        )


        # =================================================
        # ESTATÍSTICAS
        # =================================================

        colunas_numericas = (
            df_upload
            .select_dtypes(
                include="number"
            )
            .columns
        )

        if len(colunas_numericas) > 0:

            with st.expander(
                "📊 Estatísticas descritivas"
            ):

                st.dataframe(
                    df_upload[
                        colunas_numericas
                    ].describe(),
                    width="stretch",
                )


        # =================================================
        # DOWNLOAD
        # =================================================

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
            label="⬇️ Baixar CSV processado",
            data=csv_download,
            file_name="dados_ecomonitor.csv",
            mime="text/csv",
        )


# =========================================================
# DADOS MANTIDOS NA SESSÃO
# =========================================================

if "dados_upload" in st.session_state:

    st.caption(
        "✅ Os dados enviados permanecem "
        "disponíveis durante esta sessão."
    )


# =========================================================
# NAVEGAÇÃO
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "paginas/radar_ambiental.py",
        label="← Radar Ambiental",
        icon="📰",
    )

with col2:

    st.page_link(
        "paginas/sobre.py",
        label="Ir para Sobre",
        icon="🌎",
    )
import requests
import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURAÇÃO
# =========================================================

API_BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# CABEÇALHO
# =========================================================

st.title("🔌 API EcoMonitor")

st.caption(
    "Integração entre a aplicação Streamlit "
    "e a API desenvolvida com FastAPI."
)

st.divider()


# =========================================================
# STATUS DA API
# =========================================================

st.markdown("## 🟢 Status da API")

try:

    response = requests.get(
        f"{API_BASE_URL}/",
        timeout=5,
    )

    if response.status_code == 200:

        dados_status = response.json()

        st.success(
            "API conectada com sucesso."
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Aplicação",
                dados_status.get(
                    "aplicacao",
                    "EcoMonitor API",
                ),
            )

        with c2:

            st.metric(
                "Status",
                dados_status.get(
                    "status",
                    "online",
                ),
            )

        with c3:

            st.metric(
                "Versão",
                dados_status.get(
                    "versao",
                    "-",
                ),
            )

    else:

        st.error(
            f"A API respondeu com status "
            f"{response.status_code}."
        )

except requests.RequestException:

    st.error(
        "Não foi possível conectar à API."
    )

    st.info(
        "Verifique se o FastAPI está rodando em:\n\n"
        "`http://127.0.0.1:8000`"
    )


# =========================================================
# CONSULTA PRODES
# =========================================================

st.divider()

st.markdown("## 🌳 Consultar dados PRODES")

st.caption(
    "Consulta realizada através do endpoint GET /prodes."
)

col1, col2 = st.columns(2)

with col1:

    uf = st.text_input(
        "UF",
        placeholder="Exemplo: Acre",
    )

with col2:

    ano = st.number_input(
        "Ano",
        min_value=1988,
        max_value=2100,
        value=None,
        step=1,
    )


if st.button(
    "🔎 Consultar PRODES"
):

    params = {}

    if uf.strip():

        params["uf"] = (
            uf.strip()
        )

    if ano is not None:

        params["ano"] = int(
            ano
        )


    try:

        response = requests.get(
            f"{API_BASE_URL}/prodes",
            params=params,
            timeout=10,
        )

        if response.status_code == 200:

            resultado = response.json()

            dados = resultado.get(
                "dados",
                [],
            )

            st.success(
                f"{resultado.get('total_registros', 0)} "
                "registro(s) encontrado(s)."
            )

            if dados:

                df = pd.DataFrame(
                    dados
                )

                st.dataframe(
                    df,
                    width="stretch",
                    hide_index=True,
                )

        elif response.status_code == 404:

            st.warning(
                response.json().get(
                    "detail",
                    "Nenhum dado encontrado.",
                )
            )

        else:

            st.error(
                f"Erro na consulta: "
                f"{response.status_code}"
            )

    except requests.RequestException as erro:

        st.error(
            "Erro ao consultar a API."
        )

        st.code(
            str(erro)
        )


# =========================================================
# CONSULTA DE NOTÍCIAS
# =========================================================

st.divider()

st.markdown(
    "## 📰 Notícias via API"
)

st.caption(
    "Consulta realizada através do endpoint GET /noticias."
)


if st.button(
    "📰 Carregar notícias"
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/noticias",
            timeout=10,
        )

        if response.status_code == 200:

            resultado = response.json()

            dados = resultado.get(
                "dados",
                [],
            )

            st.success(
                f"{resultado.get('total_noticias', 0)} "
                "notícia(s) encontrada(s)."
            )

            if dados:

                df_noticias = pd.DataFrame(
                    dados
                )

                st.dataframe(
                    df_noticias,
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

        else:

            st.error(
                f"Erro na consulta: "
                f"{response.status_code}"
            )

    except requests.RequestException as erro:

        st.error(
            "Erro ao acessar o endpoint "
            "de notícias."
        )

        st.code(
            str(erro)
        )


# =========================================================
# POST — NOVO REGISTRO AMBIENTAL
# =========================================================

st.divider()

st.markdown(
    "## ➕ Enviar Registro Ambiental"
)

st.caption(
    "Envio de dados através do endpoint POST /registros."
)


with st.form(
    "form_registro_ambiental"
):

    col1, col2 = st.columns(2)

    with col1:

        localidade = st.text_input(
            "📍 Localidade",
            placeholder="Exemplo: Cuiabá - MT",
        )

        indicador = st.text_input(
            "📊 Indicador",
            placeholder="Exemplo: Temperatura Máxima",
        )

        valor = st.number_input(
            "🔢 Valor",
            value=0.0,
            step=0.1,
        )

    with col2:

        unidade = st.text_input(
            "📐 Unidade",
            placeholder="Exemplo: °C",
        )

        fonte = st.text_input(
            "🔗 Fonte",
            value="Usuário EcoMonitor",
        )

    enviar = st.form_submit_button(
        "📤 Enviar Registro"
    )


if enviar:

    if (
        not localidade.strip()
        or not indicador.strip()
        or not unidade.strip()
    ):

        st.warning(
            "Preencha localidade, indicador e unidade."
        )

    else:

        payload = {
            "localidade":
                localidade.strip(),

            "indicador":
                indicador.strip(),

            "valor":
                float(valor),

            "unidade":
                unidade.strip(),

            "fonte":
                fonte.strip()
                if fonte.strip()
                else "Usuário EcoMonitor",
        }


        try:

            response = requests.post(
                f"{API_BASE_URL}/registros",
                json=payload,
                timeout=10,
            )

            if response.status_code == 201:

                resultado = response.json()

                st.success(
                    resultado.get(
                        "mensagem",
                        "Registro enviado com sucesso.",
                    )
                )

                st.json(
                    resultado.get(
                        "registro",
                        payload,
                    )
                )

            else:

                st.error(
                    f"Erro ao enviar registro: "
                    f"{response.status_code}"
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.write(
                        response.text
                    )

        except requests.RequestException as erro:

            st.error(
                "Erro ao enviar dados para a API."
            )

            st.code(
                str(erro)
            )


# =========================================================
# GET — REGISTROS ENVIADOS
# =========================================================

st.divider()

st.markdown(
    "## 📋 Registros Ambientais Enviados"
)

st.caption(
    "Consulta realizada através do endpoint GET /registros."
)


if st.button(
    "📥 Atualizar registros"
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/registros",
            timeout=10,
        )

        if response.status_code == 200:

            resultado = response.json()

            dados = resultado.get(
                "dados",
                [],
            )

            total = resultado.get(
                "total_registros",
                0,
            )

            if dados:

                st.success(
                    f"{total} registro(s) encontrado(s)."
                )

                df_registros = pd.DataFrame(
                    dados
                )

                st.dataframe(
                    df_registros,
                    width="stretch",
                    hide_index=True,
                )

            else:

                st.info(
                    "Ainda não existem "
                    "registros ambientais enviados."
                )

        else:

            st.error(
                f"Erro na consulta: "
                f"{response.status_code}"
            )

    except requests.RequestException as erro:

        st.error(
            "Erro ao carregar registros."
        )

        st.code(
            str(erro)
        )


# =========================================================
# INFORMAÇÕES DA INTEGRAÇÃO
# =========================================================

st.divider()

with st.expander(
    "ℹ️ Como funciona a integração"
):

    st.markdown(
        """
        A aplicação **Streamlit** funciona como interface para o usuário,
        enquanto o **FastAPI** disponibiliza os dados através de endpoints.

        Nesta página, o EcoMonitor utiliza:

        - `GET /prodes` para consultar dados de desmatamento;
        - `GET /noticias` para consultar notícias ambientais;
        - `POST /registros` para enviar novos registros;
        - `GET /registros` para recuperar os registros enviados.

        Dessa forma, o Streamlit consome a própria API do projeto,
        demonstrando a integração entre a interface e o serviço FastAPI.
        """
    )


# =========================================================
# NAVEGAÇÃO
# =========================================================

st.divider()

st.page_link(
    "paginas/inicio.py",
    label="← Voltar para o Início",
    icon="🏠",
)
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# =========================================================
# CAMINHOS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

PRODES_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "desmatamento_prodes.csv"
)

NOTICIAS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "noticias_inpe.csv"
)

REGISTROS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "registros_ambientais.csv"
)


# =========================================================
# CONFIGURAÇÃO DA API
# =========================================================

app = FastAPI(
    title="EcoMonitor Brasil API",
    description=(
        "API para consulta e envio de dados ambientais "
        "utilizados pela plataforma EcoMonitor Brasil."
    ),
    version="1.0.0",
)


# =========================================================
# MODELO DO POST
# =========================================================

class RegistroAmbiental(BaseModel):

    localidade: str = Field(
        ...,
        min_length=2,
        description="Nome da localidade do registro.",
        examples=["Cuiabá - MT"],
    )

    indicador: str = Field(
        ...,
        min_length=2,
        description="Indicador ambiental registrado.",
        examples=["Temperatura Máxima"],
    )

    valor: float = Field(
        ...,
        description="Valor numérico do indicador.",
        examples=[35.8],
    )

    unidade: str = Field(
        ...,
        min_length=1,
        description="Unidade de medida do indicador.",
        examples=["°C"],
    )

    fonte: str = Field(
        default="Usuário",
        description="Fonte do dado informado.",
        examples=["Coleta manual"],
    )


# =========================================================
# ROTA INICIAL
# =========================================================

@app.get(
    "/",
    summary="Verificar funcionamento da API",
    description=(
        "Retorna informações básicas sobre "
        "o funcionamento da EcoMonitor Brasil API."
    ),
)
def inicio():

    return {
        "aplicacao": "EcoMonitor Brasil API",
        "status": "online",
        "versao": "1.0.0",
    }


# =========================================================
# GET — DADOS PRODES
# =========================================================

@app.get(
    "/prodes",
    summary="Consultar dados de desmatamento PRODES",
    description=(
        "Consulta os dados históricos de desmatamento "
        "coletados do PRODES/INPE. "
        "É possível filtrar por UF e por ano."
    ),
)
def consultar_prodes(
    uf: str | None = None,
    ano: int | None = None,
):

    if not PRODES_PATH.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "Arquivo de dados PRODES "
                "não encontrado."
            ),
        )

    df = pd.read_csv(
        PRODES_PATH
    )

    if uf:

        df = df[
            df["UF"]
            .astype(str)
            .str.lower()
            == uf.lower()
        ]

    if ano is not None:

        df = df[
            df["Ano"]
            == ano
        ]

    if df.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                "Nenhum registro encontrado "
                "para os filtros informados."
            ),
        )

    return {
        "total_registros": len(df),
        "dados": df.to_dict(
            orient="records"
        ),
    }


# =========================================================
# GET — NOTÍCIAS
# =========================================================

@app.get(
    "/noticias",
    summary="Consultar notícias ambientais do INPE",
    description=(
        "Retorna as notícias ambientais coletadas "
        "do portal do INPE por Web Scraping."
    ),
)
def consultar_noticias():

    if not NOTICIAS_PATH.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                "Arquivo de notícias "
                "não encontrado."
            ),
        )

    df = pd.read_csv(
        NOTICIAS_PATH
    )

    return {
        "total_noticias": len(df),
        "dados": df[
            [
                "titulo",
                "url",
            ]
        ].to_dict(
            orient="records"
        ),
    }


# =========================================================
# POST — NOVO REGISTRO AMBIENTAL
# =========================================================

@app.post(
    "/registros",
    status_code=201,
    summary="Enviar novo registro ambiental",
    description=(
        "Recebe um novo registro ambiental "
        "e armazena o dado em arquivo CSV."
    ),
)
def criar_registro(
    registro: RegistroAmbiental
):

    novo_registro = pd.DataFrame(
        [
            {
                "localidade":
                    registro.localidade,

                "indicador":
                    registro.indicador,

                "valor":
                    registro.valor,

                "unidade":
                    registro.unidade,

                "fonte":
                    registro.fonte,
            }
        ]
    )


    if REGISTROS_PATH.exists():

        df_existente = pd.read_csv(
            REGISTROS_PATH
        )

        df_final = pd.concat(
            [
                df_existente,
                novo_registro,
            ],
            ignore_index=True,
        )

    else:

        df_final = novo_registro


    df_final.to_csv(
        REGISTROS_PATH,
        index=False,
        encoding="utf-8-sig",
    )


    return {
        "mensagem":
            "Registro ambiental criado com sucesso.",

        "registro":
            registro.model_dump(),
    }


# =========================================================
# GET — REGISTROS ENVIADOS
# =========================================================

@app.get(
    "/registros",
    summary="Consultar registros ambientais enviados",
    description=(
        "Retorna os registros ambientais "
        "adicionados através da rota POST /registros."
    ),
)
def consultar_registros():

    if not REGISTROS_PATH.exists():

        return {
            "total_registros": 0,
            "dados": [],
        }


    df = pd.read_csv(
        REGISTROS_PATH
    )


    return {
        "total_registros": len(df),
        "dados": df.to_dict(
            orient="records"
        ),
    }
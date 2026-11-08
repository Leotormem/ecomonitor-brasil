from transformers import pipeline


MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)

CATEGORIAS = [
    "queimada",
    "desmatamento",
    "clima",
    "biodiversidade",
    "poluicao",
    "monitoramento ambiental",
]

MAPEAMENTO_CATEGORIAS = {
    "monitoramento ambiental":
        "monitoramento_ambiental",
}


def carregar_modelo():

    classificador = pipeline(
        "zero-shot-classification",
        model=MODELO,
        local_files_only=True,
    )

    return classificador


def classificar_texto(
    classificador,
    texto: str,
):

    resultado = classificador(
        texto,
        candidate_labels=CATEGORIAS,
        hypothesis_template=(
            "Este texto ambiental é sobre {}."
        ),
    )

    categoria_modelo = (
        resultado["labels"][0]
    )

    categoria = (
        MAPEAMENTO_CATEGORIAS.get(
            categoria_modelo,
            categoria_modelo,
        )
    )

    confianca = float(
        resultado["scores"][0]
    )

    return {
        "categoria_sugerida":
            categoria,
        "confianca":
            confianca,
        "pistas": [],
        "motor":
            MODELO,
    }
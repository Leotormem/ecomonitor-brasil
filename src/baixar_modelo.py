from transformers import AutoModelForSequenceClassification, AutoTokenizer


MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)


def baixar_modelo():

    print(
        "Baixando tokenizer..."
    )

    AutoTokenizer.from_pretrained(
        MODELO
    )

    print(
        "Baixando modelo..."
    )

    AutoModelForSequenceClassification.from_pretrained(
        MODELO
    )

    print()
    print(
        "Modelo baixado e armazenado "
        "no cache local com sucesso."
    )


if __name__ == "__main__":
    baixar_modelo()
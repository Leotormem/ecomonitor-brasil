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

TEXTO = (
    "Satélites registram aumento da área desmatada "
    "em região da Amazônia."
)


print("Carregando modelo...")

classificador = pipeline(
    "zero-shot-classification",
    model=MODELO,
)

print("Modelo carregado.")

resultado = classificador(
    TEXTO,
    candidate_labels=CATEGORIAS,
    hypothesis_template="Este texto ambiental é sobre {}.",
)

print("\nTexto:")
print(TEXTO)

print("\nResultado:")
for categoria, pontuacao in zip(
    resultado["labels"],
    resultado["scores"],
):
    print(
        f"{categoria}: "
        f"{pontuacao:.4f}"
    )
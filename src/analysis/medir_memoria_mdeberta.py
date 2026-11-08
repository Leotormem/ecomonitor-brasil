from transformers import pipeline


MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)


print("Carregando modelo...")

classificador = pipeline(
    "zero-shot-classification",
    model=MODELO,
)

print("Modelo carregado.")


memoria_bytes = sum(
    parametro.numel()
    * parametro.element_size()
    for parametro
    in classificador.model.parameters()
)

memoria_mb = (
    memoria_bytes
    / 1024
    / 1024
)

memoria_gb = (
    memoria_mb
    / 1024
)

parametros = sum(
    parametro.numel()
    for parametro
    in classificador.model.parameters()
)


print("\n==============================")
print("CUSTO DO MODELO")
print("==============================")

print(
    f"Parâmetros: "
    f"{parametros:,}"
)

print(
    f"Memória aproximada: "
    f"{memoria_mb:.2f} MB"
)

print(
    f"Memória aproximada: "
    f"{memoria_gb:.2f} GB"
)
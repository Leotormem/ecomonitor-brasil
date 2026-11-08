from transformers import pipeline


MODELO = "Qwen/Qwen2.5-1.5B-Instruct"

CATEGORIAS = [
    "queimada",
    "desmatamento",
    "clima",
    "biodiversidade",
    "poluicao",
    "monitoramento_ambiental",
]

TEXTO = (
    "Satélites registram aumento da área desmatada "
    "em região da Amazônia."
)

PROMPT = f"""
Classifique o texto ambiental abaixo em apenas uma categoria.

Categorias disponíveis:
{", ".join(CATEGORIAS)}

Texto:
{TEXTO}

Responda somente com o nome exato de uma categoria.
"""


print("Carregando modelo...")

gerador = pipeline(
    "text-generation",
    model=MODELO,
    dtype="auto",
)

print("Modelo carregado.")

resultado = gerador(
    PROMPT,
    max_new_tokens=30,
    do_sample=False,
)

texto_gerado = resultado[0]["generated_text"]

print("\nResposta completa:")
print(texto_gerado)
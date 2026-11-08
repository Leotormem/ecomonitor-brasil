from pathlib import Path
from time import perf_counter

import pandas as pd
from transformers import pipeline


ROOT_DIR = Path(__file__).resolve().parents[2]

ARQUIVO_BANCO = (
    ROOT_DIR
    / "data"
    / "analisador"
    / "banco_de_provas.csv"
)

MODELO = "Qwen/Qwen2.5-1.5B-Instruct"

CATEGORIAS = [
    "queimada",
    "desmatamento",
    "clima",
    "biodiversidade",
    "poluicao",
    "monitoramento_ambiental",
]


def extrair_categoria(texto):
    texto = texto.lower()

    for categoria in CATEGORIAS:
        if categoria.lower() in texto:
            return categoria

    return None


print("Carregando banco de provas...")

df = pd.read_csv(ARQUIVO_BANCO)

print(f"Total de exemplos: {len(df)}")

print("\nCarregando modelo...")

inicio_carregamento = perf_counter()

gerador = pipeline(
    "text-generation",
    model=MODELO,
    dtype="auto",
)

tempo_carregamento = (
    perf_counter()
    - inicio_carregamento
)

print(
    f"Modelo carregado em "
    f"{tempo_carregamento:.2f} segundos."
)

resultados = []

print("\nIniciando avaliação...\n")

for indice, linha in df.iterrows():

    texto = linha["texto"]
    esperado = linha["categoria_esperada"]

    prompt = f"""
Classifique o texto ambiental abaixo em apenas uma categoria.

Categorias disponíveis:
{", ".join(CATEGORIAS)}

Texto:
{texto}

Responda somente com o nome exato de uma categoria.
"""

    inicio = perf_counter()

    resposta = gerador(
        prompt,
        max_new_tokens=20,
        do_sample=False,
    )

    tempo = perf_counter() - inicio

    texto_gerado = resposta[0]["generated_text"]

    resposta_nova = texto_gerado[len(prompt):].strip()

    categoria_prevista = extrair_categoria(
        resposta_nova
    )

    acertou = (
        categoria_prevista
        == esperado
    )

    resultados.append(
        {
            "texto": texto,
            "categoria_esperada": esperado,
            "categoria_prevista": categoria_prevista,
            "resposta_modelo": resposta_nova,
            "tempo_segundos": round(
                tempo,
                4,
            ),
            "acertou": acertou,
        }
    )

    status = (
        "OK"
        if acertou
        else "ERRO"
    )

    print(
        f"{indice + 1:02d}/"
        f"{len(df)} "
        f"[{status}] "
        f"esperado={esperado} | "
        f"previsto={categoria_prevista} | "
        f"{tempo:.2f}s"
    )


df_resultados = pd.DataFrame(
    resultados
)

total = len(df_resultados)

acertos = int(
    df_resultados["acertou"].sum()
)

erros = total - acertos

sem_resposta = int(
    df_resultados[
        "categoria_prevista"
    ].isna().sum()
)

acuracia = (
    acertos
    / total
    * 100
)

tempo_medio = (
    df_resultados[
        "tempo_segundos"
    ].mean()
)

ARQUIVO_RESULTADO = (
    ROOT_DIR
    / "data"
    / "analisador"
    / "resultado_qwen.csv"
)

df_resultados.to_csv(
    ARQUIVO_RESULTADO,
    index=False,
    encoding="utf-8",
)

print("\n==============================")
print("RESULTADO FINAL")
print("==============================")

print(
    f"Acertos: {acertos}/{total}"
)

print(
    f"Erros: {erros}/{total}"
)

print(
    f"Sem resposta válida: "
    f"{sem_resposta}/{total}"
)

print(
    f"Acurácia: {acuracia:.2f}%"
)

print(
    f"Tempo médio por texto: "
    f"{tempo_medio:.2f}s"
)

print(
    f"Tempo de carregamento: "
    f"{tempo_carregamento:.2f}s"
)

print(
    "\nResultado salvo em:"
)

print(
    ARQUIVO_RESULTADO
)
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

MODELO = (
    "MoritzLaurer/"
    "mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
)

CATEGORIAS_MODELO = [
    "queimada",
    "desmatamento",
    "clima",
    "biodiversidade",
    "poluicao",
    "monitoramento ambiental",
]

MAPEAMENTO_CATEGORIAS = {
    "monitoramento ambiental": "monitoramento_ambiental",
}


print("Carregando banco de provas...")

df = pd.read_csv(ARQUIVO_BANCO)

print(f"Total de exemplos: {len(df)}")

print("\nCarregando modelo...")

inicio_carregamento = perf_counter()

classificador = pipeline(
    "zero-shot-classification",
    model=MODELO,
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

    inicio = perf_counter()

    resposta = classificador(
        texto,
        candidate_labels=CATEGORIAS_MODELO,
        hypothesis_template=(
            "Este texto ambiental é sobre {}."
        ),
    )

    tempo = perf_counter() - inicio

    categoria_modelo = resposta["labels"][0]

    categoria_prevista = MAPEAMENTO_CATEGORIAS.get(
        categoria_modelo,
        categoria_modelo,
    )

    confianca = resposta["scores"][0]

    acertou = (
        categoria_prevista
        == esperado
    )

    resultados.append(
        {
            "texto": texto,
            "categoria_esperada": esperado,
            "categoria_prevista": categoria_prevista,
            "confianca": round(
                float(confianca),
                4,
            ),
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
        f"conf={confianca:.4f} | "
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
    / "resultado_mdeberta.csv"
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
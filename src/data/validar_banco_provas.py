from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
ARQUIVO = ROOT_DIR / "data" / "analisador" / "banco_de_provas.csv"

CATEGORIAS_ESPERADAS = {
    "queimada",
    "desmatamento",
    "clima",
    "biodiversidade",
    "poluicao",
    "monitoramento_ambiental",
}


def validar_banco():
    if not ARQUIVO.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO}"
        )

    df = pd.read_csv(ARQUIVO)

    colunas_esperadas = {
        "texto",
        "categoria_esperada",
    }

    if set(df.columns) != colunas_esperadas:
        raise ValueError(
            "O CSV deve possuir exatamente as colunas: "
            "texto,categoria_esperada"
        )

    if df.empty:
        raise ValueError("O banco de provas está vazio.")

    if df["texto"].isna().any():
        raise ValueError(
            "Existem textos vazios no banco de provas."
        )

    if df["categoria_esperada"].isna().any():
        raise ValueError(
            "Existem categorias vazias no banco de provas."
        )

    categorias_encontradas = set(
        df["categoria_esperada"].unique()
    )

    categorias_invalidas = (
        categorias_encontradas
        - CATEGORIAS_ESPERADAS
    )

    if categorias_invalidas:
        raise ValueError(
            "Categorias inválidas encontradas: "
            f"{sorted(categorias_invalidas)}"
        )

    contagem = (
        df["categoria_esperada"]
        .value_counts()
        .sort_index()
    )

    print("\nBanco de provas validado com sucesso.")
    print(f"Arquivo: {ARQUIVO}")
    print(f"Total de exemplos: {len(df)}")

    print("\nQuantidade por categoria:")
    print(contagem)

    if len(df) != 30:
        print(
            "\nAVISO: o banco possui "
            f"{len(df)} exemplos, e não 30."
        )

    categorias_com_quantidade_diferente = (
        contagem[contagem != 5]
    )

    if not categorias_com_quantidade_diferente.empty:
        print(
            "\nAVISO: algumas categorias "
            "não possuem exatamente 5 exemplos."
        )
        print(categorias_com_quantidade_diferente)


if __name__ == "__main__":
    validar_banco()
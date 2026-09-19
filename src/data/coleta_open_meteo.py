from pathlib import Path

import pandas as pd
import requests


# Caminho da raiz do projeto
ROOT_DIR = Path(__file__).resolve().parents[2]

# Pasta onde os dados brutos serão armazenados
RAW_DIR = ROOT_DIR / "data" / "raw"

# Garante que a pasta exista
RAW_DIR.mkdir(parents=True, exist_ok=True)


def coletar_dados_cuiaba():
    """
    Coleta dados meteorológicos da Open-Meteo para Cuiabá/MT.

    Retorna:
        pandas.DataFrame: DataFrame com data, temperatura máxima,
        temperatura mínima e precipitação.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-15.60"
        "&longitude=-56.10"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=America%2FCuiaba"
    )

    response = requests.get(url, timeout=10)

    # Gera erro caso a API não responda corretamente
    response.raise_for_status()

    dados = response.json()

    df = pd.DataFrame({
        "Data": dados["daily"]["time"],
        "Temperatura Máxima (°C)": dados["daily"]["temperature_2m_max"],
        "Temperatura Mínima (°C)": dados["daily"]["temperature_2m_min"],
        "Precipitação (mm)": dados["daily"]["precipitation_sum"]
    })

    # Caminho do arquivo
    caminho_arquivo = RAW_DIR / "open_meteo_cuiaba.csv"

    # Salva os dados brutos
    df.to_csv(
        caminho_arquivo,
        index=False,
        encoding="utf-8-sig"
    )

    return df


if __name__ == "__main__":

    try:
        df = coletar_dados_cuiaba()

        print(df)

        print(
            "\nDados coletados e salvos com sucesso em:"
            "\ndata/raw/open_meteo_cuiaba.csv"
        )

    except requests.RequestException as erro:
        print(f"Erro ao acessar a Open-Meteo: {erro}")

    except Exception as erro:
        print(f"Erro inesperado: {erro}")
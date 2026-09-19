from pathlib import Path

import pandas as pd
import requests


ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


CIDADES = {
    "Cuiabá - MT": {
        "latitude": -15.60,
        "longitude": -56.10,
        "timezone": "America/Cuiaba"
    },
    "Goiânia - GO": {
        "latitude": -16.68,
        "longitude": -49.25,
        "timezone": "America/Sao_Paulo"
    },
    "Brasília - DF": {
        "latitude": -15.78,
        "longitude": -47.93,
        "timezone": "America/Sao_Paulo"
    },
    "São Paulo - SP": {
        "latitude": -23.55,
        "longitude": -46.63,
        "timezone": "America/Sao_Paulo"
    },
    "Rio de Janeiro - RJ": {
        "latitude": -22.91,
        "longitude": -43.17,
        "timezone": "America/Sao_Paulo"
    }
}


def coletar_dados_meteorologicos(cidade):
    """
    Coleta dados meteorológicos da Open-Meteo
    para a cidade selecionada.
    """

    dados_cidade = CIDADES[cidade]

    latitude = dados_cidade["latitude"]
    longitude = dados_cidade["longitude"]
    timezone = dados_cidade["timezone"]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone={timezone}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    dados = response.json()

    df = pd.DataFrame({
        "Data": dados["daily"]["time"],
        "Temperatura Máxima (°C)": dados["daily"]["temperature_2m_max"],
        "Temperatura Mínima (°C)": dados["daily"]["temperature_2m_min"],
        "Precipitação (mm)": dados["daily"]["precipitation_sum"]
    })

    nome_arquivo = (
        cidade.lower()
        .replace(" ", "_")
        .replace("-", "")
        .replace("á", "a")
        .replace("ã", "a")
        .replace("í", "i")
        .replace("ó", "o")
    )

    caminho_arquivo = RAW_DIR / f"open_meteo_{nome_arquivo}.csv"

    df.to_csv(
        caminho_arquivo,
        index=False,
        encoding="utf-8-sig"
    )

    return df


if __name__ == "__main__":
    cidade = "Cuiabá - MT"

    try:
        df = coletar_dados_meteorologicos(cidade)

        print(df)

        print(
            f"\nDados de {cidade} coletados e salvos com sucesso."
        )

    except requests.RequestException as erro:
        print(f"Erro ao acessar a Open-Meteo: {erro}")

    except Exception as erro:
        print(f"Erro inesperado: {erro}")
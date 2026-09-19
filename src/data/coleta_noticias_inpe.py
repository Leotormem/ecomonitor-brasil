from pathlib import Path
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SITE = "https://www.gov.br"
URL_NOTICIAS = (
    "https://www.gov.br/inpe/pt-br/assuntos/ultimas-noticias"
)

USER_AGENT = "EcoMonitorBrasil/1.0"


def verificar_permissao():
    robots_url = f"{SITE}/robots.txt"

    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.read()

    return parser.can_fetch(USER_AGENT, URL_NOTICIAS)


def coletar_noticias():
    if not verificar_permissao():
        raise PermissionError(
            "A coleta não está permitida pelo robots.txt."
        )

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        URL_NOTICIAS,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    noticias = []

    links = soup.select("a")

    for link in links:
        titulo = link.get_text(
            " ",
            strip=True
        )

        href = link.get("href")

        if not titulo or not href:
            continue

        # Mantém apenas links relacionados às notícias do INPE
        if "/inpe/pt-br/assuntos/ultimas-noticias/" not in href:
            continue

        if href.startswith("/"):
            href = SITE + href

        noticias.append({
            "titulo": titulo,
            "url": href
        })

    df = pd.DataFrame(noticias)

    if df.empty:
        raise ValueError(
            "Nenhuma notícia foi encontrada na página."
        )

    # Remove duplicações
    df = df.drop_duplicates(
        subset=["titulo", "url"]
    )

    caminho_csv = (
        PROCESSED_DIR /
        "noticias_inpe.csv"
    )

    df.to_csv(
        caminho_csv,
        index=False,
        encoding="utf-8-sig"
    )

    return df


if __name__ == "__main__":
    try:
        df = coletar_noticias()

        print(df.head(10))

        print(
            "\nColeta concluída com sucesso."
            "\nArquivo salvo em:"
            "\ndata/processed/noticias_inpe.csv"
        )

    except Exception as erro:
        print(f"Erro durante a coleta: {erro}")
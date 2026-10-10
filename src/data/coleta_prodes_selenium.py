from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# =========================================================
# CAMINHOS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# FONTE
# =========================================================

URL_PRODES = (
    "https://www.terrabrasilis.dpi.inpe.br/"
    "app/dashboard/deforestation/"
)

ARQ_SNAPSHOT = (
    RAW_DIR
    / "terrabrasilis_prodes_renderizado.html"
)

ARQ_CSV = (
    PROCESSED_DIR
    / "desmatamento_prodes.csv"
)


# =========================================================
# ABRIR NAVEGADOR
# =========================================================

def abrir_navegador():

    opcoes = webdriver.ChromeOptions()

    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--disable-gpu")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        options=opcoes
    )

    return driver


# =========================================================
# ESPERAR TABELA COMPLETA
# =========================================================

def esperar_tabela(driver):

    def tabela_completa(d):

        grupos_uf = d.find_elements(
            By.CSS_SELECTOR,
            "#tb-area tr.dc-table-group"
        )

        linhas_ano = d.find_elements(
            By.CSS_SELECTOR,
            "#tb-area tr.dc-table-row"
        )

        return (
            len(grupos_uf) >= 9
            and len(linhas_ano) > 0
        )

    WebDriverWait(
        driver,
        60,
        poll_frequency=0.25
    ).until(
        tabela_completa,
        message=(
            "A tabela do PRODES não "
            "ficou completa a tempo."
        )
    )


# =========================================================
# EXTRAIR TABELA
# =========================================================

def extrair_tabela(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    tabela = soup.select_one(
        "#tb-area"
    )

    if tabela is None:
        raise ValueError(
            "Tabela do PRODES não encontrada."
        )

    dados = []

    uf_atual = None

    for linha in tabela.select("tr"):

        classes = linha.get(
            "class",
            []
        )

        texto = linha.get_text(
            " ",
            strip=True
        )

        if not texto:
            continue


        # ---------------------------------------------
        # LINHA DE ESTADO
        # ---------------------------------------------

        if "dc-table-group" in classes:

            uf_atual = (
                texto
                .split(" - ")[0]
                .strip()
            )

            continue


        # ---------------------------------------------
        # LINHA DE ANO
        # ---------------------------------------------

        if "dc-table-row" in classes:

            colunas = [
                td.get_text(
                    " ",
                    strip=True
                )
                for td
                in linha.select("td")
            ]

            if len(colunas) < 2:
                continue

            ano = colunas[0]

            area = colunas[-1]

            dados.append(
                {
                    "UF": uf_atual,
                    "Ano": ano,
                    "Area_km2": area,
                }
            )


    if not dados:
        raise ValueError(
            "Nenhum dado foi extraído "
            "da tabela do PRODES."
        )


    df = pd.DataFrame(
        dados
    )


    # =====================================================
    # LIMPEZA
    # =====================================================

    df["UF"] = (
        df["UF"]
        .astype(str)
        .str.strip()
    )

    df["Ano"] = pd.to_numeric(
        df["Ano"],
        errors="coerce"
    )

    df["Area_km2"] = (
        df["Area_km2"]
        .astype(str)
        .str.replace(
            "km²",
            "",
            regex=False
        )
        .str.strip()
        .str.replace(
            ".",
            "",
            regex=False
        )
        .str.replace(
            ",",
            ".",
            regex=False
        )
    )

    df["Area_km2"] = pd.to_numeric(
        df["Area_km2"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "UF",
            "Ano",
            "Area_km2",
        ]
    )

    df["Ano"] = (
        df["Ano"]
        .astype(int)
    )


    return df


# =========================================================
# COLETA PRINCIPAL
# =========================================================

def coletar_prodes():

    driver = abrir_navegador()

    try:

        print(
            "Abrindo TerraBrasilis..."
        )

        driver.get(
            URL_PRODES
        )

        print(
            "Aguardando dados do PRODES..."
        )

        esperar_tabela(
            driver
        )

        html = (
            driver.page_source
        )

    finally:

        driver.quit()


    # =====================================================
    # SNAPSHOT
    # =====================================================

    ARQ_SNAPSHOT.write_text(
        html,
        encoding="utf-8"
    )


    # =====================================================
    # EXTRAÇÃO
    # =====================================================

    df = extrair_tabela(
        html
    )


    # =====================================================
    # SEGURANÇA DA COLETA
    # =====================================================

    if df.empty:

        raise ValueError(
            "A coleta retornou zero linhas. "
            "O CSV anterior não será sobrescrito."
        )


    if df["UF"].nunique() < 9:

        raise ValueError(
            "A coleta não encontrou "
            "as 9 UFs esperadas."
        )


    # =====================================================
    # SALVAR
    # =====================================================

    df.to_csv(
        ARQ_CSV,
        index=False,
        encoding="utf-8-sig"
    )


    return df


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    try:

        df = coletar_prodes()

        print()
        print(
            "Coleta concluída com sucesso."
        )

        print(
            f"Linhas: {len(df)}"
        )

        print(
            f"UFs: {df['UF'].nunique()}"
        )

        print(
            f"Anos: "
            f"{df['Ano'].min()} "
            f"a "
            f"{df['Ano'].max()}"
        )

        print()
        print(
            "Estados encontrados:"
        )

        print(
            sorted(
                df["UF"]
                .dropna()
                .unique()
            )
        )

        print()
        print(
            "Arquivo salvo em:"
        )

        print(
            ARQ_CSV
        )

    except Exception as erro:

        print()
        print(
            "Erro durante a coleta:"
        )

        print(
            erro
        )
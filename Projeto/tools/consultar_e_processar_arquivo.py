import os
import tempfile
import zipfile
import requests
import pandas as pd
from typing import Any
from langchain.tools import tool

@tool("consultar_e_processar_arquivo")
def consultar_e_processar_arquivo(params: dict) -> Any:
    """
    Baixa arquivos da base e processa os dados.

    Parâmetros esperados em *params*:
    - package_id (str): ID do pacote no Dados Abertos RJ
    - file_filter (str): filtro por nome do arquivo
    - operation (str): contar_linhas | media | soma
    
    """
    try:
        package_id = params.get("package_id")
        file_filter = params.get("file_filter", "")
        operation = params.get("operation", "contar_linhas")

        if not package_id:
            return {"erro": "Parâmetro 'package_id' é obrigatório."}

        url = f"https://dadosabertos.rj.gov.br/api/3/action/package_show?id={package_id}"
        resp = requests.get(url).json()

        if "result" not in resp:
            return {"erro": "Pacote não encontrado."}

        resources = resp["result"].get("resources", [])

        arquivos_filtrados = [ # filtrar aquivo pelo nome 
            r for r in resources if file_filter.lower() in r.get("name", "").lower()
        ]

        if not arquivos_filtrados:
            return {"erro": f"Nenhum arquivo encontrado com filtro: {file_filter}"}

        resultados = {}

        for resource in arquivos_filtrados:
            nome = resource.get("name")
            url_arquivo = resource.get("url")

            tmp_dir = tempfile.mkdtemp()
            caminho_arquivo = os.path.join(tmp_dir, nome)

            response = requests.get(url_arquivo)
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)

            if nome.lower().endswith(".zip"):
                try:
                    with zipfile.ZipFile(caminho_arquivo, "r") as zip_ref:
                        zip_ref.extractall(tmp_dir)

                    csvs = [
                        os.path.join(tmp_dir, f)
                        for f in os.listdir(tmp_dir)
                        if f.lower().endswith(".csv")
                    ]

                    if not csvs:
                        resultados[nome] = "ZIP extraído, mas nenhum CSV encontrado."
                        continue

                    df = pd.read_csv(csvs[0])

                except Exception as e:
                    resultados[nome] = f"Erro ao extrair ZIP: {str(e)}"
                    continue
            else:
                df = pd.read_csv(caminho_arquivo)

            if operation == "contar_linhas":
                resultados[nome] = len(df)

            elif operation == "media":
                resultados[nome] = df.mean(numeric_only=True).to_dict()

            elif operation == "soma":
                resultados[nome] = df.sum(numeric_only=True).to_dict()

            else:
                resultados[nome] = f"Operação desconhecida: {operation}"
            
            #if graph_state is not None:
            #    graph_state.set_state(f"nome do arquivo: {nome}", df)

        return resultados

    except Exception as e:
        return {"erro": f"Falha ao processar arquivo: {str(e)}"}

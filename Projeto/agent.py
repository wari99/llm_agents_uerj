import os
from typing import Any, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from dataclasses import dataclass
import requests 

from prompt import prompt
import tempfile
import pandas as pd

os.environ["GOOGLE_API_KEY"] = ""
RAG_DIR = ""

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    summary: str

@tool("ler_arquivo_rag") #####
def ler_arquivo_rag(nome_do_arquivo: str) -> str:
    """
        Ferramenta utilizada para ler o conteúdo dos arquivos

    """
    if not os.path.exists(RAG_DIR):
        return "erro:  não encontrada."
    
    arquivos = os.listdir(RAG_DIR)
    if not arquivos:
        return "Nenhum arquivo encontrado na pasta RAG."

    return "\n".join(arquivos)

@tool("listar_bases")
def listar_bases(_: str = "") -> Any:
    """
    Retorna a lista de todas as bases disponíveis no Dados Abertos do RJ.
    Consulta o endpoint oficial package_list.
    """
    url = "https://dadosabertos.rj.gov.br/api/3/action/package_list"
    try:
        resp = requests.get(url).json()
        return resp.get("result", [])
    
    except Exception as e:
        return {"erro": f"Falha ao consultar API: {str(e)}"}

@tool("buscar_infos_base")
def buscar_infos_base(base_nome: str) -> Any:
    """
    Busca informações detalhadas de uma base específica do portal Dados Abertos RJ ao usar o endpoint de package_search.
    """
    url = f"https://dadosabertos.rj.gov.br/api/3/action/package_search?q={base_nome}"
    try:
        resp = requests.get(url).json()
        return resp.get("result", {})
    
    except Exception as e:
        return {"erro": f"Falha ao consultar API: {str(e)}"}


@tool("consultar_e_processar_arquivo")
def consultar_e_processar_arquivo(params: dict) -> Any:
    """
    Consulta um package_id específico, filtra arquivos pelo nome e realiza operações de média, soma ou contagem de linhas nos arquivos CSV.
    
    Espera:
    {
        "package_id": "...",
        "file_filter": "2025-07" ou "2025-10-03.csv",
        "operation": "media" | "soma" | "contar_linhas"
    }
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

        encontrou_recurso = [r for r in resources if file_filter.lower() in r["name"].lower()]

        if not encontrou_recurso:
            return {"erro": f"Nenhum arquivo encontrado contendo: {file_filter}"}

        resultados = {}

        for resource in encontrou_recurso:
            url_arquivo = resource.get("url")
            nome = resource.get("name")
            formato = resource.get("format", "").lower()

            tmp_dir = tempfile.mkdtemp() # criação da pasta temporaria
            file_path = os.path.join(tmp_dir, nome)

            conteudo = requests.get(url_arquivo)
            with open(file_path, "wb") as f:
                f.write(conteudo.content)

            if formato == "csv": # começando pelo csv por enqt
                df = pd.read_csv(file_path)

                if operation == "contar_linhas":
                    resultados[nome] = len(df)

                elif operation == "media":
                    resultados[nome] = df.mean(numeric_only=True).to_dict()

                elif operation == "soma":
                    resultados[nome] = df.sum(numeric_only=True).to_dict()

                else:
                    resultados[nome] = f"Operação desconhecida: {operation}"

            else:
                resultados[nome] = f"Formato ainda nao suportado: {formato}"

        return resultados

    except Exception as e:
        return {"erro": f"Falha ao processar arquivo: {str(e)}"}


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

agent = create_agent(
    model=model,
    context_schema=Context,
    system_prompt=prompt,
    tools = [
        ler_arquivo_rag,
        listar_bases,
        buscar_infos_base,
        consultar_e_processar_arquivo
    ]

)

graph = StateGraph(AgentState)

graph.add_node("inicio", agent)

graph.set_entry_point("inicio")

checkpointer = InMemorySaver()

agent_memory = graph.compile(
    checkpointer=checkpointer
)

print("Bem vindo ao ARCOS-RJ! Digite '/sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "/sair": 
        print("ARCOS-RJ: Até logo!")
        break

    resultado = agent_memory.invoke(
        {"messages": [{"role": "user", "content": pergunta}]},
        config={"thread_id": "1"}
    )

    #resposta = resultado["messages"][-1].content
    #resposta = resultado["messages"][-1].content[0]["text"]

    mensagens = resultado["messages"][-1].content

    if isinstance(mensagens, list) and len(mensagens) > 0 and "text" in mensagens[0]:
        resposta = mensagens[0]["text"]
    else:
        resposta = str(mensagens)

    print("ARCOS-RJ:", resposta)


    

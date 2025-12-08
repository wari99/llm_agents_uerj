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

os.environ["GOOGLE_API_KEY"] = ""
RAG_DIR = r""

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
    Busca informações detalhadas de uma base específica do portal Dados Abertos RJ,
    usando o endpoint package_search.
    """
    url = f"https://dadosabertos.rj.gov.br/api/3/action/package_search?q={base_nome}"
    try:
        resp = requests.get(url).json()
        return resp.get("result", {})
    except Exception as e:
        return {"erro": f"Falha ao consultar API: {str(e)}"}


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
        buscar_infos_base
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


    

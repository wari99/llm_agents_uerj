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

from tools.listar_bases import listar_bases
from tools.buscar_infos_base import buscar_infos_base
from tools.consultar_e_processar_arquivo import consultar_e_processar_arquivo
from tools.ler_arquivo_rag import ler_arquivo_rag


os.environ["GOOGLE_API_KEY"] = ""
RAG_DIR = ""

@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str

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

#graph.add_node("listar_bases", listar_bases)
#graph.add_node("buscar_infos_base", buscar_infos_base)
#graph.add_node("consultar_e_processar_arquivo", consultar_e_processar_arquivo)

#graph.add_edge("inicio", "listar_bases")
#graph.add_edge("listar_bases", "buscar_infos_base")
#graph.add_edge("buscar_infos_base", "consultar_e_processar_arquivo")

# OU SEJA logica é inicio -> listar bases -> buscar infos base -> consultar e processar o arquivo (aqui dentro em processar vai ter as tools intermediarias de operations)

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
        config={"thread_id": "1"},
        #"graph_state": graph
    )

    mensagens = resultado["messages"][-1].content

    if isinstance(mensagens, list) and len(mensagens) > 0 and "text" in mensagens[0]:
        resposta = mensagens[0]["text"]
    else:
        resposta = str(mensagens)

    print("ARCOS-RJ:", resposta)


import os
from typing import Any, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from dataclasses import dataclass

os.environ["GOOGLE_API_KEY"] = ""

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    summary: str

@tool("ler_arquivo_rag")
def ler_arquivo_rag(nome_do_arquivo: str) -> str:
    """
        Ferramenta utilizada para ler o conteúdo dos arquivos.


    """
    if not os.path.exists(RAG_DIR):
        return "erro: diretório não encontrada."
    
    arquivos = os.listdir(RAG_DIR)
    if not arquivos:
        return "info: nenhum arquivo encontrado na pasta RAG."

    return "\n".join(arquivos)
    
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

agent = create_agent(
    model=model,
    context_schema=Context,
    system_prompt="Você é o ARCOS - RJ...",
    tools = [ler_arquivo_rag]

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

    resposta = resultado["messages"][-1].content
    print("ARCOS-RJ:", resposta)

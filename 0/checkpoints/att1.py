import os
from typing import Any, TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware

os.environ["GOOGLE_API_KEY"] = ""
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature= 0.5)

#ARCOS é Acesso Rapido e Consultas: Observabilidade dos Serviços no Rio de Janeiro

class CustomState(AgentState):
    user_preferences: dict

class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    #tools = [tool1, tool2]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        prefs = state.get("user_preferences", {})
        if prefs:
            print(f"[Middleware] Preferências do usuário: {prefs}")
        return None
    
@tool
def modo_RAG(query: str) -> str: # https://docs.langchain.com/oss/python/langchain/tools
    """
    Busca informações em documentos para geração de respostas no diretório C:\\Users\\Master\\ambiente\\RAG
    
    Args:
        query: Pergunta ou texto para busca semântica.
       
    """
    
    # https://docs.langchain.com/oss/python/integrations/text_embedding 

    
agent = create_agent(
    model,
    tools=modo_RAG
    middleware=[CustomMiddleware()],
    system_prompt="Você é o ARCOS - RJ: agente especialista em informações do Portal de Dados Abertos do Rio de Janeiro. Sua missão é trazer informações relevantes, contextualizadas e rápidas sobre os dados presentes no Portal de Dados Abertos."
)

state = CustomState(messages=[], user_preferences={"style": "technical", "verbosity": "detailed"}) # https://docs.langchain.com/oss/python/langchain/agents#memory

print("Bem vindo ao ARCOS-RJ! Digite '/sair' para encerrar.\n")
while True:
    pergunta = input("Input: ").strip()

    if pergunta.lower() == "/sair":
        print("ARCOS-RJ: Até logo!")
        break

    state["messages"].append({"role": "user", "content": pergunta})
    state = agent.invoke(state)

    ### 

    ultima_msg = state["messages"][-1] ### Corrige o acesso ao conteúdo da última mensagem do agente
    if hasattr(ultima_msg, "content"):
        resposta = ultima_msg.content
    else:
        resposta = ultima_msg["content"] 

    ###
    
    print("ARCOS-RJ:", resposta)


    #resultado = agent.invoke({
    #    "messages": [{"role": "user", "content": pergunta}]
    #})

    #print("ARCOS-RJ:", resultado)


# Adicionar memória (ver LangChain classes de memoria)
# ADd tools (3):  1. interpretar o dicionario 2. gerar stats (media, max, min, etc) que virarao parametro 
# https://docs.langchain.com/oss/python/langchain/overview
# https://docs.langchain.com/oss/python/langchain/tools
# https://dadosabertos.rj.gov.br/dataset/setram_sbe
# TRANBE Consolidado Dicionário
# TransaçõesconsolidadoBE_2025_01.csv


# https://docs.langchain.com/oss/python/integrations/tools/bearly

# https://dadosabertos.rj.gov.br/ne/dataset/setram_sbe

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
    
agent = create_agent(
    model,
    middleware=[CustomMiddleware()],
    system_prompt="Você é o ARCOS - RJ: agente especialista em informações do Portal de Dados Abertos do Rio de Janeiro. Sua missão é trazer informações relevantes, contextualizadas e rápidas sobre os dados presentes no Portal de Dados Abertos."
)

state = CustomState(messages=[], user_preferences={"style": "technical", "verbosity": "detailed"}) # https://docs.langchain.com/oss/python/langchain/agents#memory

print("Bem vindo ao ARCOS-RJ! Digite '/sair' para encerrar.\n")
while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "/sair":
        print("ARCOS-RJ: Até logo!")
        break

    state["messages"].append({"role": "user", "content": pergunta})
    state = agent.invoke(state)

    ultima_msg = state["messages"][-1] 
    if hasattr(ultima_msg, "content"):
        resposta = ultima_msg.content
    else:
        resposta = ultima_msg["content"] 

    print("ARCOS-RJ:", resposta)

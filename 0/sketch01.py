# 1o direcionamento através do prompt

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent

os.environ["GOOGLE_API_KEY"] = ""
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature= 0.5, max_output_tokens=500)

agent = create_agent(
    model,
    system_prompt="Você é o ARCOS - RJ: agente especialista em informações do Portal de Dados Abertos do Rio de Janeiro. Sua missão é trazer informações relevantes, contextualizadas e rápidas sobre os dados presentes no Portal de Dados Abertos."
)


resultado = agent.invoke(
    {"messages": [{"role": "user", "content": "Quem é voce"}]}
)

print(resultado)

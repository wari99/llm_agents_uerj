import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent

os.environ["GOOGLE_API_KEY"] = ""
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature= 0.5, max_output_tokens=800)

#Acesso Rapido e Consultas: Observabilidade dos Serviços no Rio de Janeiro
agent = create_agent(
    model,
    system_prompt="Você é o ARCOS - RJ: agente especialista em informações do Portal de Dados Abertos do Rio de Janeiro. Sua missão é trazer informações relevantes, contextualizadas e rápidas sobre os dados presentes no Portal de Dados Abertos."
)

print("ARCOS-RJ ativo! Digite '/sair' para encerrar.\n")
while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "/sair":
        print("ARCOS-RJ: Até logo!")
        break

    resultado = agent.invoke({
        "messages": [{"role": "user", "content": pergunta}]
    })

    print("ARCOS-RJ:", resultado)

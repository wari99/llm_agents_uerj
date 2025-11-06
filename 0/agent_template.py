import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

os.environ["GOOGLE_API_KEY"] = ""

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
resultado = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in rio de janeiro"}]}
)

print(resultado)

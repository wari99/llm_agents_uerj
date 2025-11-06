import os
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict

os.environ["GOOGLE_API_KEY"] = ""
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class State(TypedDict, total=False):
    user_input: str
    response: str

def get_user_input(state: State):
    user_input = input("Input: ")
    return {"user_input": user_input}

def call_llm(state: State):
    result = model.invoke(state["user_input"])
    response = result.content
    print(f"LLM: {response}")
    return {"response": response}

graph = StateGraph(State)

graph.add_node("input", get_user_input)
graph.add_node("llm_call", call_llm)

graph.set_entry_point("input")

graph.add_edge("input", "llm_call")
graph.add_edge("llm_call", "input")

workflow = graph.compile()

state = {}
while True:
    user_input = input("Input: ")
    
    if user_input.strip().lower() == "/sair":
        break

    state["user_input"] = user_input
    
    result = model.invoke(user_input)
    print(result.content)

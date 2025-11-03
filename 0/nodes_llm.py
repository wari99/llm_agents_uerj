import os
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
 
os.environ["GOOGLE_API_KEY"] = " "
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
 
class State(TypedDict, total=False):
    user_input: str
    response: str
 
def get_user_input(state: State): 
  """
    Node 1: user input
  """
    user_input = input("Input: ")
   
    if user_input.strip().lower() == "/sair":
        return END
    return {"user_input": user_input}
 
def call_llm(state: State):
  """
    Node 2: LLM call
  """
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
workflow.invoke({})

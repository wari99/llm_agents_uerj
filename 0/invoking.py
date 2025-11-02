import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyDifMetEsN05Zw9sC4PhSV3tflKAczBqo4"

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

print(model.invoke("Quais são as receitas mais famosas na America do Sul?"))

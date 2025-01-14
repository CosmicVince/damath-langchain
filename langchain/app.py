from langchain_ollama.llms import OllamaLLM

llm = OllamaLLM(model="llama3.2")

response = llm.invoke("Can you tell me a dark humor joke?")

print(response)

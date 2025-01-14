from flask import Flask


from langchain_ollama.llms import OllamaLLM

app = Flask(__name__)


llm = OllamaLLM(model="llama3.2")


response = llm.invoke("Can you tell me a dark humor joke?")

print(response)


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()
# Damath Langchain 

### 1. [Install](https://github.com/ollama/ollama?tab=readme-ov-file#macos) ollama and pull models

Pull the LLM you'd like to use:

```shell
ollama pull llama3.2
```

### 2. Create a virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install libraries

```shell
pip install -r requirements.txt
```

### 4. Set .env 

```shell
cp env-example .env
```
and add details configuration.

### 5. Run Flask RAG App

```shell
flask run
```

<!-- 
  steps to run:
start pgvector docker: sudo docker start pgvector
next: flask run before postman initialize
next: intialize postman
next: start kubi -->
  

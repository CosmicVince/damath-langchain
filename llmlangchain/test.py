from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

embeddings = OllamaEmbeddings(model="all-minilm:33m")

connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_name = "langchain_documents"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

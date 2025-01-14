from langchain_ollama.llms import OllamaLLM

class LLMManager:
    def __init__(self):
        self.llm = None

    def initialize_llm(self, model_name: str = "llama3.2") -> bool:
        """
        Initialize the LLM with specified model
        """
        try:
            self.llm = OllamaLLM(model=model_name)
            return True
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            return False

    def get_response(self, prompt: str) -> str:
        """
        Get a response from the LLM model
        """
        if self.llm is None:
            raise ValueError("LLM not initialized")
        return self.llm.invoke(prompt)

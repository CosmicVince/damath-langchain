from langchain_ollama.llms import OllamaLLM
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


class LLMManager:
    def __init__(self):
        self.llm = None

    def initialize_llm(self, model_name: str = "llama3.2") -> bool:
        """
        Initialize the LLM with specified model
        """
        try:
            self.llm = ChatOllama(model=model_name, temperature=0)
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

    def board_to_valid(self, board_state: str) -> str:
        """
        Diri ang same sa get response pero ang prompt is ang boardstate
        """
        if self.llm is None:
            raise ValueError("LLM not initialized")


        prompt = ChatPromptTemplate.from_template("""
        You are an expert at the board game "Damath". 
        """)

        # Define the chain
        # chain = prompt | self.llm | StrOutputParser()
        # StrOutputParser() kay para ang output dili na AIMessage, same cya as result.content
        chain = prompt | self.llm

        
        rules = """
        rules
        """


        format = """
        a
        """

        # Generate the result
        result = chain.invoke({"rules": rules, "board_state": board_state, "format": format})
        print(result)
        return result
        

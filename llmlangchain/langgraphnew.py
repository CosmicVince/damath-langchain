import random

from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain.tools import tool
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.graph import END, StateGraph, START
from typing import TypedDict, Dict, Any

# Define a tool that converts its input to all uppercase.
@tool
def to_uppercase(text: str) -> str:
    """Convert the provided text to uppercase."""
    return text.upper()

# Define a tool that generates a random number.
@tool
def generate_random_number() -> int:
    """Generate a random integer between 1 and 100."""
    return random.randint(1, 100)

tools = [to_uppercase, generate_random_number]

# Initialize the Ollama chat model using Llama3.2.
ollama_llm = ChatOllama(model="llama3.2")

# Create a chat prompt template for our agent.
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant that can call functions when needed. "
    "If the user input requires you to transform text to uppercase, call the 'to_uppercase' tool. "
    "If the user input asks for a random number, call the 'generate_random_number' tool. "

    "Here's the user's input:"
    "{input}"

    
    "{agent_scratchpad}"
)

# Create the tool-calling agent with the defined tools.
agent = create_tool_calling_agent(
    llm=ollama_llm,
    tools=tools,
    prompt=prompt
)

# Wrap the agent in a ToolNode so it can be used within a langgraph StateGraph.
agent_node = ToolNode(tools)


class AgentState(TypedDict):
    input: str
    output: Dict[str, Any]

graph = StateGraph(AgentState)  # Define the state schema
graph.add_node("agent", agent_node)  # Add the agent node
graph.add_edge(START, "agent")  # Connect START to agent
graph.add_edge("agent", END)  # Connect the agent to END
graph = graph.compile() 
# Example usage of the graph.
if __name__ == "__main__":
    user_input = "Please convert 'hello world' to uppercase and then give me a random number."
    result = graph.invoke({"input": user_input})  # Use `.invoke()`
    print(result)

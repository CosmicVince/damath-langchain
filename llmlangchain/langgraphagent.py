from langchain_ollama.llms import OllamaLLM
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents import create_tool_calling_agent
from langchain_core.messages import BaseMessage

from langchain.tools import BaseTool, StructuredTool, Tool, tool

import operator


class AgentState(TypedDict):
    # The input string
    # input: str
    system_prompt: str
    user_prompt: str
    # The list of previous messages in the conversation
    chat_history: list[BaseMessage]
    # The outcome of a given call to the agent
    # Needs `None` as a valid type, since this is what this will start as
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # List of actions and corresponding observations
    # Here we annotate this with `operator.add` to indicate that operations to
    # this state should be ADDED to the existing values (not overwrite it)
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


import random

@tool("lower_case", return_direct=True)
def to_lower_case(input:str) -> str:
  """Returns the input as all lower case."""
  return input.lower()

@tool("random_number", return_direct=True)
def random_number_maker(input:str) -> str:
    """Returns a random number between 0-100."""
    return random.randint(0, 100)

tools = [to_lower_case,random_number_maker]
# print(random_number_maker.invoke('random'))

# print(to_lower_case.run('GOSHION'))



# Define the prompt template
template = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{user_prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{agent_scratchpad}
"""

# Create a ChatPromptTemplate
prompt = ChatPromptTemplate.from_template(template)


# Choose the LLM that will drive the agent
llm = ChatOllama(model="llama3.2", temperature=0, streaming=True)

agent_runnable = create_tool_calling_agent(
                llm = llm,
                tools=tools,
                prompt=prompt
            )
# print(prompt)
# print(prompt.get_prompts())

# inputs = {
#     "system_prompt": "You are a helpful assistant.",
#     "user_prompt": "give me a random number and then write in words and make it lower case.",
#     "agent_scratchpad": "",  # initially empty
#     "chat_history": [],
#     "intermediate_steps": []
# }


# agent_outcome = agent_runnable.invoke(inputs)
# print("\n\n")
# print(agent_outcome)
# print(type(agent_outcome))


from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_node import ToolNode

tool_executor = ToolNode(tools)

# Define the agent/graph
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}

def execute_tools(data):
    # Execute the tool based on the agent outcome.
    agent_action = data['agent_outcome']
    output = tool_executor.invoke(agent_action)
    print(f"The agent action is {agent_action}")
    print(f"The tool result is: {output}")
    
    # Update intermediate_steps by appending the new step.
    data["intermediate_steps"] = data.get("intermediate_steps", []) + [(agent_action, str(output))]
    
    return data

# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data['agent_outcome'], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
    else:
        return "continue"
    


    
from langgraph.graph import END, StateGraph

# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END
    }
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge('action', 'agent')

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()


print(workflow.channels)

inputs = {
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "give me a random number and then write in words and make it lower case.",
    "agent_scratchpad": "",  # initially empty
    "chat_history": [],
    "intermediate_steps": []
}

print("app result")
res = app.invoke(inputs)
print(res)
# for s in app.stream(inputs):
#     print(list(s.values())[0])
#     print("----")





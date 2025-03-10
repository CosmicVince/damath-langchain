from langchain_ollama.llms import OllamaLLM
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from langchain import hub
from langchain_core.tools import Tool
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents import initialize_agent, create_react_agent
from langchain.agents import AgentType


@tool
def get_current_time(input: str) -> str:  # Must accept input parameter
    """Returns current time in H:MM AM/PM format."""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

@tool
def get_red_valid_moves(board: str) -> dict:
    """
    Use this function to return valid moves of red piece in a board list.

    Args:
        board (list): list representation of the board

    Returns:
        str: JSON string valid moves of the board
    """

    valid_moves = {}
    def is_valid_index(idx):
        return 0 <= idx < 64

    def get_dama_moves(index, direction):
        moves = []
        current = index
        while True:
            if direction == "left_up":
                current -= 9
            elif direction == "right_up":
                current -= 7
            elif direction == "left_down":
                current += 7
            elif direction == "right_down":
                current += 9

            if not is_valid_index(current):
                break

            if board[current][0] is None:
                moves.append(current)
            else:
                break
        return tuple(moves)

    def get_dama_captures(index, direction):
        moves = []
        current = index
        while True:
            if direction == "left_up":
                next_idx = current - 9
            elif direction == "right_up":
                next_idx = current - 7
            elif direction == "left_down":
                next_idx = current + 7
            elif direction == "right_down":
                next_idx = current + 9

            if not is_valid_index(next_idx):
                break

            # If we find an enemy piece
            if (isinstance(board[next_idx][0], dict) and
                board[next_idx][0]['color'] == "b"):

                # Check next space after enemy
                capture_idx = next_idx + (next_idx - current)
                if is_valid_index(capture_idx) and board[capture_idx][0] is None:
                    moves.append(capture_idx)
                break
            elif board[next_idx][0] is not None:
                break

            current = next_idx
        return tuple(moves)

    for index, space in enumerate(board):
        if isinstance(space[0], dict) and space[0]['color'] == "r":
            piece = space[0]
            moves = []

            # Handle dama pieces
            if piece['is_dama']:
                # Normal moves in all directions
                moves.extend([
                    get_dama_moves(index, "left_up"),
                    get_dama_moves(index, "right_up"),
                    get_dama_moves(index, "left_down"),
                    get_dama_moves(index, "right_down")
                ])

                # Capture moves in all directions
                captures = [
                    get_dama_captures(index, "left_up"),
                    get_dama_captures(index, "right_up"),
                    get_dama_captures(index, "left_down"),
                    get_dama_captures(index, "right_down")
                ]
                moves.extend(captures)

            else:
                # Regular piece moves
                left_move = index + 7
                right_move = index + 9
                normal_moves = []

                # Check normal moves
                if is_valid_index(left_move) and board[left_move][0] is None:
                    normal_moves.append(left_move)
                if is_valid_index(right_move) and board[right_move][0] is None:
                    normal_moves.append(right_move)
                moves.append(tuple(normal_moves))

                # Check captures
                capture_moves = []
                for move in [(7, 14), (9, 18)]:
                    jump = index + move[0]
                    landing = index + move[1]
                    if (is_valid_index(jump) and is_valid_index(landing) and
                        isinstance(board[jump][0], dict) and
                        board[jump][0]['color'] == "b" and
                        board[landing][0] is None):
                        capture_moves.append(landing)
                if capture_moves:
                    moves.append(tuple(capture_moves))

            # Filter out empty tuples and store moves
            moves = [m for m in moves if m]
            if moves:
                valid_moves[index] = moves

    return valid_moves

# current_time_tool = Tool(
#     name="current_time",
#     func=lambda _: current_time.invoke({}),  # Ensure invoke is used
#     description="Returns the current time in H:MM AM/PM format.",
# )


# tools = [
#     Tool(
#         name="Time",
#         func=get_current_time,
#         description="Useful for when you need to know the current time",
#     ),
# ]


class LLMManager:
    def __init__(self):
        self.llama = None
        self.deepseek = None
        self.agent = None

    def initialize_llm(self, model_name: str = "llama3.1") -> bool:
        """
        Initialize the LLM with specified model
        """
        try:

            # prompt = hub.pull("hwchase17/react")
            self.llama = ChatOllama(model=model_name, temperature=0, max_tokens=4096)

            

            self.agent = initialize_agent(
                tools=[get_current_time, get_red_valid_moves],  # Use tools here
                llm=self.llama,               # Make sure to use the LLM model
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True,
                allowed_tools=["get_current_time", "get_red_valid_moves"],
            )

            # self.agent = create_react_agent(
            #     llm = self.llama,
            #     tools=tools,
            #     prompt=prompt,
            #     stop_sequence=True,
            # )

            # self.agent = AgentExecutor.from_agent_and_tools(agent=self.agent, tools=tools, handle_parsing_errors=True, verbose=True)
            response = self.agent.invoke({
                "input": "What's the current time? Use ONLY the provided tools and return ONLY the time as your final answer. Do NOT attempt any formatting."
            })

            # response = self.agent.invoke({"input": "What's the current time? Use the tool and return ONLY the time as your final answer."})
            # response = self.agent.invoke({"input":"What is the time?"})
            print("Agent Response:", response)
            print("Hi")
            print("Current Time:", response.get('output'))
            # print("Output Tokens:", response['usage']['output_tokens'])


            return True
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            return False

    def get_response(self, prompt: str) -> str:
        """
        Get a response from the LLM model
        """
        if self.llama is None:
            raise ValueError("LLM not initialized")
        # return self.llm.invoke(prompt)
        x = "[[None, '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X', [None, '*'], 'X', [{'color': 'r','value': -11, 'is_dama': False}, '+'], 'X', [{'color': 'r', 'value': 0, 'is_dama': False}, '-'], [None, '-'], 'X', [None, '+'], 'X',[{'color': 'r', 'value': 6, 'is_dama': True}, '*'], 'X', [{'color': 'r', 'value': -9, 'is_dama': False}, '/'], 'X', 'X', [None, '+'],'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [{'color': 'b', 'value': 0, 'is_dama': True}, '*'], 'X', [None, '/'], 'X',[None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X', [None, '*'], 'X', [None, '+'], 'X', [None, '-'], [{'color': 'r', 'value':-5, 'is_dama': True}, '-'], 'X', [None, '+'], 'X', [None, '*'], 'X', [None, '/'], 'X', 'X', [None, '+'], 'X', [None, '-'], 'X', [None,'/'], 'X', [None, '*']]"
        return self.agent.invoke({"input": prompt+x})

    def board_to_valid(self, board_state: str) -> str:
        """
        Diri ang same sa get response pero ang prompt is ang boardstate
        """
        x = "[[None, '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X', [None, '*'], 'X', [{'color': 'r','value': -11, 'is_dama': False}, '+'], 'X', [{'color': 'r', 'value': 0, 'is_dama': False}, '-'], [None, '-'], 'X', [None, '+'], 'X',[{'color': 'r', 'value': 6, 'is_dama': True}, '*'], 'X', [{'color': 'r', 'value': -9, 'is_dama': False}, '/'], 'X', 'X', [None, '+'],'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [{'color': 'b', 'value': 0, 'is_dama': True}, '*'], 'X', [None, '/'], 'X',[None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X', [None, '*'], 'X', [None, '+'], 'X', [None, '-'], [{'color': 'r', 'value':-5, 'is_dama': True}, '-'], 'X', [None, '+'], 'X', [None, '*'], 'X', [None, '/'], 'X', 'X', [None, '+'], 'X', [None, '-'], 'X', [None,'/'], 'X', [None, '*']]"
        board_state = x
        if self.llama is None:
            raise ValueError("LLM not initialized")


        prompt = ChatPromptTemplate.from_template("""
        You are a game-playing agent for the board game "Damath".
        You will be given a board state in a list format.
             
        Here is the board state: {board_state}
        
        With the given board state, run the tool get_red_valid_moves.
                                                  
        provide the result of running the tool ONLY.
        """)

        # Define the chain
        # chain = prompt | self.llm | StrOutputParser()
        # StrOutputParser() kay para ang output dili na AIMessage, same cya as result.content
        chain = prompt | self.llama

        
        # instructions = """
        # 1. Check for all red pieces only.
        # 2. Determine a red piece's position by getting its index value from the list.
        # 3. A red piece's movement is determined by adding 7 to move down-left, and adding 9 to move down-right.
        # 4. Before adding it as a valid move, check first if the new index/position does not have 'X' on it.
        # 5. If it does not have an 'X', then it has a list on it. Check if the position is valid by looking at the
        #     first element of the nested list. If it has a None value, that move is valid. If it has a Piece object,
        #     the move is invalid.
        # """




        # Generate the result
        result = chain.invoke({"board_state": board_state})
        # result = chain.invoke({"instructions": instructions, "board_state": board_state})
        print(result)
        return result
        

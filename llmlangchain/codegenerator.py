import re, time, random
start = time.time()

class Piece:
    def __init__(self, color, value, is_dama=False):
        # self.row = row
        # self.col = column
        self.value = value
        self.index = None
        self.color = color
        self.is_dama = is_dama
        self.name = f"{color}, {value}"

    def __repr__(self):
        return f"Piece({self.name}, is_dama={self.is_dama})"

    def __eq__(self, other):
        return isinstance(other, Piece) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

board_state = """[
    [Piece('r', 2, is_dama=False), '*'], 'X', [Piece('r', -5, is_dama=False), '/'], 'X',
    [Piece('r', 8, is_dama=False), '-'], 'X', [Piece('r', -11, is_dama=False), '+'], 'X',
    'X', [Piece('r', -7, is_dama=False), '/'], 'X', [Piece('r', 10, is_dama=False), '*'], 'X',
    [Piece('r', -3, is_dama=False), '+'], 'X', [Piece('r', 0, is_dama=False), '-'],
    [Piece('r', 4, is_dama=False), '-'], 'X', [Piece('r', -1, is_dama=False), '+'], 'X',
    [Piece('r', 6, is_dama=False), '*'], 'X', [Piece('r', -9, is_dama=False), '/'], 'X',
    'X', [None, '+'], 'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [None, '*'],
    'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X',
    [Piece('b', -9, is_dama=False), '/'], 'X', [Piece('b', 6, is_dama=False), '*'], 'X',
    [Piece('b', -1, is_dama=False), '+'], 'X', [Piece('b', 4, is_dama=False), '-'],
    [Piece('b', 0, is_dama=False), '-'], 'X', [Piece('b', -3, is_dama=False), '+'], 'X',
    [Piece('b', 10, is_dama=False), '*'], 'X', [Piece('b', -7, is_dama=False), '/'], 'X',
    'X', [Piece('b', -11, is_dama=False), '+'], 'X', [Piece('b', 8, is_dama=False), '-'],
    'X', [Piece('b', -5, is_dama=False), '/'], 'X', [Piece('b', 2, is_dama=False), '*']
]"""


from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser




def runLLM(instruction):
    s = random.randint(0, 2**32 - 1)
    print("Seed used: ", s)
    llm = ChatOllama(
        model="llama3.2:3b-instruct-q8_0",
        streaming=True,
        temperature=0.5,
        num_ctx=4096,
        seed=s,
        # other params...
        # llama3.2:3b-instruct-q8_0
    )

    chain = llm # | StrOutputParser()
    res = ""
    res = chain.invoke(instruction)
    return res


def formatOutput(response, name):
    match = re.search(r"```(?:python)?\n(.*?)```", response, re.DOTALL)
    if match:
        python_code = match.group(1)
        
        # Save the extracted code to a file named "extracted_code.py"
        with open(f"{name}.py", "w") as file:
            file.write(python_code)
        
        print("Python code extracted and saved to 'extracted_code.py'.")
    else:
        print("No Python code block found in the provided output.")


### Normal Movement

instruction = f"""I have an initial board state (A 1-dimensional array indicated as a Python list). 
I want you to create a code that takes in a board state as an input with the function name 'func1'.

First, create a Piece class that has the attributes:
1. color: Indicates the piece's color (e.g., "r" for red, "b" for blue).
2. value: The numerical value assigned to that piece.
3. is_dama: A Boolean indicating whether the piece is promoted (dama/king) or not.
4. index: this has a default value of 0. This is the position of a piece on the board_state. This should be assigned during the func1 function call.
5. name: should be a string with the format 'name, value'
A piece’s position is determined by its index (0 to 63) in the board list (excluding unusable squares).

The piece should have these dunder methods:
__repr__: it should look like this Piece('r', 2, is_dama=False)
__eq__: it should return a boolean if another object is+ an instance of the Piece class, and their names should be equal
__hash__: the hash of its name


func1 should follow these logic:

1. The function should iterate on each element of the board state. Enumerate the board state so you can get the index and the element.
2. If the element is a string 'X', do nothing.
3. If the element is a List, check the first element of that list.
4. If the first element is None, do nothing. Else, if it is an instance of the Piece class, AND if the piece's color is 'r', assign an attribute 'index' to the Piece object its index (piece.index = index).
5. Then, call the func2 function, capture its returned key:value pair, and update the valid_moves dictionary with this data.
6. After func2 returns the key:value pair of valid moves, merge this pair into the valid_moves dictionary so that all pieces’ moves are recorded.
7. Return the dictionary of all valid moves.

Logic for func2:
1. The function takes in a Piece object.
2. With its index as its position on the board (source index), add 7 to perform a forward left movement, and add 9 to perform a forward right movement, each of these results is a destination index.
3. For each destination index, first check if the index is within the valid range of the board state by ensuring it is less than len(board_state). Then, access the destination square using board_state[destination_index]. If the index is out-of-range, consider the move invalid; otherwise, use it to check the board state.
4. If the destination square is a list, access its first element. If the first element is None, consider it a valid move; otherwise, if it is an instance of the Piece class,or if it is a string 'X', consider it an invalid move."
5. Return a key, value pair of the piece source index with a list of its valid moves ONLY.


Here is the board_state:

{board_state}


Include the board state in your code (Place it after the Piece class is created).
"""

# normalmove = runLLM(instruction)


### Dama Movement

instruction = f"""I have an initial board state (A 1-dimensional array indicated as a Python list). 
I want you to create a code that takes in a board state as an input with the function name 'func1'.

First, create a Piece class that has the attributes:
1. color: Indicates the piece's color (e.g., "r" for red, "b" for blue).
2. value: The numerical value assigned to that piece.
3. is_dama: A Boolean indicating whether the piece is promoted (dama/king) or not.
4. index: this has a default value of 0. This is the position of a piece on the board_state. This should be assigned during the func1 function call.
5. name: should be a string with the format 'name, value'
A piece’s position is determined by its index (0 to 63) in the board list (excluding unusable squares).

The piece should have these dunder methods:
__repr__: it should look like this Piece('r', 2, is_dama=False)
__eq__: it should return a boolean if another object is+ an instance of the Piece class, and their names should be equal
__hash__: the hash of its name


func1 should follow these logic:

1. The function should iterate on each element of the board state. Enumerate the board state so you can get the index (i) and the element.
2. If the element is a string 'X', do nothing.
3. If the element is a List, check the first element of that list.
4. If the first element is None, do nothing. 
5. Else, if it is an instance of the Piece class, if the piece's color is 'r', AND if the piece is a dama, do these following logic: First, assign the index value to the piece's 'index' attribute. Next, call the func2 function, capture its returned key:value pair. Then, update the valid_moves dictionary with this data.
6. After func2 returns the key:value pair of valid moves, merge this pair into the valid_moves dictionary so that all pieces’ moves are recorded.
7. After the function iterates on all element of the board state, return the dictionary of all valid moves.

Logic for func2:
1. The function also takes in a Piece object.
2. Instantiate a list called damamove with the values [7, 9, -9, -7] and a local empty list called moves.
3. Iterate each element on the damamove list. Call the element 'mv'.
4. For each mv in damamove, set dest_index to the piece’s index and initialize an empty list called holder.
5. Use a while True loop to keep adding the move offset (mv) to dest_index and, add a condition if the destination index is within range between 0 and the board_state length, and the destination square is empty (i.e. a list whose first element is None), append that destination index to holder. Stop when the square is occupied or out-of-bounds.
6. After the loop, convert holder into a tuple and append this tuple to moves (do not include the piece’s index in the tuple).
7. After processing all move directions, simply return the piece index and the list 'moves'.


Here is the board_state:

{board_state}


Include the board state in your code (Place it after the Piece class is created).
"""


# damamove = runLLM(instruction)


### Normal Capture

instruction = f"""I have an initial board state (A 1-dimensional array indicated as a Python list). 
I want you to create a code that takes in a board state as an input with the function name 'func5'.

First, create a Piece class that has the attributes:
1. color: Indicates the piece's color (e.g., "r" for red, "b" for blue).
2. value: The numerical value assigned to that piece.
3. is_dama: A Boolean indicating whether the piece is promoted (dama/king) or not.
4. index: this has a default value of 0. This is the position of a piece on the board_state. This should be assigned during the func5 function call.
5. name: should be a string with the format 'name, value'
A piece’s position is determined by its index (0 to 63) in the board list (excluding unusable squares).

The piece should have these dunder methods:
__repr__: it should look like this Piece('r', 2, is_dama=False)
__eq__: it should return a boolean if another object is+ an instance of the Piece class, and their names should be equal
__hash__: the hash of its name


func5 should follow these logic:

1. The function should iterate on each element of the board state. Enumerate the board state so you can get the index and the element.
2. If the element is a string 'X', do nothing.
3. If the element is a List, check the first element of that list.
4. If the first element is None, do nothing. Else, if it is an instance of the Piece class, AND if the piece's color is 'r', assign an attribute 'index' to the Piece object its index (piece.index = index).
5. Then, call the func6 function, capture its returned key:value pair, and update the valid_moves dictionary with this data.
6. After func6 returns the key:value pair of valid moves, merge this pair into the valid_moves dictionary so that all pieces’ moves are recorded.
7. Return the dictionary of all valid moves.

Logic for func6:
1. The function takes in a Piece object.
2. Instantiate an empty list called 'capmoves' and a list called 'dia' with the values of 7, 9, -7, -9. Additionally, set a variable named 'src_ind' to the index of the piece object.
3. Iterate all the elements inside dia using a variable 'd'. Inside the iteration, set a variable named 'temp_ind' to have the value of 'src_ind'.
4. Add temp_ind with the variable 'd' from the list dia. Assign it to a variable named 'capt_ind'.
5. Check if capt_ind is between 0 and the length of the board state. If it is not in between, continue. 
6. Then, check if board_state[capt_ind] is a list. If it is a list, use a nested if-statement to check if the first element is an instance of the Piece class, and if the piece's color is blue. If this is True, add capt_ind with the value of the variable 'd', and store it to a variable named 'dest_ind'.
7. Use the dest_ind as an index to the board state. Check if it is a list and the first element is None, append the dest_ind to the capmoves list.
8. Return a pair of piece.index and capmoves.


Here is the board_state:

{board_state}


Include the board state in your code (Place it after the Piece class is created).
"""


normalcap = runLLM(instruction)


### Dama Capture

instruction = f"""I have an initial board state (A 1-dimensional array indicated as a Python list). 
I want you to create a code that takes in a board state as an input with the function name 'func7'.

First, create a Piece class that has the attributes:
1. color: Indicates the piece's color (e.g., "r" for red, "b" for blue).
2. value: The numerical value assigned to that piece.
3. is_dama: A Boolean indicating whether the piece is promoted (dama/king) or not.
4. index: this has a default value of 0. This is the position of a piece on the board_state. This should be assigned during the func7 function call.
5. name: should be a string with the format 'name, value'
A piece’s position is determined by its index (0 to 63) in the board list (excluding unusable squares).

The piece should have these dunder methods:
__repr__: it should look like this Piece('r', 2, is_dama=False)
__eq__: it should return a boolean if another object is an instance of the Piece class, and their names should be equal
__hash__: the hash of its name


func7 should follow these logic:

1. The function should iterate on each element of the board state. Enumerate the board state so you can get the index (i) and the element.
2. If the element is a string 'X', do nothing.
3. If the element is a List, check the first element of that list.
4. If the first element is None, do nothing. 
5. Else, if it is an instance of the Piece class, if the piece's color is 'r', AND if the piece is a dama: set piece.index to the value of 'i', call the func8 function, capture its returned pair using key, value. Then, update the valid_moves dictionary using the data.
6. After func8 returns the key:value pair of valid moves, merge this pair into the valid_moves dictionary so that all pieces’ moves are recorded.
7. After the function iterates on all element of the board state, return the dictionary of all valid moves.

Logic for func8:
1. In func8, accept a Piece object and initialize an empty list named 'capmoves'.
2. Define a list 'dia' with values [7, 9, -7, -9] and set 'src_ind' to the piece’s index.
3. For each value d in dia, initialize 'capt_ind' with the value of src_ind added to d, and an empty list named holder.
4. While capt_ind is between 0 to the length of board_state AND if the board_state with an index of capt_ind is an instance to a list, create an if, elif, else blocks stated on steps 5, 6, 8, respectively.
5. If the first element of the board_state[capt_ind] is None, increment capt_ind with the value of d, then continue.
6. Else, if the first element of the board_state[capt_ind] has an attribute 'color' with the value of a string 'b', set dest_ind with the value of capt_ind added by d.
Inside this elif block, create a while loop with the conditions: dest_ind is between 0 and len(board_state), board_state[dest_ind] is an instance of a list, the first element of the board_state[dest_ind] is None, append dest_ind to the list holder, increment dest_ind with d. Outside the while block, break the outer loop.
7. Else, break out of the loop.
8. After breaking out of the while loop, append a tuple version of the holder list to the list 'capmoves'.
9. After all iterations of the for-loop, return exactly piece.index, capmoves.


Here is the board_state:

{board_state}


Include the board state in your code (Place it after the Piece class is created).
"""


# damacap = runLLM(instruction)


# normalmove = normalmove.content

# damamove =damamove.content

normalcap = normalcap.content

# damacap = damacap.content



# formatOutput(normalmove, "normalmove")
# formatOutput(damamove, "damamove")
formatOutput(normalcap, "normalcap")
# formatOutput(damacap, "damacap")



end = time.time()

print("It took", end-start, "seconds to run.")
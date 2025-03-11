import json
import csv
import random
import os
import sys
# from format import json_format

ROWS, COLS = 8, 8

operations = [
    ["*", 0, "/", 0, "-", 0, "+", 0],
    [0, "/", 0, "*", 0, "+", 0, "-"],
    ["-", 0, "+", 0, "*", 0, "/", 0],
    [0, "+", 0, "-", 0, "/", 0, "*"],
    ["*", 0, "/", 0, "-", 0, "+", 0],
    [0, "/", 0, "*", 0, "+", 0, "-"],
    ["-", 0, "+", 0, "*", 0, "/", 0],
    [0, "+", 0, "-", 0, "/", 0, "*"],
]

values = [
    ["2", 0, "-5", 0, "8", 0, "-11", 0],
    [0, "-7", 0, "10", 0, "-3", 0, "0"],
    ["4", 0, "-1", 0, "6", 0, "-9", 0],
    [0, "+", 0, "-", 0, "/", 0, "*"],
    ["*", 0, "/", 0, "-", 0, "+", 0],
    [0, "-9", 0, "6", 0, "-1", 0, "4"],
    ["0", 0, "-3", 0, "10", 0, "-7", 0],
    [0, "-11", 0, "8", 0, "-5", 0, "2"],
]


class Board:
    def __init__(self):
        self.board = []
        self.initialize_board()

    def initialize_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # FIX: Changed (row + 1) to row to have the correct board setup
                if col % 2 == (row % 2):

                    # comment/uncomment along with if False to make board empty

                    if row < 3:
                        self.board[row].append(
                            (
                                Piece("r", int(values[row][col])),
                                row,
                                col,
                                operations[row][col],
                            )
                        )
                    elif row > 4:
                        self.board[row].append(
                            (
                                Piece("b", int(values[row][col])),
                                row,
                                col,
                                operations[row][col],
                            )
                        )

                    # temporary if, to make board empty
                    # if False:
                    #     pass

                    else:
                        # board[row].append((f"Free({row},{col})", operations[row][col]))
                        self.board[row].append((None, row, col, operations[row][col]))
                        # print (self.board[row])
                else:
                    self.board[row].append("X")
                    # print (self.board[row])

        holder = self.board
        self.board = []
        for row in holder:
            for item in row:
                if isinstance(item, tuple):
                    self.board.append([item[0], item[3]])
                else:
                    self.board.append("X")
        
        for index, item in enumerate(self.board):
            # print(index, item)
            element = item[0]
            if not isinstance(element, Piece):
                continue
            else:
                element.index = index

        print("Done Initializing")
        # print(len(self.board))
        # print(self.board)

    ### DO NOT DELETE
    # def to_json(self):
    #     json_board = []
    #     for position, item in enumerate(self.board):
    #         if isinstance(item, list):
    #             piece_data = {
    #                 "position": [position, item[1]],
    #                 "piece": None
    #             }
    #             if item[0] is not None:
    #                 piece = item[0]
    #                 color = 'red' if piece.color == 'r' else 'blue'
    #                 value = piece.value
    #                 piece_data["piece"] = [color, value, piece.is_dama]
    #             json_board.append(piece_data)
    #     print(json.dumps({"board": json_board}, indent=1))
    #     print("\n")
    #     return json.dumps({"board": json_board})

    def __repr__(self):
        return str(self.board)


class Piece:
    def __init__(self, color, value, is_dama=False):
        # self.row = row
        # self.col = column
        self.value = value
        self.index = None
        self.color = color
        self.is_dama = is_dama
        self.name = f"\'{color}\', {value}"
        self.capture_index = {}

    def __repr__(self):
        return f"Piece({self.name}, is_dama={self.is_dama})"

    def __eq__(self, other):
        return isinstance(other, Piece) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Game:
    def __init__(self):
        self.current_move = "r"
        self.board = Board()
        self.has_mandatory_capture = False
        self.has_mandatory_capture_check = False
        self.dama_mandatory_capture = False
        self.dama_mandatory_capture_check = False
        self.valid_moves = {}
        self.move_history = []
        self.scores = {"b": 0, "r": 0}
        self.game_over = False

        # Extra options, edit boolean value
        self.disable_write = True
        self.randomize_choices = False

        # Uncomment these lines if you want to see new valid moves (this is another game state)
        # self.board.board[13][0] = (Piece("r", 7))
        # self.board.board[13][0].index = 48
        # self.board.board[13][0].is_dama = True

        # self.board.board[48][0] = (Piece("r", 10))
        # self.board.board[48][0].index = 13
        # self.board.board[41][0] = (Piece("r", 0))
        # self.board.board[41][0].index = 41

        # self.board.board[25][0] = (Piece("b", -5))
        # self.board.board[25][0].index = 25

        # self.board.board[36][0] = (Piece("r", 23))
        # self.board.board[36][0].index = 36

        # self.board.board[47][0] = (Piece("r", 11))
        # self.board.board[47][0].index = 47

        # self.board.board[18][0] = (Piece("r", -21))
        # self.board.board[18][0].index = 18

        # self.board.board[54][0] = (Piece("b", 6))
        # self.board.board[54][0].index = 54
        # self.board.board[54][0].is_dama = False

        # self.board.board[63][0] = (Piece("b", 5))
        # self.board.board[63][0].index = 63

        # USE THIS
        x = """[
        [None, '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X',
        [None, '/'], 'X', [None, '*'], 'X', [Piece('r', -11, is_dama=False), '+'], 'X',
        [Piece('r', 0, is_dama=False), '-'], [None, '-'], 'X', [None, '+'], 'X', 
        [Piece('r', 6, is_dama=True), '*'], 'X', [Piece('r', -9, is_dama=False), '/'], 'X', 'X',
        [None, '+'], 'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [Piece('b', 0, is_dama=True), '*'], 'X',
        [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X',
        [None, '*'], 'X', [None, '+'], 'X', [None, '-'], [Piece('r', -5, is_dama=True), '-'], 'X',
        [None, '+'], 'X', [None, '*'], 'X', [None, '/'], 'X', 'X', [None, '+'], 'X',
        [None, '-'], 'X', [None, '/'], 'X', [None, '*']
        ]"""
      
        self.board.board = eval(f"{x}")
        for index, item in enumerate(self.board.board):
            # print(index, item)
            element = item[0]
            if not isinstance(element, Piece):
                continue
            else:
                element.index = index

        a = list(self.board.board)
        for index, i in enumerate(a):
            if isinstance(i[0], Piece):
                temp = i[0].value
                # if len(temp) == 1:
                #     temp = "0" + temp

                if i[0].color == "r":
                    a[index] = f"{temp}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"
                else:
                    a[index] = f"{temp}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"

            elif i == "X":
                pass
            elif i[0] == None:
                a[index] = "___"
        for i in range(0, len(a), 8):
                    print(a[i : i + 8])

        for index, x in enumerate(self.board.board):
            print(index, x)
        self.gameloop()

    def write_to_file(self):
        if self.disable_write:
            return
        # First, store all valid moves in a list
        filtered_moves = {k: v for k, v in self.valid_moves.items() if v and any(v)}
        self.valid_moves = filtered_moves

        with open("decision.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["instruction", "input", "output"])

            for key, value in self.valid_moves.items():
                # Flatten tuple values into a list of individual moves
                moves = []
                for val in value:
                    if isinstance(val, tuple):
                        moves.extend(val)
                    else:
                        moves.append(val)

                for val in moves:
                    # Check if this is a capture move by checking if val exists in capture_index
                    is_capture = val in key.capture_index

                    # Create combined game state
                    game_state = {
                        "board": json.loads(self.board.to_json())["board"],
                        "valid_moves": json.loads(self.valid_moves_to_json())["valid_moves"]
                    }

                    if is_capture:
                        try:
                            # Replace division operator with integer division
                            operator = self.board.board[val][1]
                            if operator == '/':
                                operator = '//'

                            # Calculate score using integer division
                            raw_score = eval(f"{key.value} {operator} {self.board.board[key.capture_index[val]][0].value}")

                            # For division, apply special rules
                            if self.board.board[val][1] == '/':
                                if abs(raw_score) < 1:
                                    score = 0
                                else:
                                    score = round(raw_score)
                            else:
                                score = int(raw_score)
                        except ZeroDivisionError:
                            score = 0

                        capture_data = {
                            "capture": {
                                "source": {
                                    "position": [key.index, self.board.board[key.index][1]],
                                    "piece": ["red", key.value, key.is_dama]
                                },
                                "middle": {
                                    "position": [key.capture_index[val], self.board.board[key.capture_index[val]][1]],
                                    "piece": ["blue",
                                            self.board.board[key.capture_index[val]][0].value,
                                            self.board.board[key.capture_index[val]][0].is_dama]
                                },
                                "destination": {
                                    "position": [val, self.board.board[val][1]],
                                    "piece": None
                                },
                                "score": score
                            }
                        }
                        decision = json.dumps(capture_data)
                    else:
                        move_data = {
                            "move": {
                                "source": {
                                    "position": [key.index, self.board.board[key.index][1]],
                                    "piece": ["red",
                                            key.value,
                                            key.is_dama]
                                },
                                "destination": {
                                    "position": [val, self.board.board[val][1]],
                                    "piece": None
                                }
                            }
                        }
                        decision = json.dumps(move_data)

                    # writer.writerow(["You are a Damath game-playing agent focusing on making strategic moves for the red player. Your analysis should always comply with Damath rules, prioritize capturing high-value blue pieces when possible, and aim to maximize the score for the red side.", json.dumps(game_state), decision])

                    writer.writerow(["Given a board state in JSON format, Provide a list of valid moves for each red piece on the board.", self.board.to_json(), self.valid_moves_to_json()])

                        # prompt = (
                        #     "given the valid moves of capture, get the best move in terms of score\n"
                        #     f"\n{self.valid_moves_to_json()}"
                        # )

                        # writer.writerow([prompt, decision])

                    # prompt = (
                    #     "Given a Board state, provide the best move or capture in terms of score\n"
                    #     f"\n{self.board.to_json()}\n"
                    # )

                    # writer.writerow([prompt, decision])

    def gameloop(self):
        while True:
            if self.game_over:
                print("Game Over!")
                break
            # Print JSON board state
            # print("\nCurrent Board State:")
            # print(self.board.to_json())
            self.valid_moves = {}
            self.has_mandatory_capture = False
            self.has_mandatory_capture_check = False
            self.dama_mandatory_capture_check = False
            self.dama_mandatory_capture = False
            if self.current_move == "b":
                self.check_all_valid("b")
                self.move("b")
            elif self.current_move == "r":
                self.check_all_valid("r")
                self.write_to_file()
                self.move("r")

    def check_all_valid(self, turn):

        for index, item in enumerate(self.board.board):
            # print(index, item)
            element = item[0]
            if not isinstance(element, Piece):
                continue
            elif element.color != turn:
                continue
            else:
                element.capture_index = {}
                element.index = index

                # if element.is_dama == False:
                self.valid_moves[element] = self.check_valid_moves(element)
                # print(element.capture_index)
                # else:
                #     self.valid_moves[element] = self.dama_valid_moves(element)

    def check_potential_capture(self, piece):

        if piece.color == "r":
            left_movement = piece.index + 7
            right_movement = piece.index + 9
            bleft_movement = piece.index - 9
            bright_movement = piece.index - 7
            lls = left_movement + 7
            rls = right_movement + 9
            blls = bleft_movement - 9
            brls = bright_movement - 7
        elif piece.color == "b":
            left_movement = piece.index - 9
            right_movement = piece.index - 7
            bleft_movement = piece.index + 7
            bright_movement = piece.index + 9
            lls = left_movement - 9
            rls = right_movement - 7    
            blls = bleft_movement + 7
            brls = bright_movement + 9

        # if piece.color == "r":
        #     left_movement = 7
        #     right_movement = 9
        #     bleft_movement = -9
        #     bright_movement = -7
        # elif piece.color == "b":
        #     left_movement = -9
        #     right_movement = -7
        #     bleft_movement = 7
        #     bright_movement = 9

        diagonals = [left_movement, right_movement, bleft_movement, bright_movement]
        landing_squares = [lls, rls, blls, brls]
        # all index values must stay inside the board
        for index, val in enumerate(diagonals):
            if val < 0:
                diagonals[index] = None
            elif val > 63:
                diagonals[index] = None
        for index, val in enumerate(landing_squares):
            if val < 0:
                diagonals[index] = None
            elif val > 63:
                diagonals[index] = None

        # self.current_move
        capture_moves = []
        for i, val in enumerate(diagonals):
            if val == None:
                continue
            diagonal_square = self.board.board[val]
            if (
                isinstance(diagonal_square[0], Piece)
                and diagonal_square[0].color != self.current_move
            ):
                # Capture is available, remove all normal movement moves

                # if the diagonal behind the enemy piece is empty, append index
                if self.board.board[landing_squares[i]][0] == None:

                    # Add to capture_index
                    piece.capture_index[landing_squares[i]] = diagonals[i]
                    capture_moves.append(landing_squares[i])
                    self.has_mandatory_capture = True

        return capture_moves

    def check_dama_moves(self, piece):

        # To check dama moves, check all adjacent diagonals. After that, increase
        # index values to check next diagonals on the same direction.

        # Continue until a diagonal with a piece in it appears. Stop on that direction.
        # Check for mandatory capture.
        # Continue on other directions until a piece appears.

        if piece.color == "r":
            dama_movement = {"left": 7, "right": 9, "bleft": -9, "bright": -7}
        elif piece.color == "b":
            dama_movement = {"left": -9, "right": -7, "bleft": 7, "bright": 9}

        dama_moves = []
        for direction in dama_movement.keys():
            starting_index = piece.index
            moves = []
            while True:

                starting_index += dama_movement[direction]
                if starting_index < 0 or starting_index > 63:
                    break
                if isinstance(self.board.board[starting_index][0], Piece):

                    if self.board.board[starting_index][0].color != self.current_move:

                        dama_capture_moves = self.dama_potential_capture(
                            piece, self.board.board[starting_index][0], direction
                        )

                        if dama_capture_moves != ():
                            piece.capture_index[dama_capture_moves] = starting_index
                            self.dama_mandatory_capture = True
                            if self.dama_mandatory_capture == True:
                                if self.dama_mandatory_capture_check == False:
                                    self.valid_moves = {}
                                    dama_moves = []
                                    self.dama_mandatory_capture_check = True
                            dama_moves.append(tuple(dama_capture_moves))

                        break
                    else:
                        break

                if self.dama_mandatory_capture == False and self.has_mandatory_capture == False:
                    if self.board.board[starting_index][0] == None:
                        moves.append(starting_index)

            if not self.dama_mandatory_capture:
                dama_moves.append(tuple(moves))
            else:
                pass

        return dama_moves
        # print(moves)

    def dama_potential_capture(self, piece, potential_capture_piece, direction):

        if piece.color == "r":
            dama_movement = {"left": 7, "right": 9, "bleft": -9, "bright": -7}
        elif piece.color == "b":
            dama_movement = {"left": -9, "right": -7, "bleft": 7, "bright": 9}

        capture_index = potential_capture_piece.index
        moves = []
        while True:

            capture_index += dama_movement[direction]
            if capture_index < 0 or capture_index > 63:
                break
            if isinstance(self.board.board[capture_index][0], Piece):
                # meaning theres a piece blocking, stopping from getting
                # more valid moves for capture landing squares

                break
            elif self.board.board[capture_index][0] == None:
                moves.append(capture_index)

        # if there are moves in potential capture, set potential capture piece
        # in capture index <<< ???

        return tuple(moves)

    def check_valid_moves(self, piece):

        # If the piece is a Dama piece, proceed to this method
        if piece.is_dama == True:
            moves = self.check_dama_moves(piece)
            return moves

        # if theres a dama mandatory capture, return [] for all normal piece
        if self.dama_mandatory_capture == True:
            return []

        # Movement for White (top to bottom)
        # +7 for left, +9 for right

        # Movement for Red (bottom to top)
        # -9 for left, -7 for right

        # Check for Potential Take
        capture_moves = self.check_potential_capture(piece)
        # print(capture_moves)

        # Check if has mandatory capture is true
        # if yes, delete all normal piece movement
        if self.has_mandatory_capture == True:
            if self.has_mandatory_capture_check == False:
                self.valid_moves = {}
                self.has_mandatory_capture_check = True

            if capture_moves != []:
                return capture_moves
            else:
                return []

        # Normal Piece movement first
        if piece.color == "r":
            left_movement = piece.index + 7
            right_movement = piece.index + 9
        elif piece.color == "b":
            left_movement = piece.index - 9
            right_movement = piece.index - 7

        valid_moves = []
        if left_movement < 0 or right_movement > 63:
            pass
        else:
            if isinstance(self.board.board[left_movement][0], Piece):
                pass
            elif self.board.board[left_movement][0] == None:
                valid_moves.append(left_movement)

            if isinstance(self.board.board[right_movement][0], Piece):
                pass
            elif self.board.board[right_movement][0] == None:
                valid_moves.append(right_movement)

        return valid_moves

    def valid_moves_to_json(self):
        key_indices = []
        valid_moves_json = {"valid_moves": []}

        for key, value in self.valid_moves.items():
                key_indices.append(key.index)

                move = {
                    "position": [key.index, self.board.board[key.index][1]],
                    "piece": ["blue" if key.color == "b" else "red", key.value, key.is_dama],
                    "destination": list(value) if isinstance(value, tuple) else value
                }
                valid_moves_json["valid_moves"].append(move)
        return json.dumps(valid_moves_json)



    def move(self, turn):

        if self.current_move == "b":
            turntext = "[Blue's Turn]"
        else:
            turntext = "[Red's Turn]"

        a = list(self.board.board)
        for index, i in enumerate(a):
            if isinstance(i[0], Piece):
                temp = str(index)
                if len(temp) == 1:
                    temp = "0" + temp

                if i[0].color == "r":
                    a[index] = f"{temp}{i[0].color}"
                else:
                    a[index] = f"{temp}{i[0].color}"

            elif i == "X":
                pass
            elif i[0] == None:
                a[index] = "___"

        for i in range(0, len(a), 8):
            print(a[i : i + 8])

        print(self.board.board)

        while True:
            print("\nScores:", self.scores)
            print("Move History:", self.move_history)
            eaten = False
            filtered_moves = {k: v for k, v in self.valid_moves.items() if v and any(v)}
            self.valid_moves = filtered_moves

            for key, value in self.valid_moves.items():
                pass

            print(self.valid_moves)
            if self.valid_moves == {}:
                print("valid moves:", self.valid_moves)
                print("\n\nThis is the initial score: ", self.scores, "and the last move is", self.current_move, "\n\n")
                for element in self.board.board:
                    # this is a space-operator pair, or an x
                    if element == "X":
                        continue
                    elif isinstance(element[0], Piece):
                        if element[0].is_dama == True:
                            self.scores[element[0].color] += element[0].value * 2
                        else:
                            self.scores[element[0].color] += element[0].value
                self.game_over = True
                a = list(self.board.board)
                for index, i in enumerate(a):
                    if isinstance(i[0], Piece):
                        temp = i[0].value
                        # if len(temp) == 1:
                        #     temp = "0" + temp

                        if i[0].color == "r":
                            a[index] = f"{temp}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"
                        else:
                            a[index] = f"{temp}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"

                    elif i == "X":
                        pass
                    elif i[0] == None:
                        a[index] = "___"

                for i in range(0, len(a), 8):
                    print(a[i : i + 8])
                print("\n\nThis is the final score: ", self.scores, "\n\n")
                break

            print("\nThese are the moves you can do:")
            key_indices = []
            for key, value in self.valid_moves.items():
                key_indices.append(key.index)
                print(f"[{key.index}] {key}: {value}")
            print(self.valid_moves)
            # print("\n", self.valid_moves_to_json())

            if self.randomize_choices:
                print(f"\n{turntext} Type the index of the piece (54, 12, etc.)):  ")
                piece_chosen = random.choice(key_indices)
                piece_chosen_index = int(piece_chosen)
                piece_chosen = self.board.board[int(piece_chosen)]
            else:
                piece_chosen = input(
                    f"\n{turntext} Type the index of the piece (54, 12, etc.)):  "
                )

                piece_chosen_index = int(piece_chosen)
                if piece_chosen_index not in key_indices:
                    print("Invalid piece. Please try again\n")
                    continue
                piece_chosen = self.board.board[int(piece_chosen)]

            # print(piece_chosen, isinstance(piece_chosen[0], Piece), self.current_move)

            print("\nWhere would you like to put it?")
            if self.randomize_choices:
                print(f"Valid Moves: {self.valid_moves[piece_chosen[0]]}\n>> ")
                container = self.valid_moves[piece_chosen[0]]
                # Flatten the container to only have integers
                flat_list = [item for sublist in container for item in (sublist if isinstance(sublist, tuple) else [sublist])]
                piece_destination = random.choice(flat_list)
            else:
                piece_destination = int(
                    input(f"Valid Moves: {self.valid_moves[piece_chosen[0]]}\n>> ")
                )

                appeared = False
                for item in self.valid_moves[piece_chosen[0]]:
                    if isinstance(item, tuple):
                        if piece_destination in item:
                            appeared = True
                    elif piece_destination == item:
                        appeared = True
                if not appeared:
                    print("Invalid move. Try again\n")
                    continue

            # print(self.board.board[piece_destination], "piece desti")

            # Performing the move
            # if :
            eaten = False
            score = 0
            if self.dama_mandatory_capture == True:
                for key in piece_chosen[0].capture_index:
                    if piece_destination in key:
                        index_of_captured_piece = piece_chosen[0].capture_index[key]
                        # Replace division operator with integer division
                        operator = self.board.board[piece_destination][1]
                        if operator == '/':
                            operator = '//'

                        try:
                            # Calculate raw score
                            raw_score = eval(f"{self.board.board[piece_chosen_index][0].value} {operator} {self.board.board[index_of_captured_piece][0].value}")

                            # Handle division specially
                            if self.board.board[piece_destination][1] == '/':
                                if abs(raw_score) < 1:  # If result would be less than 1
                                    score = 0
                                else:
                                    score = round(raw_score)
                            else:
                                score = int(raw_score)
                        except ZeroDivisionError:
                            score = 0

                        self.scores[self.current_move] += score
                        self.board.board[index_of_captured_piece][0] = None
                        eaten = True

            elif self.has_mandatory_capture == True:
                index_of_captured_piece = piece_chosen[0].capture_index[piece_destination]
                # Replace division operator with integer division
                operator = self.board.board[piece_destination][1]
                if operator == '/':
                    operator = '//'

                try:
                    # Calculate raw score
                    raw_score = eval(f"{self.board.board[piece_chosen_index][0].value} {operator} {self.board.board[index_of_captured_piece][0].value}")

                    # Handle division specially
                    if self.board.board[piece_destination][1] == '/':
                        if abs(raw_score) < 1:  # If result would be less than 1
                            score = 0
                        else:
                            score = round(raw_score)
                    else:
                        score = int(raw_score)
                except ZeroDivisionError:
                    score = 0

                self.scores[self.current_move] += score
                self.board.board[index_of_captured_piece][0] = None
                eaten = True

            self.board.board[piece_destination][0] = piece_chosen[0]
            self.board.board[piece_destination][0].index = piece_destination
            self.board.board[piece_chosen_index][0] = None

            # Move History
            # piece_chosen_index, index_of_captured_piece, piece_destination
            if eaten:
                self.move_history.append(
                    (
                        self.current_move,
                        (
                            piece_chosen_index,
                            index_of_captured_piece,
                            piece_destination,
                        ),
                        score,
                    )
                )
            else:
                self.move_history.append(
                    (self.current_move, (piece_chosen_index, piece_destination), score)
                )

            piece = self.board.board[piece_destination][0]

            if (
                piece.index in [0, 2, 4, 6]
                and piece.color == "b"
                or piece.index in [57, 59, 61, 63]
                and piece.color == "r"
            ):
                piece.is_dama = True

            # print(self.board.board)

            # check if theres a possibility of multiple capture
            if eaten:
                eaten = False
                a = list(self.board.board)
                for index, i in enumerate(a):
                    if isinstance(i[0], Piece):
                        temp = str(index)
                        if len(temp) == 1:
                            temp = "0" + temp

                        if i[0].color == "r":
                            a[index] = f"{temp}{i[0].color}"
                        else:
                            a[index] = f"{temp}{i[0].color}"

                    elif i == "X":
                        pass
                    elif i[0] == None:
                        a[index] = "___"

                self.valid_moves = {}
                self.has_mandatory_capture = False
                self.has_mandatory_capture_check = False
                self.dama_mandatory_capture_check = False
                self.dama_mandatory_capture = False

                piece.capture_index = {}

                self.valid_moves[piece] = self.check_valid_moves(piece)

                filtered_moves = {k: v for k, v in self.valid_moves.items() if v and any(v)}
                self.valid_moves = filtered_moves

                if not self.has_mandatory_capture and not self.dama_mandatory_capture:
                    self.valid_moves = {}
                    filtered_moves = {k: v for k, v in self.valid_moves.items() if v and any(v)}
                    self.valid_moves = filtered_moves
                # elif not self.dama_mandatory_capture:
                #     self.valid_moves = {}

                if self.valid_moves != {}:
                    if self.current_move == "r":
                        self.write_to_file()
                    # print("\n")
                    # for i in range(0, len(a), 8):
                    #     print(a[i : i + 8])
                    continue

            if self.current_move == "b":
                self.current_move = "r"
            else:
                self.current_move = "b"
            break







generate_dataset = False
rows = 10000

if not generate_dataset:
    game = Game()
elif generate_dataset:
    file_path = "gamehistory.csv"
    print("Starting dataset generation...")
    sys.stdout = open(os.devnull, 'w')

    for game_id in range(1, rows+1):
        # Check if the file exists and is non-empty
        file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0
        game = Game()
        red = game.scores["r"]
        blue = game.scores["b"]
        # game history
        # red_score
        # blue_score
        # win
        with open("gamehistory.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["game_id", "game_history", "red_score", "blue_score", "win"])
            writer.writerow([
                game_id,
                json_format(game.move_history),
                red,
                blue, 
                "red" if red >= blue else "blue"
            ])

    sys.stdout = sys.__stdout__
    print("Done executing")
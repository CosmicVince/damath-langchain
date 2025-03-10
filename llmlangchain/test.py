class Piece:
    def __init__(self, color, value, is_dama=0, index=0, name=""):
        self.color = color
        self.value = value
        self.is_dama = is_dama
        self.index = index
        self.name = f"{color}, {value}"

    def __repr__(self):
        return f"Piece('{self.color}', {self.value}, is_dama={self.is_dama})"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def func1(board_state):
    valid_moves = {}
    for i, element in enumerate(board_state):
        if element == 'X':
            continue
        elif isinstance(element, list):
            first_element = element[0]
            if first_element is None:
                continue
            elif isinstance(first_element, Piece) and first_element.color == 'r':
                piece = first_element
                piece.index = i
                key, value = func2(piece)
                valid_moves.update({key: value})
    print(valid_moves)


def func2(piece):
    if piece.is_dama:
        return func3(piece)
    else:
        moves = []
        for move in [piece.index + 7, piece.index + 9]:
            if move < len(board_state):
                square = board_state[move]
                if isinstance(square, list) and square[0] is None:
                    moves.append(move)
                elif isinstance(square, Piece) or square == 'X':
                    continue
        return (piece.index, moves)


def func3(piece):
    moves = []
    dia = [7, 9, -9, -7]

    for mv in dia:
        src = piece.index
        dest_index = src
        holder = []
        while True:
            dest_index = dest_index + mv
            print("piece index", src, dest_index)
            print(holder)
            if 0 <= dest_index < len(board_state):
                if isinstance(board_state[dest_index], list) and board_state[dest_index][0] == None:
                    print(isinstance(board_state[dest_index], list), board_state[dest_index][0] == None)
                    holder.append(dest_index)
                else:
                    break
            else:
                break


        moves.append(tuple(holder))
    return piece.index, moves


# Example usage
board_state = [
        [None, '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X',
        [None, '/'], 'X', [None, '*'], 'X', [Piece('r', -11, is_dama=False), '+'], 'X',
        [Piece('r', 0, is_dama=False), '-'], [None, '-'], 'X', [None, '+'], 'X', 
        [Piece('r', 6, is_dama=True), '*'], 'X', [Piece('r', -9, is_dama=False), '/'], 'X', 'X',
        [None, '+'], 'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [Piece('b', 0, is_dama=True), '*'], 'X',
        [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X',
        [None, '*'], 'X', [None, '+'], 'X', [None, '-'], [Piece('r', -5, is_dama=True), '-'], 'X',
        [None, '+'], 'X', [None, '*'], 'X', [None, '/'], 'X', 'X', [None, '+'], 'X',
        [None, '-'], 'X', [None, '/'], 'X', [None, '*']
        ]

func1(board_state)


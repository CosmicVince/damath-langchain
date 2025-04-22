class Piece:
    def __init__(self, color, value, is_dama=False, index=0):
        self.color = color
        self.value = value
        self.is_dama = is_dama
        self.index = index
        self.name = f"{color}, {value}"

    def __repr__(self):
        return f"Piece('{self.color}', {self.value}, {self.is_dama})"

    def __eq__(self, other):
        return isinstance(other, Piece) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


board_state = [
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
]

def func5(board_state):
    valid_moves = {}
    for i, element in enumerate(board_state):
        if isinstance(element, str) and element == 'X':
            continue
        elif isinstance(element, list):
            piece = element[0]
            if piece is None:
                continue
            if not isinstance(piece, Piece):
                continue
            if piece.color == 'r':
                piece.index = i
            key, value = func6(piece)
            valid_moves[key] = value
    return valid_moves


def func6(piece):
    capmoves = []
    dia = [7, 9, -7, -9]
    src_ind = piece.index
    for d in dia:
        temp_ind = src_ind + d
        if not (0 <= temp_ind < len(board_state)):
            continue
        if isinstance(board_state[temp_ind], list):
            nested_piece = board_state[temp_ind][0]
            if nested_piece is None or nested_piece.color != 'b':
                continue
            dest_ind = temp_ind + d
            if dest_ind < 0 or dest_ind >= len(board_state) or not isinstance(board_state[dest_ind], list) or board_state[dest_ind][0] is None:
                capmoves.append(dest_ind)
    return piece.index, capmoves


# Call func5 and print the result
print(func5(board_state))
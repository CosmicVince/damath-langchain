class Piece:
    def __init__(self, color, value, is_dama=0, index=0):
        self.color = color
        self.value = value
        self.is_dama = is_dama
        self.index = index
        self.name = f"{color}, {value}"

    def __repr__(self):
        return f"Piece('{self.color}', {self.value}, {self.is_dama})"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def func5(board_state):
    valid_moves = {}
    for i, element in enumerate(board_state):
        if element == 'X':
            continue
        elif isinstance(element, list):
            piece = element[0]
            if piece is None:
                continue
            if not isinstance(piece, Piece) or piece.color != 'r':
                continue
            piece.index = i
            key, value = func6(piece)
            valid_moves.update({key: value})
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
            if isinstance(board_state[dest_ind], list) and board_state[dest_ind][0] is None:
                capmoves.append(dest_ind)
    return piece.index, capmoves


# Example usage
board_state = [
        [Piece('r', -112, is_dama=False), '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X',
        [Piece('b', 0, is_dama=False), '/'], 'X', [None, '*'], 'X', [Piece('b', -11, is_dama=False), '+'], 'X',
        [None, '-'], [None, '-'], 'X', [None, '+'], 'X', 
        [None, '*'], 'X', [Piece('r', -9, is_dama=False), '/'], 'X', 'X',
        [None, '+'], 'X', [None, '-'], 'X', [None, '/'], 'X', [None, '*'], [Piece('b', 0, is_dama=False), '*'], 'X',
        [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X',
        [None, '*'], 'X', [None, '+'], 'X', [None, '-'], [Piece('r', -5, is_dama=False), '-'], 'X',
        [None, '+'], 'X', [None, '*'], 'X', [Piece('b', 6, is_dama=False), '/'], 'X', 'X', [None, '+'], 'X',
        [None, '-'], 'X', [None, '/'], 'X', [Piece('r', 6, is_dama=False), '*']
        ]

print(func5(board_state))
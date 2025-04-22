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


# Board state
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


def func1(board_state):
    valid_moves = {}
    for i, element in enumerate(board_state):
        if isinstance(element, str) and element == 'X':
            continue
        elif isinstance(element, list):
            piece = element[0]
            if piece is None:
                continue
            if piece.color == 'r' and piece.is_dama:
                piece.index = i
                key, value = func2(piece)
                valid_moves.update({key: value})
    return valid_moves


def func2(piece):
    damamove = [7, 9, -9, -7]
    moves = []
    for mv in damamove:
        dest_index = piece.index + mv
        holder = []
        while 0 <= dest_index < len(board_state) and board_state[dest_index][0] is None:
            holder.append(dest_index)
            dest_index += mv
        if holder:
            moves.append(tuple(holder))
    return piece.index, moves


def func1_test():
    print(func1(board_state))


if __name__ == "__main__":
    func1_test()

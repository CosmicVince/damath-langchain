class Piece:
    def __init__(self, color, value, is_dama=0, index=0):
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


def func7(board_state):
    valid_moves = {}
    for i, element in enumerate(board_state):
        if element == 'X':
            continue
        elif isinstance(element, list):
            first_element = element[0]
            if first_element is None:
                continue
            elif isinstance(first_element, Piece):
                if first_element.color == "r" and first_element.is_dama:
                    piece = first_element
                    piece.index = i
                    key, value = func8(piece)
                    valid_moves.update({key: value})
    return valid_moves


def func8(piece):
    capmoves = []
    dia = [7, 9, -7, -9]
    src_ind = piece.index

    for d in dia:
        holder = []
        capt_ind = src_ind + d
        # Continue along the direction d as long as the index is valid and cell is a list
        while 0 <= capt_ind < len(board_state) and isinstance(board_state[capt_ind], list):
            # If the square is empty, simply move to the next square in that direction
            if board_state[capt_ind][0] is None:
                capt_ind += d
                continue
            # If an opponent's piece ('b') is encountered, check for landing moves beyond it
            elif board_state[capt_ind][0].color == 'b':
                # For debugging: print(piece.index, ":", capt_ind)
                dest_ind = capt_ind + d
                # Continue while the destination square is within bounds, is a list,
                # and is empty so that it can be a landing spot after the capture.
                while (0 <= dest_ind < len(board_state) and 
                    isinstance(board_state[dest_ind], list) and 
                    board_state[dest_ind][0] is None):
                    # For debugging: print(dest_ind)
                    holder.append(dest_ind)
                    dest_ind += d
                # Once the capture sequence is done, break out of the while loop.
                break
            else:
                # If the square is occupied by a piece not matching our criteria, stop exploring this direction.
                break
        capmoves.append(tuple(holder))

    return piece.index, capmoves



# Example usage:
board_state = [
        [Piece('r', -112, is_dama=False), '*'], 'X', [None, '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X',
        [Piece('b', 0, is_dama=False), '/'], 'X', [None, '*'], 'X', [None, '+'], 'X',
        [None, '-'], [None, '-'], 'X', [None, '+'], 'X', 
        [None, '*'], 'X', [Piece('r', -9, is_dama=False), '/'], 'X', 'X',
        [None, '+'], 'X', [Piece('b', -11, is_dama=False), '-'], 'X', [None, '/'], 'X', [None, '*'], [Piece('b', 0, is_dama=False), '*'], 'X',
        [Piece('r', -5, is_dama=True), '/'], 'X', [None, '-'], 'X', [None, '+'], 'X', 'X', [None, '/'], 'X',
        [Piece('b', -5, is_dama=True), '*'], 'X', [None, '+'], 'X', [None, '-'], [None, '-'], 'X',
        [None, '+'], 'X', [None, '*'], 'X', [Piece('b', 6, is_dama=False), '/'], 'X', 'X', [None, '+'], 'X',
        [None, '-'], 'X', [None, '/'], 'X', [Piece('r', 6, is_dama=False), '*']
        ]

print(func7(board_state))
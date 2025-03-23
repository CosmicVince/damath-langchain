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


def func7(board_state):
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
                key, value = func8(piece)
                valid_moves.update({key: value})
    print(valid_moves)


def func8(piece):
    capmoves = []
    dia = [7, 9, -7, -9]
    src_ind = piece.index
    for d in dia:

        capt_ind = src_ind
        holder = []
        while True:
            capt_ind = capt_ind + d
            
            if 0 <= capt_ind < len(board_state) and isinstance(board_state[capt_ind], list): 
                if board_state[capt_ind][0] == None:
                    continue
            
                elif board_state[capt_ind][0].color == 'b':
                    dest_ind = capt_ind
                    print(piece.index, ":", dest_ind)
                    
                    while True:
                        dest_ind = dest_ind + d
                        print(dest_ind)
                        if 0 <= dest_ind < len(board_state) and isinstance(board_state[dest_ind], list): 
                            if board_state[dest_ind][0] == None:
                                holder.append(dest_ind)
                        else:
                            break
                
            else:
                capmoves.append(tuple(holder))
                break


    return piece.index, capmoves


# Example usage
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

a = list(board_state)
for index, i in enumerate(a):
    if isinstance(i[0], Piece):
        temp = i[0].value
        # if len(temp) == 1:
        #     temp = "0" + temp

        if i[0].color == "r":
            a[index] = f"{index}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"
        else:
            a[index] = f"{index}{i[0].color}{'t' if i[0].is_dama == True else 'f'}"

    elif i == "X":
        pass
    elif i[0] == None:
        a[index] = "___"
for i in range(0, len(a), 8):
    print(a[i : i + 8])

print(func7(board_state))
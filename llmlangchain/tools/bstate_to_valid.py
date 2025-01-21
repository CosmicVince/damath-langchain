

def boardstate_to_validmoves():


    filtered_moves = {k: v for k, v in valid_moves.items() if v and any(v)}
    valid_moves = filtered_moves
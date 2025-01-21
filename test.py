def display_board(start, valid_moves, board_size=8, occupied_positions=None):
    """
    Display the chessboard graphically in the console.

    Args:
        start (int): The starting position of the piece.
        valid_moves (list): A list of valid moves for the piece.
        board_size (int): The size of the board (default is 8 for an 8x8 board).
        occupied_positions (set): Positions where other pieces are located.
    """
    if occupied_positions is None:
        occupied_positions = set()

    print("Chessboard Representation:")
    for row in range(board_size):
        row_display = ""
        for col in range(board_size):
            pos = row * board_size + col
            if pos == start:
                row_display += " S "  # Starting position
            elif pos in occupied_positions:
                row_display += " O "  # Occupied positions
            elif pos in valid_moves:
                row_display += " * "  # Valid moves
            else:
                row_display += " . "  # Empty space
        print(row_display)
    print()


def get_diagonal_moves(start, board_size=8, occupied_positions=None):
    """
    Get all valid diagonal moves for a piece starting at `start`.

    Args:
        start (int): The starting position of the piece (0-63).
        board_size (int): The size of the board (default is 8 for an 8x8 board).
        occupied_positions (set): Positions where other pieces are located.

    Returns:
        list: A list of valid diagonal moves.
    """
    if occupied_positions is None:
        occupied_positions = set()

    directions = [-9, -7, 7, 9]  # Top-left, top-right, bottom-left, bottom-right
    valid_moves = []

    for direction in directions:
        current = start
        while True:
            next_square = current + direction

            # Check if the move stays on the board
            if next_square < 0 or next_square >= board_size**2:
                break

            # Check if the move wraps around the edges
            if abs((current % board_size) - (next_square % board_size)) > 1:
                break

            # If the square is occupied, stop but 
            if next_square in occupied_positions:
                break

            # Add the move and keep going in this direction
            valid_moves.append(next_square)
            current = next_square

    return valid_moves


# Example usage
occupied_positions = {13, 43}  # Example occupied squares
start_position = 27  # The piece starts at position 27
valid_moves = get_diagonal_moves(start_position, occupied_positions=occupied_positions)

# Display the board
display_board(start_position, valid_moves, occupied_positions=occupied_positions)

# Show valid moves in text
print("Valid Moves:", valid_moves)

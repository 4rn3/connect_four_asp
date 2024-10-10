import re
import random
import subprocess

def extract_cell_info(cell_info, pattern = r"\d+,\d+,\d+"):
    info = re.findall(pattern, cell_info)
    if len(info) > 0:
        position_info = [int(num) for num in info[0].split(',')]
        return position_info

def extract_positions(file_path = "./connect_four_input.lp"):
    with open(file_path, "r") as f:
        positions = {"player":[], "row":[], "col":[]}
        for line in f.readlines():
            info = extract_cell_info(line)
            if info:
                positions["player"].append(info[0])
                positions["row"].append(info[1])
                positions["col"].append(info[2])
        return positions
        
def create_game_board(num_row, num_col, default_value=' '):
    return [[default_value for _ in range(num_col)] for _ in range(num_row)]

def place_chips(positions, row, col):
    board = create_game_board(row, col)
    for i in range(len(positions['player'])):
        player = positions['player'][i]
        row = positions['row'][i] - 1  
        col = positions['col'][i] - 1

        if player == 1:
            board[row][col] = 'X'  
        elif player == 2:
            board[row][col] = 'O'
    return board    

def extract_coords_from_moves(moves_list, pattern = r"\d+,\d+"):
    return [re.findall(pattern, move) for move in moves_list]

def get_moves(file_path = "./connect_four.txt", pattern = r"\d+,\d+"):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        moves = [str for str in lines if (str.startswith("best") or str.startswith("valid") or str.startswith("win"))]
        moves = moves[0].split(" ")
        
        best_moves = [move for move in moves if move.startswith("best")]
        best_moves = extract_coords_from_moves(best_moves)
        
        valid_moves = [move for move in moves if move.startswith("valid")]
        valid_moves = extract_coords_from_moves(valid_moves)
        
        win = [move for move in moves if move.startswith("win")]
        
        return best_moves, valid_moves, win
        
def get_player(positions):
    return 1 if positions["player"][-1] % 2 == 0 else 2

def place_valid_moves(valid_moves, board):
    for move in valid_moves:
        x, y = int(move[0][0]), int(move[0][2])
        x_coord = x-1
        y_coord = y-1
        
        board[x_coord][y_coord] = "+"
    return board
        
def write_move_to_file(player, best_move_x, best_move_y, file_path="./connect_four_input.lp"):
    with open(file_path, "a") as f:
        f.write(f"cell({player},{best_move_x},{best_move_y}).  % Player {player} has a chip at row {best_move_x}, column {best_move_y}.\n")
        
def place_best_move(best_moves, board, player, greedy=True, symbol="*"):
    if greedy:
        best_move = best_moves[0]
    else:
        best_move = random.choice(best_moves)
        
    x, y = int(best_move[0][0]), int(best_move[0][2])
    x_coord = x-1
    y_coord = y-1
    board[x_coord][y_coord] = symbol
    
    write_move_to_file(player, x, y)
    
    return board

def show_board(board):
    for row in reversed(board):
        print(row)
        
def run_clingo():
    command = [
    "clingo", "0", 
    "connect_four_input.lp", "weights.lp", "connect_four.lp"
    ]
    
    output_file = "connect_four.txt"
    
    with open(output_file, "w") as file:
        subprocess.run(command, stdout=file, text=True)

def get_user_move():
    move = input("Enter the row, col you want to place your chip (i.e. 1,1) or q to quit:")
    
    if move == 'q':
        return False
    
    temp = move.split(',')
    x = int(temp[0])
    y = int(temp[1])
    
    write_move_to_file(player=1, best_move_x=x, best_move_y=y)
    return True

def main(num_row = 6, num_col = 7, real_game = False, greedy = True):
    
    game_loop = True
    
    while game_loop:
        game_loop = get_user_move()
        run_clingo()
        
        positions = extract_positions()
        board_with_chips = place_chips(positions, num_row, num_col)
        best_moves, valid_moves, win = get_moves()
        
        player = get_player(positions)
        
        if len(win)>0:
            print(f"Game over: Player {2 if player == 1 else 1} won")
            break
        
        if not real_game:
            board_with_valid_moves = place_valid_moves(valid_moves, board_with_chips)
            board_with_best_move = place_best_move(best_moves=best_moves, board=board_with_valid_moves, player=player)
            show_board(board_with_best_move)
        
        if real_game:
            symbol = "X" if player == 1 else "O"
            board_with_best_move = place_best_move(best_moves=best_moves, board=board_with_chips, player=player, symbol=symbol)
            show_board(board_with_best_move)

main(real_game=True)
import re

num_row = 6
num_col = 7

pattern = r"\d+,\d+,\d+"

with open("./positions.txt", "r") as f:
    positions = f.readlines()


cells = {"player":[], "row":[], "col":[]}
for pos in positions:
    temp = re.findall(pattern, pos)
    cells["player"].append([int(num) for num in temp[0].split(',')][0])
    cells["row"].append([int(num) for num in temp[0].split(',')][1])
    cells["col"].append([int(num) for num in temp[0].split(',')][2])
    

def create_game_board(num_row, num_col, default_value=' '):
    return [[default_value for _ in range(num_col)] for _ in range(num_row)]

board = create_game_board(num_row, num_col)

def place_player_chips(game_field, positions):
    for i in range(len(positions['player'])):
        player = positions['player'][i]
        row = positions['row'][i] - 1  
        col = positions['col'][i] - 1 
        
        if player == 1:
            game_field[row][col] = 'X'  
        elif player == 2:
            game_field[row][col] = 'O'
    
    return game_field

board = place_player_chips(board, cells)

def select_valid_moves(file_path="./connect_four.txt"):
    valid_moves = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("best_move"):
                valid_moves.append(line.strip())

    return valid_moves

valid_moves = select_valid_moves()
valid_moves = [move for move in valid_moves[0].split(' ')]
best_move = valid_moves[0]
valid_moves = valid_moves[1:]

def convert_valid_moves(valid_moves):
    pattern = r'\(\d+,\d+\)'
    moves = []
    for move in valid_moves:
        temp = re.findall(pattern, move)[0]
        moves.append(temp)
    return moves

converted_moves = convert_valid_moves(valid_moves)

for pos in converted_moves:
    x ,y = int(pos[1])-1, int(pos[3])-1
    board[x][y] = '|'

board[int(best_move[10])-1][int(best_move[12])-1] = "*"

print(best_move)

for row in reversed(board):
    print(row)

first_or_second = 1 if cells["player"][-1] % 2 == 0 else 2
  
with open("./connect_four_input.lp", "a") as f:
    f.write(f"cell({first_or_second},{best_move[10]},{best_move[12]}).  % Player {first_or_second} has a chip at row {best_move[10]}, column {best_move[12]}.\n")
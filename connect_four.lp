%Default board config
#const num_row = 6.
#const num_col = 7.

%Board
row(1..num_row).
col(1..num_col).
player(1;2).

%Moves
occupied(Row, Col) :- cell(_, Row, Col). %can't place chip if there is already a chip
empty(Row, Col) :- row(Row), col(Col), not occupied(Row, Col).

%% a move is valid if the row the chip being placed is empty and it is the lowest row or the row under it is occupied
valid_move(1, Col) :- empty(1, Col). %valid if lowest row selected and it's empty
valid_move(Row, Col) :- row(Row), Row > 1, col(Col), empty(Row, Col), occupied(Row-1, Col). %valid if selected is free and row under it is occupied

%Win conditions
win(Player) :- cell(Player, Row, Col), cell(Player, Row, Col+1), cell(Player, Row, Col+2), cell(Player, Row, Col+3). %horizontal conneft four
win(Player) :- cell(Player, Row, Col), cell(Player, Row+1, Col), cell(Player, Row+2, Col), cell(Player, Row+3, Col). %vertical connect four
win(Player) :- cell(Player, Row, Col), cell(Player, Row+1, Col+1), cell(Player, Row+2, Col+2), cell(Player, Row+3, Col+3). %diagonal upward
win(Player) :- cell(Player, Row, Col), cell(Player, Row-1, Col+1), cell(Player, Row-2, Col+2), cell(Player, Row-3, Col+3). %diagonal downward

%Strategy

%%Set preference for center
score(Row, 4, center_weight) :- valid_move(Row, 4). %TO DO make dynamic

%%%Gradually decrease weight for rows further from the center
score(Row, Col, center_weight) :- valid_move(Row, Col), Col = 3; Col = 5.
score(Row, Col, 2) :- valid_move(Row, Col), Col = 2; Col = 6. %to do make decrease dynamic
score(Row, Col, 1) :- valid_move(Row, Col), Col = 1; Col = 7.

%%Set preference for odd rows when player 1
odd(1).
odd(Row) :- row(Row), row(Prev_Row), odd(Prev_Row), Row = Prev_Row + 2.
score(Row, Col, odd_even_weight) :- valid_move(Row, Col), player(1), odd(Row).

%%Set prefence for even rows when player 2
score(Row, Col, odd_even_weight) :- valid_move(Row, Col), player(2), not odd(Row).

%%Immediate win moves
%%% Horizontal connect four with variations
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row, Col-1), cell(Player, Row, Col-2), cell(Player, Row, Col-3). 
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row, Col+1), cell(Player, Row, Col+2), cell(Player, Row, Col+3).
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row, Col-1), cell(Player, Row, Col+1), cell(Player, Row, Col-2).
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row, Col+1), cell(Player, Row, Col-1), cell(Player, Row, Col-2).

%%% Vertical connect four, only this variation is possible
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row-1, Col), cell(Player, Row-2, Col), cell(Player, Row-3, Col).

%%% Diagonal win (upward-right and downward-left) with their variations
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row-1, Col-1), cell(Player, Row-2, Col-2), cell(Player, Row-3, Col-3).
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row+1, Col-1), cell(Player, Row+2, Col-2), cell(Player, Row+3, Col-3). 
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row-1, Col+1), cell(Player, Row-2, Col+2), cell(Player, Row-3, Col+3).  
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row+1, Col+1), cell(Player, Row+2, Col+2), cell(Player, Row+3, Col+3). 
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row+1, Col+1), cell(Player, Row-1, Col-1), cell(Player, Row+2, Col+2).  
winning_move(Player, Row, Col) :- valid_move(Row, Col), cell(Player, Row-1, Col+1), cell(Player, Row+1, Col-1), cell(Player, Row+2, Col-2).  

score(Row, Col, immediate_win_weight) :- winning_move(1, Row, Col). %assign a score to this category of move

%%Blocking moves
blocking_move(Row, Col) :- valid_move(Row, Col), player(1), winning_move(2, Row, Col). %if we see a winning move for our opponent take the cell
blocking_move(Row, Col) :- valid_move(Row, Col), player(2), winning_move(1, Row, Col).

score(Row, Col, block_weight) :- blocking_move(Row, Col).

%%Combine scores
total_score(Row, Col, Total) :- valid_move(Row, Col), Total = #sum{S : score(Row, Col, S)}.
#maximize{Total, Row, Col : total_score(Row, Col, Total)}.
best_move(Row, Col) :- total_score(Row, Col, Total), Total = #max{T : total_score(_, _, T)}.

#show valid_move/2.
#show best_move/2.
#show win/1.
#show score/3.
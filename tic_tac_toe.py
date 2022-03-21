board = ['-', '-', '-',
         '-', '-', '-',
         '-', '-', '-']

gameplay = [1, 0, 1, 0, 1, 0, 1, 0, 1]
player_dict = {1: 'X', 0: 'O'}
play_history_dict = {}
def display_board():
    print(board[0] + '|' + board[1] + '|' + board[2])
    print(board[3] + '|' + board[4] + '|' + board[5])
    print(board[6] + '|' + board[7] + '|' + board[8])

def play_history():
    pass

winner = None
class Win_Determine:
    def row(player):
        global winner
        previous = 0
        for i in range(3, 12, 3):
            arr = list(board[previous:i]); previous = i
            if '-' not in arr:
                if all([x == arr[0] for x in arr]):
                    winner = player_dict[player]
                    print('Player {} win'.format(player))
    
    def column(player):
        global winner
        for index in range(3):
            arr = [board[index], board[index+3], board[index+6]]
            if '-' not in arr:
                if all([x == arr[0] for x in arr]):
                    winner = player_dict[player]
                    print('Player {} win'.format(player))

    def slash(player):
        global winner
        arr_1 = [board[0], board[4], board[8]]
        arr_2 = [board[2], board[4], board[6]]
        for i in [arr_1, arr_2]:
            if '-' not in i:
                if all([x == i[0] for x in i]):
                    winner = player_dict[player]
                    print('Player {} win'.format(player))

def play_move(player):
    move = int(input('Player {}, Select a location: '.format(player_dict[player])))
    if board[move] == '-':
        board[move] = player_dict[player]
    else:
        return play_move(player)

def clear_board():
    for index in range(len(board)):
        if index != '-':
            board[index] = '-'

def tic_tac_toe():
    while True:
        display_board()
        for player in gameplay:
            play_move(player)
            display_board()
            Win_Determine.row(player)
            Win_Determine.column(player)
            Win_Determine.slash(player)
            if winner != None:
                clear_board()
                break
        if winner == None:
            clear_board()
            print('Draw')
        print('-----------------------')
tic_tac_toe()

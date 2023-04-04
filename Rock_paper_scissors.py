import random as rd

objects = ['rock', 'paper', "scissor"] # Rock: 0, Paper: 1, Scissor: 2
condition = {'0,2': 'rock', '2,0': 'rock', '0,1': 'paper', '1,0': 'paper', '1,2': 'scissor', '2,1': 'scissor'}
rounds = int(input('How many rounds(int): '))
game = 0
drew = 0
count = 0

def play():
    global rounds, game, count, drew
    while game < rounds:
        game += 1
        print('Game %d'.center(20, "-") % game)
        player_move = objects.index(input("Rock, Paper, or Scissor: ").lower())
        computer_move = rd.randint(0,2) # Computer pick an object
        print("Your selection: %s, Computer's selection: %s" % (objects[player_move], objects[computer_move]))
        if player_move == computer_move:
            drew += 1
            print('Game %d: Drew!' % game)
            continue
        winning_move = [str(player_move) + ',' + str(computer_move)]
        print(condition[''.join(winning_move)], player_move)
        if condition[''.join(winning_move)] == objects[player_move]:
            count += 1
            print('Game %d: Player Wins!' % game)
        if condition[''.join(winning_move)] == objects[computer_move]:
            print('Game %d: Computer Wins!' % game)

    if count > (rounds-drew)/2:
        return 'Final Result: Player Wins'
    if count == (rounds-drew)/2:
        return 'Final Result: Drew'
    else:
        return 'Final Result: Computer Wins'

print(play())

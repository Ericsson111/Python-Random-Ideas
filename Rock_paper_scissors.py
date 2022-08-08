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
        return 'Final Conclusion: Player Wins'
    if count == (rounds-drew)/2:
        return 'Final Conclusion: Drew'
    else:
        return 'Final Conclusion: Computer Wins'

print(play())

# Use reverse method(list[::-1])
'''
import random as rd

objects = ['rock', 'paper', "scissor"] # Rock: 0, Paper: 1, Scissor: 2
condition = {'0,2': 'rock', '0,1': 'paper', '1,2': 'scissor'}
rounds = int(input('How many rounds(int): '))
game = 0
count = 0

def play():
    global rounds, game, count
    while game < rounds:
        game += 1
        print('Game %d'.center(20, "-") % game)
        player_move = objects.index(input("Rock, Paper, or Scissor: ").lower())
        computer_move = rd.randint(0,2) # Computer pick an object
        print("Your selection: %s, Computer's selection: %s" % (objects[player_move], objects[computer_move]))
        if player_move == computer_move:
            print('Game %d: Drew!' % game)
            continue
        winning_move = [str(player_move) + ',' + str(computer_move)]
        winning_move_reverse = [str(computer_move) + ',' + str(player_move)]
        if ''.join(winning_move) in condition.keys():
            print('a')
            if condition[''.join(winning_move)] == objects[player_move]:
                print('b')

                if winning_move[0] == player_move:
                    print('c',winning_move)
                    count += 1
                    print("Game %d: Player Wins!" % game)
                if winning_move[0] == computer_move:
                    print('x',winning_move[0])
                    print("Game %d: Computer Wins!" % game)

            if condition[''.join(winning_move)] != objects[player_move]:
                print('y', ''.join(winning_move_reverse)[0])
                print("Game %d: Computer Wins!" % game)

        if ''.join(winning_move) not in condition.keys():
            print('d')
            if ''.join(winning_move_reverse) in condition.keys():
                print('e')
                if condition[''.join(winning_move_reverse)] == objects[player_move]:
                    print('f')

                    if winning_move_reverse[-1] == player_move:
                        print('g', ''.join(winning_move_reverse)[-1])
                        count += 1
                        print("Game %d: Player Wins!" % game)
                    if winning_move_reverse[0] == computer_move:
                        print('h', ''.join(winning_move_reverse)[0])
                        print("Game %d: Computer Wins!" % game)

                if condition[''.join(winning_move_reverse)] != objects[player_move]:
                    print('z', ''.join(winning_move_reverse)[0])
                    print("Game %d: Computer Wins!" % game)
 
    if count > rounds/2:
        return 'Final Conclusion: Player Wins'
    if count == rounds/2:
        return 'Final Conclusion: Drew'
    else:
        return 'Final Conclusion: Computer Wins'

print(play())

# Use reverse method(list[::-1])
'''
'''
import random as rd

objects = ['rock', 'paper', "scissor"] # Rock: 0, Paper: 1, Scissor: 2
condition = {'0,2': 'rock', '0,1': 'paper', '1,2': 'scissor'}
rounds = int(input('How many rounds(int): '))
game = 0
count = 0

def play():
    global rounds, game, count
    while game < rounds:
        game += 1
        print('Game %d'.center(20, "-") % game)
        player_move = objects.index(input("Rock, Paper, or Scissor: ").lower())
        computer_move = rd.randint(0,2) # Computer pick an object
        print("Your selection: %s, Computer's selection: %s" % (objects[player_move], objects[computer_move]))
        if player_move == computer_move:
            print('Game %d: Drew!' % game)
            continue

        winning_move = [player_move,computer_move] # integers
        # certain move from player and computer could not be found on the condition keys, so we create a reverse list to double check
        winning_move_reverse = [computer_move, player_move]
        if objects[int(','.join(map(str,winning_move))[0])] == condition[','.join(map(str,winning_move))]:
            count += 1
            print("Game %d: Player Wins!" % game)
        if objects[int(','.join(map(str,winning_move))[0])] != condition[','.join(map(str,winning_move))]:
            print("Game %d: Computer Wins!" % game)
        if objects[int(','.join(map(str,winning_move_reverse))[2])] == condition[','.join(map(str,winning_move_reverse))]:
            count += 1
            print("Game %d: Player Wins!" % game)

    if count > rounds/2:
        return 'Final Conclusion: Player Wins'
    if count == rounds/2:
        return 'Final Conclusion: Drew'
    else:
        return 'Final Conclusion: Computer Wins'

print(play())

# Use reverse method(list[::-1])
'''
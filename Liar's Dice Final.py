# Liar's Dice
# Inspiration taken from https://gist.github.com/dxdydz/2411156
# Emily Hostetler
# 11/28/2017

'''This program is designed to run a game called Liar's Dice.
There is one human player, and between one and four computer players.
The goal of the game is to have the highest bet without being accused of lying.
The game continues until all but one players have lost all their dice.
The program runs through use of global variables and functions, in an attempt to make
the code easier to understand.'''

import random
import time
import itertools

names = ['Emily', 'Erin', 'Collin', 'Austin', 'Daniel', 'Owen', 'Kayla', 'Gottfreid', 'Srinivasa', 'Leonardo', 'Blaise', 'Leonhard', 'Pythagoras']
numbers = ['', 'one', 'two', 'three', 'four', 'five', 'six']
num_players = 0
player_list = []
player_name = ''
player_rolls = []
player = ''
current_bet = []
challenger = ''
player_num = 0
num_dice = []
player_alive = True
dice_list = []


def welcome(): #Welcomes the player to the game and runs initializing sequence
    global num_players
    global player_list
    global player_name
    print("Welcome to Liar's Dice!")
    player_name  = input('Please enter your name: ')
    num_players = input('Enter how many players, between two and five: ') #Allows player to select number of players
    try: #Handles any errors in input
        num_players = int(num_players)
    except:
        num_players = int(input('please enter a digit between 2 and 5: '))
    player_list.append(player_name)
    for i in range(0, num_players-1):
        a = names[random.randint(0,len(names)-1)]
        player_list.append(a)
        names.remove(a)
    return player_list #Creates a list of players in this game

def instructions(): #prints instructions if needed
    q = input("Do you know how to play Liar's Dice? Type Y or N: ")
    if q.lower() == 'y':
        print("Great, let's begin!")
    else:
        print("Liar's Dice Rules: ")
        time.sleep(1)
        print("Every player begins with 5 dice. They roll and look at the hand they have been given.")
        time.sleep(4)
        print("The first player must then put out a bet, saying what number, and how many they believe are on the table.")
        time.sleep(5)
        print("The next player must either up the ante by number of dice, or by number on the die, or accuse the last player of lying.")
        time.sleep(5)
        print("If they accuse the last player of lying, all the dice are laid out on the table, and the number suggested are counted.")
        time.sleep(5)
        print("Whoever was wrong, either the liar, or the accuser, loses one die.")
        time.sleep(4)
        print("The game continues until only one player is left with dice.")
        time.sleep(2)
        print("Now, Let's begin!")

def dice_roll_init(): #Gives players their rolls for the round
    global num_players
    global player_list
    global player_rolls
    global dice_list
    for i in range(0,num_players):
        init_dice = []
        for j in range(0,5): #Rolls 5 dice for each player, can be adjusted to make a shorter or longer game
            player_roll = random.randint(1,6)
            init_dice.append(player_roll)
        player_rolls.append(init_dice)
        dice_list.append(len(init_dice))
    return player_rolls


def reroll():
    global num_players
    global player_list
    global player_rolls
    global dice_list
    print("\nReroll!\n")
    player_rolls.clear()
    for j in dice_list:
        init_dice = []
        for k in range(0,j):
            player_roll = random.randint(1,6)
            init_dice.append(player_roll)
        player_rolls.append(init_dice)
    return player_rolls
amt_of_dice = 0
dice_num = 0

def player_turn(): #Runs every time it is the human player's turn
    global current_bet
    global player_alive
    global dice_num
    global amt_of_dice
    print()
    try:
        print("There are %s dice on the table" % str(str(player_rolls).count(',')+1))
        time.sleep(.5)
        human_index = player_list.index(player_name)
    except:
        player_alive = False
        return player_alive
    print("Your Dice: ", player_rolls[human_index])
    time.sleep(.5)
    print("Would you like to [b]et or [c]hallenge?")
    choice = input()
    try:
        if choice == 'b':
            print("Enter your bet in the form, [number of dice] [number on dice]: ")
            bet_input = input()
            current_bet = bet_input.split(" ")
            amt_of_dice = int(current_bet[0])
            dice_num = int(current_bet[1])
        elif choice == 'c':
            challenger = player_list[0]
            challenge(challenger)
        else:
            raise Exception("Failed to enter 'b' or 'c'")

    except RuntimeError:
        print("Please enter 'b' or 'c'")
        choice  = input()
        if choice == 'b':
            print("Enter your bet in the form, [number of dice] [number on dice]: ")
            bet_input = input()
            current_bet = bet_input.split(" ")
            amt_of_dice = int(current_bet[0])
            dice_num = int(current_bet[1])
        elif choice == 'c':
            challenger = player_list[0]
            challenge(challenger)
    time.sleep(1)

#Runs when a player decides to challenge a bet, whether human or computer
def challenge(challenger):
    global player_list
    global player_rolls
    global amt_of_dice
    global dice_num
    global current_bet
    global num_players
    print(challenger + " has decided to challenge the bet")
    time.sleep(1)
    actual = 0
    for i in player_rolls:
        for j in i:
            if j==dice_num:
                actual+=1
    print()
    print("There are" + " " + str(actual) + " " + str(current_bet[1]) + "'s on the board.")
    time.sleep(1)
    print()
    if int(current_bet[0]) <= actual:
        loser = player_list.index(challenger)
        loser_name = player_list[loser]
        print("Current Hands: ",  player_rolls)
        print()
        print(challenger + " loses one die.")
        print()
        player_rolls[loser].pop()
        dice_list[loser] -= 1
        time.sleep(1)
        current_bet = []
        if player_rolls[loser] == []: #Removes player after all their dice are gone
            player_list.remove(loser_name)
            player_rolls.remove(loser)
            num_players -= 1
        reroll()
    else:
        loser = player_list.index(challenger)-1
        dice_list[loser] -= 1
        loser_name = player_list[loser]
        print("Current Hands: ", player_rolls)
        player_rolls[loser].pop()
        print()
        print(loser_name + " loses one die.")
        print()
        time.sleep(1)
        current_bet = []
        if player_rolls[loser] == []: #Same as above
            player_rolls.pop(loser)
            player_list.remove(loser_name)
            num_players -= 1
        reroll()
    time.sleep(1)
    

def turn_select(): #Selects whose turn it is in the beginning
    global num_players
    global player
    global player_num
    player_num = random.randint(1,num_players-1)
    player = player_list[player_num]
    if player == player_name:
        print("It's your turn!")
        print()
    else:
        print("It's " + player + "'s turn")
        print()

def computer_turn(player): #Runs for computer's turn
    global current_bet
    global amt_of_dice
    global dice_num
    global numbers
    global player_num
    global dice_list
    if current_bet == []:
        amt_of_dice = 1
        dice_num = random.randint(1,6)
        current_bet = [amt_of_dice, dice_num]
        time.sleep(1)
        print((player + " has bet one " + numbers[dice_num]))
        time.sleep(1)
    else:
        actual = 0
        for i in player_rolls[player_list.index(player)]:
            if i==dice_num:
                actual+=1
        if int(current_bet[0]) > (actual + 2): #Challenges the bet when someone bets anything higher than how many the computer has
            challenger = player
            challenge(challenger)
        else:
            current_bet[0] = int(current_bet[0]) + 1 #Raises the current bet by one
            print(player + " has bet " +str(current_bet[0]) + " " + numbers[int(current_bet[1])] + "'s")
            time.sleep(1)
    time.sleep(1)

          
    

welcome()
instructions()
dice_roll_init()
time.sleep(1)
print('Your Hand: ', player_rolls[0])
time.sleep(1)
print()
turn_select()

if  player == player_name:
    player_turn()
else:
    computer_turn(player)
while len(player_list) > 1:
    #Something in this cycle is wonky with more than two players,
    #it continues to give players turns, even after they are removed from player_list
    for player in itertools.cycle(player_list):
        if len(player_list) == 1:
            break
        if player == player_name:
            player_turn()
            time.sleep(1)
        else:
            computer_turn(player)
            time.sleep(1)
if player_list[0] == player_name:
    print("You Win!!")
    time.sleep(.5)
else:
    print("Better Luck Next Time...")
    time.sleep(.5)
print("Thanks for playing!")
time.sleep(1)



    

    









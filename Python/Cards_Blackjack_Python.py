#Blackjack
#29-30 Sept 2022, maroun

#Program Functions first
#Main code after them
#exersice & game instructions at the very bottom


# F U N C T I O N S

def print_final_winner(sum_pl, sum_com):
  print("...AND THE WINNER IS...")
  if sum_pl==21 and sum_com==21:
      print("Both won    :-O")
  elif (sum_com>=17 and sum_com<=21) and (sum_pl>=17 and sum_pl<=21):
      if sum_com>sum_pl:
          print("Computer won!")
      elif sum_com==sum_pl:
          print("Same points, chose the winner yourselves...")
      else:
          print("You won!!")
  elif (sum_com>=17 and sum_com<=21) and not (sum_pl>=17 and sum_pl<=21):
      print("Computer won!")
  elif not (sum_com>=17 and sum_com<=21) and (sum_pl>=17 and sum_pl<=21):
      print("You won!")
  else:
      print("Both lost   :'(")

def continue_game(player, sum):
    if player == 0:
        #computer playing
        if (sum<17):
          ans = "0"
        else:
          import random
          decide = random.randint(0,1)
          if decide==0:
            ans = "0"
          else:
            ans = "jfka;afh"
    else:
        #real user playing
        ans = input("Press 0 to continue, or anything else to quit playing\n->")
        if ans!="0":
            if sum<17:
              print(f"Current cards summary is {sum}")
              print("DEFEAT")
            else:
              print(f"Current cards summary is {sum}")
              print("Stop playing and risking")
    return ans

def manage_aces(sum,aces1, aces11):
    if aces1 == 0 and aces11 == 0:
        return sum, aces1, aces11
    #empty all aces points and manage them from the beginning
    sum = sum - aces1*1 - aces11*11
    #add how many Ace cards you got
    count = aces1 + aces11
    while(count > 0):
        if (sum + 11 <= 21):
            sum = sum + 11
            aces11 = aces11 + 1
        else:
            sum = sum + 1
            aces1 = aces1 + 1
        count = count - 1
    return sum, aces1, aces11

def card_points(num):
    cards = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King")
    print("  *NEW CARD*")
    if (num>=2 and num<=10):
        print(f"     Card picked: {cards[num-1]}")
        print(f"     +{num} points")
        return num
    elif (num>10):
        print(f"     Card picked: {cards[num-1]}")
        print(f"     +{10} points")
        return 10
    else: 
        print("     Card picked: Ace")
        print(f"     +{1} or +{11} points")
        #suppose you count aces as 11 (might change later)
        return 11

def update_sum(sum,aces1,aces11):
    import random
    new_card = random.randint(1,13)
    sum = sum + card_points(new_card)
    if new_card==1:
        aces11 = aces11 + 1
        if sum <= 21:
            print(f"Current cards summary is either {sum} or {sum - 11 + 1}\n")
        else:
            sum, aces1, aces11 = manage_aces(sum,aces1, aces11)
            print(f"Current cards summary is {sum}\n")
    else:
        print(f"Current summary is {sum}\n")
    return sum, aces1, aces11
  
def make_a_move(player, sum, aces1, aces11):
    #the first return value indicates a situation
    #-1 for lossing game, 0 for keep playing, 1 for winning
    if sum < 17:
        print("Summary less than 17. Needs to continue OR quit and lose")
    elif sum<21:
        print("Over 17, you're in the game, but still not reached 21...")
      
    if sum<17 or sum<21:
        ans = continue_game(player, sum)
        if (ans == "0"):
            sum, aces1, aces11 = update_sum(sum, aces1, aces11)
        else:
            return -1, sum, aces1, aces11
            
    if (sum==21):
        print("21 points! AMAZING!!!")
        print("WIN WIN WIN")
        return 1, sum, aces1, aces11
    elif (sum>21):
        print("Summary over 21")
        print("DEFEAT")
        return -1, sum, aces1, aces11
    else:
        return 0, sum, aces1, aces11




# M A I N   C O D E

#write main code
def main():
  print("\nB  L  A  C  K  J  A  C  K\n\n")
  cards = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King")
  
  print("YOUR TURN\n")
  sum_pl = 0
  aces1 = 0
  aces11 = 0
  print(f"Current cards summary is {sum_pl}")
  situation_pl = 0 
  #situation values could be:
  #-1 for lossing game, 0 for keep playing, 1 for winning
  while (situation_pl == 0):
      situation_pl, sum_pl, aces1, aces11 = make_a_move(1, sum_pl, aces1, aces11)
      import time
      time.sleep(1)
  print("---------------------------")
  print(f"YOUR Total points: {sum_pl}")
  print("---------------------------\n\n\n")
  
  print("COMPUTER'S TURN\n")
  sum_com = 0
  aces1 = 0
  aces11 = 0
  print(f"Current cards summary is {sum_com}")
  situation_com = 0 
  #situation values could be:
  #-1 for lossing game, 0 for keep playing, 1 for winning
  while (situation_com == 0):
      situation_com, sum_com, aces1, aces11 = make_a_move(0, sum_com, aces1, aces11)
      import time
      time.sleep(2)
  print("---------------------------")
  print(f"COMPUTER'S Total points: {sum_com}")
  print("---------------------------\n\n\n")
  
  print_final_winner(sum_pl, sum_com)

#execute main code
main()


#     G  A  M  E     I  N  S  T  R  U  C  T  I  O  N  S

#  B L A C K J A C K ,   A S   A   C A R D   G A M E
#Blackjack is a game played with cards
#Players keep collecting cards from the deck and count the summary of the numbers indicated in the cards they picked
#The goal is the summary of your cards to be 21, or something close to it, smaller than 21
#If someone has a summary that exceeds 21, they automatically lose
#Also, it is forbidden to someone to stop picking cards while their summary is under 17
#While picking cards, the numbers from 2,3,...,10 count as 2,3,...,10 points
#Special figures (king, queen, jack) count as 10 points 
# The 1 (Ace) counts as 1 or 11, whatever the user needs most. 
# The Ace value can change from 1 to 11 (or vise versa), but in the end the most beneficial number is been picked

#  P R O G R A M M I N G   B L A C K J A C K
#write a program in which the user plays against the computer
#the program shall generates random cards to be picked each time for the user and later for the computer
#before picking a card, human players shall be asked if they want to procced or stop playing. They can withdraw anytime, even if their cards summary is less than 17 (this means they lose). Humans shall continue playing by hitting "0", or anything different to stop risking. 
#for the computer, when summary is lower than 17, we assume the machine keeps playing. If over 17 but lower than 21, a random generator shall decide its luck.


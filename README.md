usage:

python Bridge.py -p 3 -r True 

-- or --

python Bridge.py 
        The players note their points when one player has no more cards.

        These are the card values:
         6: 0
         7: 0
         8: 0
         9: 0
        10: 10
         J: 20 (-20)
         Q: 10
         K: 10
         A: 15

        The points of several rounds will be added.
        If a player finishes a round with a 'J' his score will be
        reduced by 20 for each 'J' on stack of his last move.
        If a player reaches exactly 125 points, his score is back on 0!
        When the blind was empty and therefor the stack was reshuffeled,
        the points of this round are doubled (trippled, ...).
        The player with the highest score starts the next round.

        The round is over once a player reaches more than 125 points.

        During the game you can play several rounds.

        
Enter number of players (2-4):3

Game with 3 players
Play against Robots (y)es or (n)o:y

You play against 2 robot(s)!

                         Press 'enter' to start




Player-1 holds (4) card(s) [10 points]:
♦9 ♥7 ♠8 ♦10 
Player-2 holds (5) card(s):
## ## ## ## ## 
Player-3 holds (5) card(s):
## ## ## ## ## 

                    Blind (21) card(s):
                    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 

Bridge monitor (1) card(s):
♦A 

                    Stack (1) card(s):
                    ♦A 

Player-1 has played (1) card(s) / drawn (0) card(s) and can play (0) card(s):

Player-1 holds (4) card(s) [10 points]:
♦9 ♥7 ♠8 ♦10 


       | TAB: toggle |  SHIFT: put  |  ALT: draw  |
       |            SPACE: next Player            |
       |  (s)cores   |   (r)ules    |   (q)uit    |

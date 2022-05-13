#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Classic Card Game for 2-4 Players or 1 Player against Robots
'''

import sys
import argparse
import os
import random
from datetime import date
import keyboard

suits = ['\u2666', '\u2665', '\u2660', '\u2663']
ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suit_colors = ['\033[95m', '\033[91m', '\033[93m', '\033[94m']
RESET_COLOR = '\033[0m'


class Card:
    ''' Card definition - 4 ranks with values from 6 to Ace'''

    def __init__(self, suit, rank):
        if suit in suits and rank in ranks:
            self.suit = suit
            self.rank = rank
            self.value = self.set_value(self.rank)

    def __str__(self):
        card = None
        if self.suit == '\u2666':
            card = f'{suit_colors[0]}{self.suit}{self.rank}{RESET_COLOR} '
        elif self.suit == '\u2665':
            card = f'{suit_colors[1]}{self.suit}{self.rank}{RESET_COLOR} '
        elif self.suit == '\u2660':
            card = f'{suit_colors[2]}{self.suit}{self.rank}{RESET_COLOR} '
        elif self.suit == '\u2663':
            card = f'{suit_colors[3]}{self.suit}{self.rank}{RESET_COLOR} '
        return card

    def __lt__(self, other):
        if self.get_value() < other.get_value():
            return True
        return False

    def __gt__(self, other):
        if self.get_value() > other.get_value():
            return True
        return False

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def set_value(self, rank):
        value = 0
        if rank in {'10', 'Q', 'K'}:
            value = 10
        if rank == 'A':
            value = 15
        if rank == 'J':
            value = 20
        return value

    def get_value(self):
        return self.value


class Jsuit:
    ''' Representing special representation of card 'J' by 2 suits '''

    def __init__(self, suit, color):
        self.suit = suit
        self.color = color

    def __str__(self):
        sign = f'{self.color}{self.suit}{self.suit}{RESET_COLOR} '
        return sign

    def __eq__(self, other):
        if self.suit == other.suit:
            return True
        else:
            return False

    def get_suit(self):
        return self.suit


class Jchoice:
    ''' Choose a Jsuits '''
    # js = []
    # j = None

    def __init__(self):
        self.js = [Jsuit('\u2666', '\033[95m'), Jsuit('\u2665', '\033[91m'),
                   Jsuit('\u2660', '\033[93m'), Jsuit('\u2663', '\033[94m')]
        self.j = None

    def toggle_js(self):
        self.js.insert(0, self.js.pop())

    def set_j(self, color=None):
        if color:
            self.j = self.js[color]
        else:
            self.j = self.js[-1]

    def clear_j(self):
        self.j = None

    def get_j(self):
        if self.j:
            return self.j
        return ''

    def get_j_suit(self):
        if self.j:
            return self.j.suit

    def show_js(self):
        js = ''
        for j in self.js:
            js += str(j)
        print(11 * " " + js)


jchoice = Jchoice()


class Deck:
    ''' The game board with blind and stack '''

    def __init__(self):
        self.blind = []
        self.stack = []
        self.cards_played = []
        self.bridge_monitor = []
        self.shufflings = 1
        self.is_visible = False

        for suit in suits:
            for rank in ranks:
                self.blind.append(Card(suit, rank))
        self.shuffle_blind()

    def show(self):
        self.show_blind(self.is_visible)
        self.show_bridge_monitor()
        self.show_stack(self.is_visible)

    def show_blind(self, visible=True):
        blind = ''
        for card in self.blind:
            if visible:
                blind += str(card)
            else:
                blind += '## '
        print(f'\n{20 * " "}Blind ({len(self.blind)}) card(s):')
        print(f'{20 * " "}{blind}\n')

    def shuffle_blind(self):
        random.shuffle(self.blind)

    def card_from_blind(self):
        if len(self.blind) == 0:
            self.blind = self.stack
            self.stack = []
            self.stack.append(self.blind.pop())
            random.shuffle(self.blind)
            self.shufflings += 1
        if self.blind:
            return self.blind.pop()
        print('not enough cards available')
        sys.exit()

    def show_stack(self, visible=True):
        stack = ''
        if visible:
            for card in self.stack:
                stack = str(card) + stack

        else:
            if self.cards_played:
                for card in range(len(self.stack) - len(self.cards_played)):
                    stack += '## '
                stack = f'{self.show_cards_played()}' + stack
            else:
                for card in range(
                        len(self.stack) - len(self.cards_played) - 1):
                    stack += '## '
                stack = str(self.stack[-1]) + stack

        stack = f'{jchoice.get_j()}' + stack
        print(f'{20 * " "}Stack ({len(self.stack)}) card(s):')
        print(f'{20 * " "}{stack}\n')

    def put_card_on_stack(self, card):
        self.stack.append(card)
        self.cards_played.append(card)
        self.update_bridge_monitor(card)

    def get_top_card_from_stack(self):
        if self.stack:
            return self.stack[-1]

    def update_bridge_monitor(self, card: Card):
        if deck.bridge_monitor and card.rank != deck.bridge_monitor[0].rank:
            deck.bridge_monitor.clear()
        deck.bridge_monitor.append(card)

    def show_bridge_monitor(self):
        bridge_stack = ''
        for card in self.bridge_monitor:
            bridge_stack = str(card) + bridge_stack
        print(f'Bridge monitor ({len(self.bridge_monitor)}) card(s):')
        print(f'{bridge_stack}\n')

    def show_cards_played(self):
        cards_played = ''
        for card in self.cards_played:
            cards_played = str(card) + cards_played
        return cards_played


deck = Deck()


class Handdeck:
    ''' The cards in one players hand '''

    def __init__(self):
        self.cards = []
        self.cards_drawn = []
        self.possible_cards = []

    def __len__(self):
        return len(self.cards)

    def count_points(self):
        points = 0
        for card in self.cards:
            points += card.value
        return points

    def arrange_hand_cards(self, pattern=0):
        patterns = (('J', '9', '7', '8', '10', 'Q', 'K', 'A', '6'),
                    ('J', 'A', 'K', 'Q', '10', '9', '8', '7', '6'),
                    ('9', '8', '7', '6', '10', 'Q', 'K', 'A', 'J'))

        sorted_cards = []

        for rank in patterns[pattern]:
            for card in self.cards:
                if card.rank == rank:
                    sorted_cards.append(card)
        self.cards = sorted_cards

    def remove_card_from_cards(self, c: Card):
        if self.cards:
            for card in self.cards:
                if card.suit == c.suit and card.rank == c.rank:
                    self.cards.remove(card)

    def remove_card_from_possible_cards(self, c: Card):
        if self.possible_cards:
            for card in self.possible_cards:
                if card.suit == c.suit and card.rank == c.rank:
                    self.possible_cards.remove(card)

    def get_possible_cards(self):

        self.possible_cards = []
        stack_card = deck.get_top_card_from_stack()

        '''
        1st move:
        ---------
        general rule:         suit   rank    J
        if stack_card = 'J': Jsuit           J

        2nd move:
        ---------
        general rule:                rank
        if stack_card = '6': suit     '6'
        if stack_card = 'J':          'J'
        '''

        # 1st move:
        if not deck.cards_played:
            if stack_card.rank == 'J':
                for card in self.cards:
                    if card.suit == jchoice.get_j_suit() or \
                       card.rank == 'J':
                        self.possible_cards.append(card)
            else:
                for card in self.cards:
                    if card.rank == stack_card.rank or \
                       card.suit == stack_card.suit or \
                       card.rank == 'J':
                        self.possible_cards.append(card)
        # 2nd move
        if deck.cards_played:
            if stack_card.rank == '6':
                for card in self.cards:
                    if card.rank == stack_card.rank or \
                       card.suit == stack_card.suit or \
                       card.rank == 'J':
                        self.possible_cards.append(card)
            elif stack_card.rank == 'J':
                for card in self.cards:
                    if card.rank == 'J':
                        self.possible_cards.append(card)
            else:
                for card in self.cards:
                    if card.rank == stack_card.rank:
                        self.possible_cards.append(card)
        return self.possible_cards

    def toggle_possible_cards(self):
        if self.possible_cards:
            card = self.possible_cards.pop()
            self.cards.remove(card)
            self.cards.insert(0, card)
            self.possible_cards.insert(0, card)


class Player:
    ''' The player - human or robot '''

    def __init__(self, name, is_robot):
        self.name = name
        self.is_robot = is_robot
        self.hand = Handdeck()
        self.score = 0

    def __lt__(self, other):
        if self.score < other.score:
            return True
        return False

    def __gt__(self, other):
        if self.score > other.score:
            return True
        return False

    def draw_new_cards(self):
        self.hand.__init__()

        for card in range(5):
            self.hand.cards.append(deck.blind.pop())

    def show(self):
        self.show_possible_cards()
        self.show_hand(True)

    def show_hand(self, visible=False):
        if self.is_robot:
            self.hand.arrange_hand_cards()
        cards = ''
        for card in self.hand.cards:
            if visible:
                cards += str(card)
            else:
                cards += '## '
        if visible:
            print(f'{self.name} holds ({len(self.hand.cards)}) card(s) '
                  f'[{self.hand.count_points():2d} points]:')
        else:
            print(f'{self.name} holds ({len(self.hand.cards)}) card(s):')
        print(cards)

    def show_possible_cards(self):
        cards = ''
        self.hand.get_possible_cards()
        for card in self.hand.possible_cards:
            cards += str(card)
        print(f'{self.name} has played ({len(deck.cards_played)}) card(s) / '
              f'drawn ({len(self.hand.cards_drawn)}) card(s) '
              f'and can play ({len(self.hand.possible_cards)}) card(s):')
        print(cards)

    def draw_card_from_blind(self, cards=1):
        for card in range(cards):
            card = deck.card_from_blind()
            self.hand.cards.append(card)
            self.hand.cards_drawn.append(card)

    def is_must_draw_card(self):
        '''
        must draw card, if:
        ---------------------------------
         card   possible  card    pull  next player
        played    card    drawn   card  possible
            1       1       1       N       Y
            1       1       0       N       Y
            1       0       1       N       Y
            1       0       0       N       Y
            0       1       1       N       N
            0       1       0       N       N
            0       0       1       N       Y
            0       0       0       Y       N   <-- must draw card
        '6' on stack:
        -------------
            1       0       1       Y       N   <-- must draw card
        '''

        stack_card = deck.get_top_card_from_stack()
        if stack_card.rank == '6' and not self.hand.possible_cards:
            return True
        if not deck.cards_played and \
           not self.hand.possible_cards and \
           not self.hand.cards_drawn:
            return True
        return False

    def play_card(self, is_initial_card=False):
        if not self.is_robot:
            self.hand.arrange_hand_cards()
        if is_initial_card:
            card = self.hand.cards.pop()
            deck.put_card_on_stack(card)
        elif not is_initial_card and self.hand.possible_cards:
            card = self.hand.possible_cards.pop()
            self.hand.cards.remove(card)
            deck.put_card_on_stack(card)
            jchoice.clear_j()

    def set_robot(self, is_robot=False):
        self.is_robot = is_robot

    def is_robot(self):
        return self.is_robot

    def auto_play(self):
        ''' Card 'flow' when robots play '''
        # self.hand.arrange_hand_cards()
        while self.hand.possible_cards:
            self.play_card()
            self.hand.get_possible_cards()
        while self.is_must_draw_card():
            self.draw_card_from_blind()
            self.hand.get_possible_cards()


class Bridge:
    ''' A Classic Card Game for 2-4 Players '''

    def __init__(self, number_of_players=None, is_robot_game=None):

        self.number_of_games = 0
        self.number_of_rounds = 0
        self.player_list = []
        self.player = None
        self.shuffler = None

        if not number_of_players:
            while True:
                try:
                    num = input("Enter number of players (2-4):")
                    self.number_of_players = int(num)
                except ValueError:
                    print('Valid number, please')
                    continue
                if 2 <= self.number_of_players <= 4:
                    print(f'\nGame with {self.number_of_players} players')
                    break
                print('Please enter value between 2 and 4')
        else:
            self.number_of_players = number_of_players

        if not is_robot_game:
            while True:
                try:
                    robot = input("Play against Robots (y)es or (n)o:")
                    if robot == 'n':
                        self.is_robot_game = False
                        print(f'\nYou play all {self.number_of_players - 1} '
                              f'players yourself')
                    elif robot == 'y':
                        self.is_robot_game = True
                        print(
                            f'\nYou play against {self.number_of_players - 1} '
                            f'robot(s)!')
                    else:
                        continue
                except ValueError:
                    print('Valid input, please')
                    continue
                print(f"\n{25 * ' '}Press 'enter' to start")
                keyboard.wait('enter')
                break
        else:
            self.is_robot_game = is_robot_game
        try:
            os.remove(f'{date.today()}_scores.txt')
        except OSError as e:
            print('no scorelist found', e)

    @classmethod
    def rules(cls):

        print(f'''
        {30 * " "}Game of Bridge

        Rules Of The Game:
        ------------------
        Bridge is played with 36 cards (4 suits and ranks from 6 to Ace)
        by 2-4 players. Each player starts with 5 cards. The first player
        puts a card onto the stack and can add more cards with same rank.
        The next player can play first card either same suit or same rank
        and can play more cards with same rank. At first the cards on hand
        must be used and at least 1 card must be played. If the player
        does not have a suitable card - a card must be drawn from blind.
        This card may be played if it fits to the card on stack or the
        next player continues. No more than one card can be drawn from blind,
        except a '6' on the stack must be covered.

        Special Cards:
        --------------
        6   must be covered by same player, may be by drawing cards from
            blind until the '6' is covered by a different rank.
        7   next player must draw 1 card from blind
        8   the next player must draw 2 cards and will be passed over.
            When multiple '8' were played either next player must draw
            2 for each '8' on stack and will be passed over - or the
            following players must draw 2 cards and will be passed over
        J   can be played to any suit and player can choose which suit
            must follow
        A   next player will be passed over. With multiple 'A' the next
            players will be passed over

        Special Rule 'Bridge':
        ----------------------
        If there are the same 4 cards in a row on the stack, the player
        of the 4th card can choose whether or not to finish the actual
        round.

        Counting:
        ---------

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

        If a player finishes a round with a 'J'
        - his score will either be reduced by 20
          for each 'J' of his last move - or
        - the scores of the other players will be increased by 20
          for each 'J' of his last move.
        The winner of the current round decides which rule will apply.

        If a player reaches exactly 125 points, his score is back on 0.

        When the blind was empty and therefor the stack was reshuffeled,
        the points of this round are doubled (trippled, ...).
        This also applies to the 'J'-rule mentioned before.

        The player with the highest score starts the next round.

        The round is over once a player reaches more than 125 points.

        During the game you can play several rounds.

        ''')

    def start_game(self):
        # if self.is_server or not self.is_online:
        self.number_of_games += 1
        self.number_of_rounds = 0
        self.player_list.clear()

        for player in range(self.number_of_players):
            self.player_list.append(
                Player(f'Player-{player + 1}', self.is_robot_game))

        self.player_list[0].is_robot = False

        self.start_round()

    def start_round(self):
        self.number_of_rounds += 1

        deck.__init__()

        for player in self.player_list:
            player.draw_new_cards()

        self.player = self.set_shuffler()
        self.player.play_card(is_initial_card=True)
        self.play()

    def set_shuffler(self):
        if self.shuffler is None:
            self.shuffler = self.player_list[0]
        else:
            self.shuffler = max(self.player_list)
            # Shuffler must be set to playerlist[0]
            while self.shuffler != self.player_list[0]:
                self.cycle_playerlist()

        return self.shuffler

    def cycle_playerlist(self):
        self.player_list.append(self.player_list.pop(0))
        self.player = self.player_list[0]

    def activate_next_player(self):
        sevens = 0
        eights = 0
        aces = 0
        key = 'n'

        self.show_full_deck()

        for card in deck.cards_played:
            if card.rank == '7':
                sevens += 1
            elif card.rank == '8':
                eights += 1
            elif card.rank == 'A':
                aces += 1

        if eights >= 2:
            if self.player.is_robot:
                key = random.choice(['a', 'n'])
                if key == 'a':
                    print(f'\n{22 * " "}{self.player.name} says:')
                    print(f"{21 * ' '}You share the 8's")
                    print(f'{21 * " "}|     SPACE    |\n')
                elif key == 'n':
                    print(f'\n{22 * " "}{self.player.name} says:')
                    print(f"{18 * ' '}All 8's for next player")
                    print(f'{21 * " "}|     SPACE    |\n')
                keyboard.wait('space')
            else:
                print(f"\n{13 * ' '}? ? ? How to share the 8's ? ? ?\n")
                print(f'{13 * " "}| (n)ext player | (a)ll players |\n')
                key = keyboard.read_hotkey(suppress=False)

        self.player.hand.cards_drawn.clear()
        self.cycle_playerlist()
        deck.cards_played.clear()

        for card in range(sevens):
            self.player.draw_card_from_blind()
            self.player.hand.cards_drawn.clear()

        if eights and key == 'n':
            for eight in range(eights):
                self.player.draw_card_from_blind(2)
                self.player.hand.cards_drawn.clear()
            self.cycle_playerlist()

        if eights and key == 'a':
            leap = 1
            while leap <= eights:
                if leap != self.number_of_players:
                    self.player.draw_card_from_blind(2)
                    self.player.hand.cards_drawn.clear()
                    self.cycle_playerlist()
                else:
                    self.cycle_playerlist()
                    eights += 1
                leap += 1

        if aces:
            leap = 1
            while leap <= aces:
                if leap != self.number_of_players:
                    self.cycle_playerlist()
                else:
                    self.cycle_playerlist()
                    aces += 1
                leap += 1

    def show_full_deck(self):
        print(f'\n{84 * "-"}\n')
        self.show_all_players(deck.is_visible)
        deck.show()

        self.player.show()
        '''
        for player in self.player_list:
            if player.name == 'Player-1':
                player.show()
        '''
        print(f'\n'
              f'\n{7 * " "}| TAB: toggle |  SHIFT: put  |  ALT: draw  |'
              f'\n{7 * " "}|            SPACE: next Player            |'
              f'\n{7 * " "}|  (s)cores   |   (r)ules    |   (q)uit    |')

    def make_choice_for_J(self):
        if self.player.is_robot:
            jchoice.j = jchoice.js[random.randint(0, 3)]
        else:
            jchoice.j = jchoice.js[-1]
            self.show_full_deck()
            while True:
                jkey = keyboard.read_hotkey(suppress=False)
                if jkey == 'tab':
                    jchoice.toggle_js()
                    jchoice.j = jchoice.js[-1]
                    self.show_full_deck()
                if jkey == 'space':
                    break

    def show_all_players(self, is_visible=False):
        for player in sorted(self.player_list, key=lambda p: p.name):
            if player == self.player:
                player.show_hand(True)
            else:
                player.show_hand(is_visible)

    def finish_round(self):
        print(
            f'\n\n{7 * " "}| * * * {self.player.name} has won this round! * * * |\n')

        # evaluate the points for J on stack:
        if deck.get_top_card_from_stack().rank == 'J':
            if self.player.is_robot:
                key = random.choice(['m', 'p'])
                if key == 'm':
                    print(f'\n{22 * " "}{self.player.name} says:')
                    print(f"{25 * ' '}minus for me")
                    print(f'{21 * " "}|     SPACE    |\n')
                elif key == 'p':
                    print(f'\n{22 * " "}{self.player.name} says:')
                    print(f"{19 * ' '}plus for the others")
                    print(f'{21 * " "}|     SPACE    |\n')
                keyboard.wait('space')
            else:
                print(f"\n{13 * ' '}? ? ? minus or plus for J ? ? ?\n")
                print(f'{7 * " "}|  (m)inus for me | (p)lus for the others  |\n')
                key = keyboard.read_hotkey(suppress=False)
            # consider previous player has played 'J'
            # or active player has played '6' + 'J'
            self.player.score -= 20 * \
                min(len(deck.cards_played), len(
                    deck.bridge_monitor)) * deck.shufflings
            if key == 'p':
                for player in self.player_list:
                    player.score += 20 * \
                        min(len(deck.cards_played), len(deck.bridge_monitor)) * \
                        deck.shufflings

        # evaluate cards_played of last round:
        self.activate_next_player()
        print('\n')
        for player in self.player_list:
            player.score += player.hand.count_points() * deck.shufflings
            if player.score == 125:
                player.score = 0
        self.show_all_players(True)

        try:
            f = open(f'{date.today()}_scores.txt')
        except IOError:
            f = open(f'{date.today()}_scores.txt', 'a')
            f.write(f'\n\n{9 * " "}Game - Round   ')
            for player in sorted(self.player_list, key=lambda p: p.name):
                f.write(f'{player.name} ')
            f.write('\n')
        finally:
            f.close()
            with open(f'{date.today()}_scores.txt', 'a') as f:
                f.write(f'{11 * " "}{self.number_of_games:2d} -'
                        f'{self.number_of_rounds:2d}{7 * " "}')
                for player in sorted(self.player_list, key=lambda p: p.name):
                    f.write(" {:4d}    ".format(player.score))
                f.write(f'{4 * " "}{(deck.shufflings - 1) * " *"}\n')

        self.show_scores()

        self.set_shuffler()

        if self.shuffler.score <= 125:
            print(
                f'\n  {13 * " "}{self.shuffler.name} will start next round\n')
            print(f'{21 * " "}|     SPACE    |\n')
            keyboard.wait('space')
            self.start_round()
        else:
            print(f'\n{6 * " "}The Winner is ...\n')
            print(f'{24 * " "}{min(self.player_list).name}\n')
            # winner = sorted(self.player_list,
            # key=lambda player: player.score, reverse=True).pop()
            print(f'{14 * " "}+ + + G A M E  O V E R + + + \n')
            print(f'{21 * " "}| (n)ew game |\n')
            keyboard.wait('n')
            self.start_game()

    def show_scores(self):
        try:
            with open(f'{date.today()}_scores.txt') as f:
                print(f.read())
        except IOError:
            print(f'\n\n{6 * " "}'
                  f'Playing 1st round - No score list availabe yet\n')

    def check_if_bridge(self):
        if len(deck.bridge_monitor) == 4:

            self.show_full_deck()

            print(f'\n{17 * " "}* * * B R I D G E * * *\n')

            if self.player.is_robot:
                if self.player.hand.count_points() == 0:
                    key = 'y'
                elif self.player.hand.count_points() >= 25:
                    key = 'n'
                else:
                    key = random.choice(['n', 'y'])
                if key == 'n':
                    print(f'{22 * " "}{self.player.name} says:')
                    print(f"{16 * ' '}Let's continue this round")
                    print(f'{21 * " "}|     SPACE    |\n')
                    deck.bridge_monitor.clear()
                    keyboard.wait('space')
                    return False
                elif key == 'y':
                    print(f'{22 * " "}{self.player.name} says:')
                    print(f'{17 * " "}YES - count your points!')
                    print(f'{21 * " "}|     SPACE    |\n')
                    keyboard.wait('space')
                    return True
            else:
                print(f'{22 * " "}|  Y  |  N  |\n')
                key = keyboard.read_hotkey(suppress=False)
            if key == 'n':
                deck.bridge_monitor.clear()
                return False
            if key == 'y':
                return True
        else:
            return False

    def is_next_player_possible(self):
        if self.check_if_bridge():
            self.finish_round()
            return False

        if deck.get_top_card_from_stack().rank == '6':
            return False

        if not self.player.hand.cards:
            self.show_full_deck()
            # print(f'\n\n{7 * " "}\
            # | * * * {self.player.name} has won this round! * * * |\n')
            keyboard.wait('space')
            self.finish_round()
            return True

        if deck.get_top_card_from_stack().rank == 'J':
            if deck.cards_played:
                self.make_choice_for_J()
                return True

            '''
            next player possible, (except 6 on stack) if:

                 card   possible  card    next
                played    card    drawn   player
                        1       1       1       Y
                        1       1       0       Y
                        1       0       1       Y
                        1       0       0       Y
                        0       1       1       N
                        0       1       0       N
                        0       0       1       Y
                        0       0       0       N       <-- must draw card
                       0/1     0/1     0/1      N       <-- & when '6'
            '''

        if deck.cards_played:
            return True

        if not deck.cards_played:
            if not self.player.hand.possible_cards and \
               self.player.hand.cards_drawn:
                return True
            return False

    def play(self):
        while True:

            self.show_full_deck()

            if self.player.is_robot:
                while not self.is_next_player_possible() or \
                        self.player.hand.possible_cards:
                    self.player.auto_play()
                key = keyboard.read_hotkey(suppress=False)
                if key == 'space':
                    self.activate_next_player()

            else:
                key = keyboard.read_hotkey(suppress=False)

                if key == 'tab':
                    self.player.hand.toggle_possible_cards()
                elif key == 'shift':
                    self.player.play_card()
                elif key == 'alt' and self.player.is_must_draw_card():
                    self.player.draw_card_from_blind()
                elif key == 'space' and self.is_next_player_possible():
                    self.activate_next_player()

                elif key == 's':
                    self.show_scores()
                    print(f'{21 * " "}|     SPACE    |\n')
                    keyboard.wait('space')
                elif key == 'r':
                    Bridge.rules()
                    print(f'{21 * " "}|     SPACE    |\n')
                    keyboard.wait('space')
                elif key == 'q':
                    break

                elif key == 'ctrl+v':
                    if deck.is_visible:
                        deck.is_visible = False
                    else:
                        deck.is_visible = True
                elif key == 'ctrl+r':
                    self.start_round()
                elif key == 'ctrl+6':
                    for suit in suits:
                        self.player.hand.cards.append(Card(suit, '6'))
                elif key == 'ctrl+7':
                    for suit in suits:
                        self.player.hand.cards.append(Card(suit, '7'))
                elif key == 'ctrl+8':
                    for suit in suits:
                        self.player.hand.cards.append(Card(suit, '8'))
                elif key == 'ctrl+j':
                    for suit in suits:
                        self.player.hand.cards.append(Card(suit, 'J'))
                elif key == 'ctrl+a':
                    for suit in suits:
                        self.player.hand.cards.append(Card(suit, 'A'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("bridge",
                                     description=Bridge.rules())
    parser.add_argument("--number_of_players", "-p",
                        type=int, choices=[2, 3, 4], help="number of players")
    parser.add_argument("--is_robot_game", "-r",
                        type=bool, choices=[True], help="play against robots")
    try:
        args = parser.parse_args()
    except AttributeError:
        parser.print_help()
        parser.exit()

    bridge = Bridge(args.number_of_players, args.is_robot_game)
    bridge.start_game()

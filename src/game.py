from numpy.random import randint
from icecream import ic

class Game():

    def __init__(self, players):
        """This method nitializes the game with a random player starting, and rolls the dice for all players."""
        self.players = players
        self.game_over = False
        self.active_players = len(players)
        self.bids = []
        self.n_dice = [5 for i in range(len(players))]
        self.current_player = self.players[randint(len(self.players))]
        print("Player {} is starting.".format(self.current_player.index))
        self.previous_player = None
        self.roll_dice()
        self.play_game(players)

    def play_game(self, players):
        while not self.game_over:
            move = self.current_player.move(self.bids, self.dice[self.current_player.index], self.n_dice)
            self.execute_move(move)
        print("Player {} wins.".format(self.current_player.index))

    def roll_dice(self):
        """The role dice method takes a list of integers representing the number of dice each player has
            and returns a list of lists where each list has the corresponding number of pseudo-random integers."""
        print("Rolling dice for all players.")
        self.dice = [list(randint(low=1,high=7, size=i)) for i in self.n_dice]

    def get_actual(self, value):
        """This method finds the actual number of dice of a given value on the table."""
        actual = sum([sum([x == value or x == 6 for x in cup]) for cup in self.dice])
        print("There are {} {}s on the table.".format(actual, value))
        return actual

    def eval_bid(self, bid):
        """This method returns the difference between the number of dice of the value bid on the table and the quantity bid."""
        (quantity, value) = bid
        return self.get_actual(value) - quantity

    def is_valid_challenge(self, move):
        """This method checks is a move is a valid challenge."""
        return (type(move) == str) and any(self.bids) and (move == "Liar" or move == "Spot on, lose two" or (move == "Spot on, gain one" and self.n_dice[self.current_player.index] < 5))

    def is_valid_bid(self, move):
        """This method checks if a move is a valid bid."""
        if type(move) == tuple:
            if any(self.bids):
                if move[1] == 6:
                    current_bid_value = move[0] * 2
                else:
                    current_bid_value = move[0]

                if self.bids[-1][1] == 6:
                    previous_bid_value = self.bids[-1][0] * 2
                else:
                    previous_bid_value = self.bids[-1][0]
                if current_bid_value > previous_bid_value and (move[1] >= 1 and move[1] <= 6):
                    return True
                else:
                    print("Bid too low.")
                    return False
            elif move[0] >= 1 and (move[1] >= 1 and move[1] <= 6):
                return True
        else:
            return False

    def execute_move(self, move):
        """Executes the move submitted by the player."""
        if self.is_valid_bid(move):
            self.execute_bid(move)
        elif self.is_valid_challenge(move):
            self.execute_challenge(move)
        else:
            print("Player says '{}', but '{}' is an invalid move. Player {} disqualified.".format(move, move, self.current_player.index))
            self.n_dice[self.current_player.index] = 0
            self.active_players -= 1
            self.current_player = self.get_next_player()
        

    def execute_challenge(self, challenge):
        """This method evaluates the consequences of a player challenging."""
        print("Player {} calls '{}'.".format(self.current_player.index, challenge))
        value = self.eval_bid(self.bids[-1])
        if challenge == "Liar":
            if value >= 0:
                self.lose_dice(self.current_player, 1)
                self.current_player = self.get_next_player()
            else:
                self.lose_dice(self.previous_player, 1)
        elif challenge == "Spot on, lose two":
            if value == 0:
                self.lose_dice(self.previous_player, 2)
            else:
                self.lose_dice(self.current_player, 1)
                self.current_player = self.get_next_player()
        else:
            if value == 0:
                print("Player {} gains a die.".format(self.current_player.index))
                self.n_dice[self.current_player.index] += 1
            else:
                self.lose_dice(self.current_player, 1)
                self.current_player = self.get_next_player()
                
        if not self.game_over:
            print("New round. Player {} starting".format(self.current_player.index))
            self.roll_dice()
            self.bids = []

    def execute_bid(self, bid):
        """This method appends the playes bid to the bids structure and moves to the next player."""
        self.bids.append(bid)
        print("Player {} bids {} {}s.".format(self.current_player.index, *bid))
        self.previous_player = self.current_player
        self.current_player = self.get_next_player()
        
    def get_next_player(self):
        """This method returns the next player with remaining dice."""
        current_index = self.current_player.index
        while True:
            if self.n_dice[(current_index + 1) % len(self.players)] > 0:
                return self.players[(current_index + 1) % len(self.players)]
            else:
                current_index += 1

    def lose_dice(self, player, number):
        """This method subtrcts the given number of dice from a player."""
        if min(self.n_dice[player.index], number) == 1:
            print("Player {} loses a die.".format(player.index))
        else:
            print("Player {} loses two dice.".format(player.index, min(self.n_dice[player.index], number)))
        self.n_dice[player.index] -= min(self.n_dice[player.index], number)
        print("Player {} now has {} dice left.".format(player.index, self.n_dice[player.index]))
        if self.n_dice[player.index] == 0:
            print("Player {} is out.".format(player.index))
            self.active_players -= 1
        if not self.active_players > 1:
            self.game_over = True
    
from player import Player

class Believer(Player):
    """The Believer class implements a player who always believes the previous player to be exactly right."""

    def move(self, bid, dice):
        """The move method returns 'Spot on' if bid is not empty and '1,1' otherwise."""
        if bid:
            return 'Spot on'
        else:
            return '1,1'
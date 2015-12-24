"""Abstract classes. Your classes must inherit from these.
"""
import abstract

class AbstractSelectivePlayer(abstract.AbstractPlayer):
    """Your player must inherit from this class, and your player class name must be 'Player', as in the given examples.
Like this: 'class Player(abstract.AbstractPlayer):'
    """
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        """Player initialization.

        :param setup_time: Allowed setup time in seconds, float.
        :param player_color: A String representing this player's color.
        :param time_per_k_turns: Allowed move calculation time per k turns.
        :param k: The k above.
        """
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)

        self.w = self.get_w()

    def get_w(self):
        """Get the w paramter that determines the number of child nodes to select.

        :return: The value of w.
        """
        raise NotImplementedError

    def subset_selection(self, state, w, possible_moves):
        """Select a subset of the possible moves using the w parameter and some heuristic

        :param state: the current state
        :param w: The percent of possible moves to select
        :param possible_moves: The possible moves for the next move
        :return: a subset of the possible moves using the w parameter
        """
        raise NotImplementedError
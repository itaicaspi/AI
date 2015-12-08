"""A generic turn-based game runner.
"""
# from __future__ import print_function
import sys
import amazons_board
import utils
import copy
import players.interactive

WHITE_PLAYER = 'white'
BLACK_PLAYER = 'black'

TIE = 'tie'

class amazonsRunner:
    def __init__(self, setup_time, time_per_k_turns, k, printPref, white_player, black_player):
        """Game runner initialization.

        :param setup_time: Setup time allowed for each player in seconds.
        :param time_per_k_turns: Time allowed per k moves in seconds.
            The interactive player always gets infinite time to decide, no matter what.
        :param k: The k turns we measure time on. Must be a positive integer.
        :param printPref: preference of printing the board each turn. 'y' - yes, print. 'n' - no,  don't print.
        :param white_player: The name of the module containing the white player. E.g. "myplayer" will invoke an
            equivalent to "import players.myplayer" in the code.
        :param black_player: Same as 'white_player' parameter, but for the black one.
        """

        self.printPref = printPref.lower()
        self.setup_time = float(setup_time)
        self.time_per_k_turns = float(time_per_k_turns)
        self.k = int(k)
        self.players = []

        # Dynamically importing the players. This allows maximum flexibility and modularity.
        self.white_player = 'players.{}'.format(white_player)
        self.black_player = 'players.{}'.format(black_player)
        __import__(self.white_player)
        __import__(self.black_player)
        white_is_interactive = sys.modules[self.white_player].Player == players.interactive.Player
        black_is_interactive = sys.modules[self.black_player].Player == players.interactive.Player
		
        self.remaining_times = [
            utils.INFINITY if white_is_interactive else self.time_per_k_turns,
            utils.INFINITY if black_is_interactive else self.time_per_k_turns,
        ]

    def setup_player(self, player_class, player_color):
        """ An auxiliary function to populate the players list, and measure setup times on the go.

        :param player_class: The player class that should be initialized, measured and put into the list.
        :param player_color: Player color, passed as an argument to the player.
        :return: A boolean. True if the player exceeded the given time. False otherwise.
        """
        try:
            player, measured_time = utils.run_with_limited_time(
                player_class, (self.setup_time, player_color, self.time_per_k_turns, self.k), {}, self.setup_time*1.5)
        except MemoryError:
            return True

        self.players.append(player)
        return measured_time > self.setup_time

    def run(self):
        """The main loop.
        :return: The winner.
        """

        white_player_exceeded = self.setup_player(sys.modules[self.white_player].Player, WHITE_PLAYER)
        black_player_exceeded = self.setup_player(sys.modules[self.black_player].Player, BLACK_PLAYER)
        winner = self.handle_time_expired(white_player_exceeded, black_player_exceeded)
        if winner:
            return winner

        board_state = amazons_board.amazonsBoard()
        curr_player_idx = 0

        remaining_run_times = self.remaining_times[:]
        k_count = 0

        # Running the actual game loop. The game ends if someone is left out of moves,
        # or exceeds his time.
        while True:
            if self.printPref == 'y':
                board_state.printBoard()

            player = self.players[curr_player_idx]
            remaining_run_time = remaining_run_times[curr_player_idx]
            try:
                possible_moves = board_state.legalMoves()
                if not possible_moves:
                    winner = self.make_winner_result(0 if curr_player_idx == 1 else 1)
                    break
                move, run_time = utils.run_with_limited_time(
                    player.get_move, (copy.deepcopy(board_state), possible_moves), {}, remaining_run_time*1.5)
                remaining_run_times[curr_player_idx] -= run_time
                if remaining_run_times[curr_player_idx] < 0:
                    raise utils.ExceededTimeError
            except (utils.ExceededTimeError, MemoryError):
                print('Player {} exceeded resources.'.format(player))
                winner = self.make_winner_result(0 if curr_player_idx == 1 else 1)
                break

            board_state.doMove(move)
            if self.printPref == 'y':
                print('Player ' + repr(player) + ' performed the move: ' + repr(move))
            curr_player_idx = (curr_player_idx + 1) % 2

            if curr_player_idx == 0:
                # White and black played.
                k_count = (k_count + 1) % self.k
                if k_count == 0:
                    # K rounds completed. Resetting timers.
                    remaining_run_times = self.remaining_times[:]

        self.end_game(winner)
        return winner

    @staticmethod
    def end_game(winner):
        print('The winner is {}'.format(winner[0]))

    def make_winner_result(self, idx):
        if idx < 0:
            return TIE, TIE

        if idx == 0:
            return self.players[0], WHITE_PLAYER

        return self.players[1] if len(self.players) > 1 else BLACK_PLAYER, BLACK_PLAYER

    def handle_time_expired(self, white_player_exceeded, black_player_exceeded):
        winner = None
        if white_player_exceeded and black_player_exceeded:
            winner = self.make_winner_result(-1)
        elif white_player_exceeded:
            winner = self.make_winner_result(1)
        elif black_player_exceeded:
            winner = self.make_winner_result(0)

        if winner:
            self.end_game(winner)

        return winner


if __name__ == '__main__':
    try:
        amazonsRunner(*sys.argv[1:]).run()
    except TypeError:
        print("""Syntax: {0} setup_time time_per_k_turns k printPref white_player black_player
For example: {0} 3 3 3 y interactive random_player
Please read the docs in the code for more info.""".
              format(sys.argv[0]))
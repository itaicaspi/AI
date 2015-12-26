from run_amazons import amazonsRunner

players_scores = dict()
players = ['simple_player', 'selective_alpha_beta_0.5', 'selective_alpha_beta_0.25', 'selective_alpha_beta_0.125']

for player in players:
    players_scores[player] = 0

for k in [2, 10, 50]:
    for player1 in players:
        for player2 in players:
            if player1 == player2:
                continue
            winner_color = amazonsRunner(2, k, 5, 'n', player1, player2).run()
            if winner_color == 'white':
                winner = player1
            elif winner_color == 'black':
                winner = player2

            players_scores[winner] += 1
            print(k + ', ' + player1 + ', ' + player2 + ', ' + winner)
            amazonsRunner(2, k, 5, 'n', player2, player1).run()
            if winner_color == 'white':
                winner = player1
            elif winner_color == 'black':
                winner = player2

            players_scores[winner] += 1
            print(k + ', ' + player1 + ', ' + player2 + ', ' + winner)
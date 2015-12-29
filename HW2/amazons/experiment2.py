from run_amazons import amazonsRunner

players_scores = dict()
players = ['simple_player', 'selective_alpha_beta_k', 'upgraded_simple_player', 'selective_alpha_beta_0_125']
f = open('exp1_res_k2.txt', 'w')
for player in players:
    players_scores[player] = 0

for k in [2, 10]:
    f.write('k is' + str(k) + '\n')
    for player1 in players:
        for player2 in players:
            if player1 == player2:
                continue
            winner_color = amazonsRunner(2, k, 5, 'n', player1, player2).run()
            winner = 'tie'
            if winner_color[1] == 'white':
                winner = player1
                players_scores[winner] += 1
            elif winner_color[1] == 'black':
                winner = player2
                players_scores[winner] += 1

            f.write('k: ' + str(k) + ', player1: ' + player1 + ', player2:' + player2 + ', winner:' + winner+ '\n')

    for player in players:
        f.write('for player: ' + player + 'score is: ' + str(players_scores[player]) + '\n')
        players_scores[player] = 0

f.close()
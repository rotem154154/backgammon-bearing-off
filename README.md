# backgammon-bearing-off
This project allows you get statistics about bearing off board (when all checkers in home board)
* show the best move for given board and dice
* show the average amount of moves until win
* show the precent to win against another player

#### What I implemented for this project:
* Dynamic algorithm to calculate the best move for any board
* Simulate random games from given board to get average amount of moves to win
* Create dataset of random boards competing with each others to see the precent of each player to win under random dice.
* create regression neural network to show the win percentage for any two given boards


the neural net model can predict the percentage of the player to win in less then 1% accuracy.
the input for the neural net can be either the two boards or the amount of movements for each player.

<img src="https://github.com/rotem154154/backgammon-bearing-off/blob/main/backgammon_stats.jpg" width="400">



<p>
<img src="https://github.com/rotem154154/backgammon-bearing-off/blob/main/2_players_winner_plot.png">
The horizontal axis is the amount of movements needed by player 1 to win.<br />
The vertical axis is the amount of movements needed by player 2 to win.<br />
The color of the dots changes from blue to red if player 1 has more chances to win.</p>

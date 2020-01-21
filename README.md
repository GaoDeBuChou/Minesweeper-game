# Minesweeper

This game is similar as the Minesweeper game in previous _Windows_ editions, with three difficulty levels: Easy, Normal, Hard.

To play this game, make sure you have installed the site-package "pygame" by running `pip install pygame` or `pip install -r requirements.txt` command under the project directory. Then, run `python sweeper.py` command under the project directory.

The followings are valid actions:
1. Left click on a grey empty position with no flag or question mark to expand the position.
2. Right click on a grey position to add a flag, or change the flag to a question mark, or remove the question mark.
3. Double click (both left and right click) on a white position with number to expand all surrounding non-flag positions if the number of surrounding flags is the same as the number indicated by the position; double click is invalid if the number does not match.

If a position with bomb is expanded, then you lose. If all non-bomb positions are expanded and shown, then you win. The game restarts if you left click on any position after winning or losing, or if you change difficulty level.

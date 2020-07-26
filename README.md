# Building a Chess AI

In this project I use the minimax algorithm with alpha-beta pruning to create a Chess AI that can play
against a human. The code is written in Python using the [python-chess](https://python-chess.readthedocs.io/en/latest/) library.

### Usage
On your local machine, clone the repository by typing:
```console
git clone https://github.com/Ajay-Chopra/chess-ai.git
```
In order to run the program, you will need to have python-chess installed. This can be done with:
```console
pip install python-chess
```
Once you have the necessary libraries installed run the program with the following commands:
```console
cd chess-ai
python chess_ai.py
```
You should see a starting chess board and a welcome message:
```console
WELCOME TO CHESS
---------------------------------------------------------------------
Enter moves in the form: r1f1r2f2
For example if you wanted to move from F2 to F3 you would type f2f3
---------------------------------------------------------------------
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
---------------------------------------------------------------------
Please enter a move. Type DONE when finished
```
By default you are playing as the uppercase pieces. Simply enter your move and the program should handle it from there!

##### Using the Jupyter Notebook
If you desire a more elaborate chessboard representation and you have jupyterlab installed, you can use the
chess.ipynb file. We can use an SVG component to display the board like so:




![Chess Board Image](assets/1_nH4AerChS2uPEy4igMIshw.png)



### Theory
In order to create my chess AI, I utilize both a board evaluation algorithm and a search algorithm. 
Board evaluation is based on first valuing the total "material" a player has on the board (i.e. assigning weights
to each piece and calculating a player's total material by summing all the pieces multiplied by their weights).
The second step is evaluating the positions of the pieces. This is done using piece-square tables. If you would like 
to know more about how weights and piece-square tables are calculated you can visit this [link](https://www.chessprogramming.org/Piece-Square_Tables).

In order to search for the best move among all possible choices, I use the minimax algorithm with alpha-beta pruning. 
More information on the algorithm can be found on [Wikipedia](https://en.wikipedia.org/wiki/Minimax).

### Next Steps
Future plans for this project center around assigning better weights to pieces and creating more accurate piece-square tables.
In order to do this, I will need to extensively test my program to measure its performance. Some have used [Stockfish](https://stockfishchess.org/) 
for this purpose. I would also like to take a look at improving the search algorithm so that it is not constrained by a certain depth, 
a problem often referred to as the [Horizon Effect](https://www.chessprogramming.org/Horizon_Effect). 



























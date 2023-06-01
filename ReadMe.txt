# CNG462 Artificial Intelligence – Assignment 2 

This is a Readme.txt file containing a brief explanation of the code and how to compile it.

About The Code

This is an Othello game implemented in Python using a MiniMax with alpha-beta pruning algorithm. The program asks for a depth which determines the depth of the search. 

Player 2 (O) uses the isOnEdge() function as a heuristic. This heuristic prefers moving to the edges or corners of the board.
If the computer is playing against itself, Player 1 (X) uses the best score heuristic. This heuristic prefers making moves which maximize its score.


How To Compile
This code can be run so that a user can play against the computer, or the computer can play against itself.

To run the program so that the user plays against the computer, use:
>>python othello_ab.py pvc

To run the program so that the computer plays against itself, use:
>>python othello_ab.py cvc

Enter a depth value for the algorithm. Recommended values are 1 - 4. Any higher will cause the search to be very slow.

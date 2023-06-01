import random
import sys 
def drawBoard(board):
    #Prints the board after every move
    h_line = '  +---+---+---+---+---+---+---+---+'    
    v_line = '  |   |   |   |   |   |   |   |   |'
    print('    1   2   3   4   5   6   7   8')
    print(h_line)
    for y in range(8):
        print(v_line)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(v_line)
        print(h_line)

def resetBoard(board):
    # Makes an existing board empty
    # Needs a board to have been created before using this function
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

def newBoard():
    # Creates a brand new, blank board
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

def isValidMove(board, tile, x_coord, y_coord):
    # Checks if Player move is allowable, otherwise returns False
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[x_coord][y_coord] != ' ' or not isOnBoard(x_coord, y_coord):
        return False
    board[x_coord][y_coord] = tile # temporarily set the tile on the board.
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x_coord, y_coord
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # Checks if surrounding pieces belong to opponent
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over
                # Record tiles to flip over while going back to original coordinates
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == x_coord and y == y_coord:
                        break
                    tilesToFlip.append([x, y])
    board[x_coord][y_coord] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScore(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    x_score = 0
    o_score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                x_score += 1
            if board[x][y] == 'O':
                o_score += 1
    return {'X':x_score, 'O':o_score}

def makeMove(board, tile, x_coord, y_coord):
    # Place the tile on the board at x_coord, y_coord, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, x_coord, y_coord)
    if tilesToFlip == False:
        return False
    board[x_coord][y_coord] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    boardCopy = newBoard()
    for x in range(8):
        for y in range(8):
            boardCopy[x][y] = board[x][y]
    return boardCopy

def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 18 will be the bottom-left corner.')
    return [x, y]

def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScore(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScore(mainBoard)
    print('Player 1 has %s points. Player 2 has %s points.' % (scores[playerTile], scores[computerTile]))

print('Welcome to Othello/Reversi!')
while True:
    # Reset the board and game.
    mainBoard = newBoard()
    resetBoard(mainBoard)
    if sys.argv[1]== 'PvC':
        print('You are Player 1 (X). The computer is Player 2 (O). You will go first!')
    elif sys.argv[1] == 'CvC':
        print('Player 1 is X, Player 2 is O. Player 1 will go first!')
    playerTile, computerTile = ['X', 'O']
    print('Player 1 will go first.')
    turn = 'player1'
    while True:
        if turn == 'player1':
            # Player's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            #input('Press Enter to see the Player 1\'s move.')
            if sys.argv[1] == 'CvC':
                move = getComputerMove(mainBoard, playerTile)
            elif sys.argv[1] == 'PvC':
                move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])
            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'player2'
        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            #input('Press Enter to see the Player 2\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)
            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player1'
    # Display the final score.
    drawBoard(mainBoard)
    scores = getScore(mainBoard)
    print('Player 1 (X) scored %s points. Player 2 (O) scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('Player 1 beat Player 2 by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
        break
    elif scores[playerTile] < scores[computerTile]:
        print('Player 1 lost. Player 2 won by %s points.' % (scores[computerTile] - scores[playerTile]))
        break
    else:
        print('The game was a tie!')
        break
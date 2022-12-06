#Hello! Welcome to our project :)

# Source: from inventwithpython.com, buggy programs
# This version of the game has a bug in it. See if you can figure out how to fix it.
# http://inventwithpython.com/pygame/buggy
# Bug Description: When dropping a token on a tall stack, the token appears to drop past the top token on the stack.

# Four-In-A-Row (a Connect Four clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

#Current distribution: (these are assigned with random name selector, feel free to change anything!)
#Part 1 - Juman
#Part 2 - Athena
#Part 3 - Kohinoor
#Part 4 - Iris
#The parts are commented on the source code

# ------- first person starts here ********* Juman

# importing four modules:
#random- used to generate random numbers/moves
#copy- allows to copy lists and use those copies
#sys- access files within system (used to get png files)
#pygame- used to run window
import random, copy, sys, pygame

#importing everything from pygame.locals
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6  # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4  #Board must be at least 4x4

DIFFICULTY = 2  # how many moves to look ahead. (>2 is usually too much)

SPACESIZE = 50  # size of the tokens and individual board spaces in pixels

FPS = 30  # frames per second to update the screen
WINDOWWIDTH = 640  # width of the program's window, in pixels
WINDOWHEIGHT = 480  # height in pixels

#creates an integer with variables specified
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) /
              2)  #width - number of pixels = xmargin along sides
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) /
              2)  #height - number of pixels = ymargin along sides

BRIGHTBLUE = (0, 0, 255)
#change BG colour to green
GRASSGREEN = (127, 255, 0)
WHITE = (255, 255, 255)

BGCOLOR = GRASSGREEN  #backgoround colour
TEXTCOLOR = WHITE  #text colour

#variables for set-up
RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'


def main():
    #makes all variables global which means those variables could be used anywhere in the code
    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
    global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
    global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

    pygame.init()  #initializes pygame
    FPSCLOCK = pygame.time.Clock()  #time clock for pygame, sets up FPS?
    DISPLAYSURF = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT))  #displays window width and height

    pygame.display.set_caption(
        'Four in a Row')  #sets caption to be 'Four in a Row'

    REDPILERECT = pygame.Rect(int(SPACESIZE / 2),
                              WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE,
                              SPACESIZE)  #creating rectangles for collision?
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2),
                                WINDOWHEIGHT - int(3 * SPACESIZE / 2),
                                SPACESIZE, SPACESIZE)
    REDTOKENIMG = pygame.image.load(
        'cat-test-image01.png')  #loads in token for image
    REDTOKENIMG = pygame.transform.smoothscale(
        REDTOKENIMG,
        (SPACESIZE, SPACESIZE))  #transforms image into token size needed
    BLACKTOKENIMG = pygame.image.load(
        '4row_black.png')  #loads in token for image
    BLACKTOKENIMG = pygame.transform.smoothscale(
        BLACKTOKENIMG,
        (SPACESIZE, SPACESIZE))  #transforms image into token size needed
    BOARDIMG = pygame.image.load('4row_board.png')  #loads in board for image
    BOARDIMG = pygame.transform.smoothscale(
        BOARDIMG,
        (SPACESIZE, SPACESIZE))  #transforms image into board size needed

    HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')  #loading image
    COMPUTERWINNERIMG = pygame.image.load(
        '4row_computerwinner.png')  #loading image
    TIEWINNERIMG = pygame.image.load('4row_tie.png')  #loading image
    WINNERRECT = HUMANWINNERIMG.get_rect()  #creates rectangle for image
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
                         )  #creates rectangle for image

    ARROWIMG = pygame.image.load('4row_arrow.png')  #loading image
    ARROWRECT = ARROWIMG.get_rect()  #creates rectangle for image?
    ARROWRECT.left = REDPILERECT.right + 10  #creates rectangle for image?
    ARROWRECT.centery = REDPILERECT.centery  #creates rectangle for image?

    isFirstGame = True  #verifies that it's the first game

    while True:  #turns false after running game the first time
        runGame(isFirstGame)
        isFirstGame = False

def runGame(isFirstGame):
    if isFirstGame:
        # Let the computer go first on the first game, so the player can see how the tokens are dragged from the token piles.
        turn = COMPUTER
        showHelp = True
    else:
        # Randomly choose who goes first.
        if random.randint(0, 1) == 0:
            turn = COMPUTER
        else:
            #after first turn, it'll be false
            turn = HUMAN
        showHelp = False

    # Set up a blank board data structure.
    mainBoard = getNewBoard()  #runs getNewBoard fucntion

    while True:  # main game loop
        if turn == HUMAN:
            # if it's the Human player's turn, it'll run the getHumanMove function
            getHumanMove(mainBoard, showHelp)
            if showHelp:
                # turn off help arrow after the first move
                # help arrow disappears after the first move is made
                showHelp = False
            if isWinner(mainBoard, RED):
                #if Human is the winner, it'll play HUMANWINNERIMG
                winnerImg = HUMANWINNERIMG
                break
            turn = COMPUTER  # switch to other player's turn
        else:
            # Computer player's turn.
            column = getComputerMove(mainBoard)
            animateComputerMoving(mainBoard, column)
            makeMove(mainBoard, BLACK, column)
            if isWinner(mainBoard, BLACK):
                #if Computer is the winner, it'll play COMPUTERWINNERIMG
                winnerImg = COMPUTERWINNERIMG
                break
            turn = HUMAN  # switch to other player's turn

        if isBoardFull(mainBoard):
            # A completely filled board means it's a tie.
            #function   #if all tokens are filled up, it's a tie and it'll display the TIEWINNERIMG
            winnerImg = TIEWINNERIMG
            break

# ------- second person starts here ********* Athena
    while True:
        # the while True loop keep repeating the code inside it until the player clicks the mouse or quits.
        drawBoard(mainBoard)  #create the mainboard
        DISPLAYSURF.blit(
            winnerImg, WINNERRECT
        )  # "blit" stands for Block Transfer, it copy winner image from the source file to the display surface

        pygame.display.update(
        )  # update/refresh the display, make the surface appear on the user's monitor

        FPSCLOCK.tick()  #update the clock once per frame

        #this is a for loop that handles events
        for event in pygame.event.get(
        ):  # for each event that we get from the queue
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP
                                             and event.key == pygame.K_ESCAPE):
                #QUIT happens when the user closes the game window by pressing the [X] button
                #KEYUP means when a key is released, K_ESCAPE is the escape key. So when the user presses the escape key, the game would close
                pygame.quit()  #quit the game, uninitialize pygame modules
                sys.exit()  #exit the system

            elif event.type == MOUSEBUTTONUP:  # MOUSEBUTTONUP is when the mouse button is released (after the player drags token to the top of a stack)
                return  #return and comes out of the function runGame


def makeMove(board, player, column):
    '''
    board (list) - tracking what's on the game board
    player (str) - this differentiates between the human player and the computer
    column (int) - this is the column that the token will be placed on (or attempted to be placed on)
    
    This function determines whether or not the person or the computer can add a token to a column.
    It makes sure that the token is placed at the lowest possible space in the column by using getLowestEmptySpace.
    If there is no space in the column selected by the player, then the variable "lowest" would equal -1, and the move cannot be made. Otherwise, the player's token will be put into the lowest empty space in the selected column.
    '''
    lowest = getLowestEmptySpace(
        board, column
    )  # lowest checking if there is an empty space in that column to fit the token
    if lowest != -1:  #if there is space to fit the token
        board[column][
            lowest] = player  #the lowest row of the selected column of the board will be changed to a token (with the player's colour)


def drawBoard(board, extraToken=None):
    '''
    This function creates the display for the game board. 
    It creates rectangles barriers for the tokens, extra tokens, board image, and token piles.
  
    board (list) - tracking what's on the game board
    extraToken=None - each time the board is drawn, the amount of extra token is reset to zero (another extra token will be generated if the player drags a token from their stack)
    '''
    DISPLAYSURF.fill(BGCOLOR)  #the background colour fills the display screen

    spaceRect = pygame.Rect(
        0, 0, SPACESIZE, SPACESIZE
    )  #create a variable spaceRect to store rectangle coordinates of around each token
    for x in range(BOARDWIDTH):
        for y in range(
                BOARDHEIGHT
        ):  #nested for loops iterating each column and row from the game board
            spaceRect.topleft = (
                XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE)
            )  #fit a rectangle to each space in the columns and rows, use ".topleft" to align them
            if board[x][
                    y] == RED:  #if that space on the board is assigned to a token from the human player
                DISPLAYSURF.blit(
                    REDTOKENIMG, spaceRect
                )  #display the human token image in the rectangle space
            elif board[x][
                    y] == BLACK:  #if that space on the board is assigned to a token from the computer
                DISPLAYSURF.blit(
                    BLACKTOKENIMG, spaceRect
                )  #display the computer token image in the rectangle space

    # when the human player or computer drag a token, an extra token will be created
    if extraToken != None:  #if there should exist an extra token
        if extraToken[
                'color'] == RED:  #if the extra token from the human player
            DISPLAYSURF.blit(
                REDTOKENIMG,
                (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE)
            )  #draw an extra token image to the appropriate location on the display surface
        elif extraToken[
                'color'] == BLACK:  #if the extra token is from the computer
            DISPLAYSURF.blit(
                BLACKTOKENIMG,
                (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE)
            )  #draw an extra token image to the appropriate location on the display surface

    # draw board over the tokens, so that the blue board structure image appears above the tokens
    for x in range(BOARDWIDTH):
        for y in range(
                BOARDHEIGHT
        ):  #nested for loops iterating each column and row from the game board
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE),
                                 YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(
                BOARDIMG, spaceRect
            )  #draw a single square picture of the game board onto each space of the board, and align image with ".topleft"

    # display the starting piles of tokens
    DISPLAYSURF.blit(
        REDTOKENIMG, REDPILERECT
    )  # human player's tokens on the left, at the space of the pile rectangle
    DISPLAYSURF.blit(
        BLACKTOKENIMG, BLACKPILERECT
    )  # computer's tokens on the right, at the space of the pile rectangle


def getNewBoard():
    '''
  This function create a new empty board.
  '''
    board = []  #the board variable is assigned to an empty list
    for x in range(BOARDWIDTH):
        board.append(
            [EMPTY] *
            BOARDHEIGHT)  #add zero for each entry in each column of the matrix
        return board  #return the new board, with the proper dimensions and all zeros entries


def getHumanMove(board, isFirstMove):
    '''
    This function controls the human player's movement of the token.
    It includes the process of dragging and dropping a token to place it on the board.

    board (list) - tracking what's on the game board
    isFirstMove(bool) - if True, then this is the first move of the human in this game, will need to display the instruction image
    '''
    draggingToken = False  #default state is not dragging a token
    tokenx, tokeny = None, None  #default state of the location of the token being dragged
    while True:
        for event in pygame.event.get(
        ):  #handling each event that we get from the queue
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE
            ):  #similar to before, close the game if the play clicks the [X] button of the game window or press the escape key
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(
                    event.pos
            ):  #if the mouse button is pressed down, and draggingToken state has yet to be activated, and the mouse clicks the human player's token pile
                draggingToken = True  #change the state of the draggingToken variable from False to True
                tokenx, tokeny = event.pos  #the location of the token is set to where the user clicked the mouse

            elif event.type == MOUSEMOTION and draggingToken:  #if the mouse button is pressed down, and draggingToken state has already been activated
                tokenx, tokeny = event.pos  # update the position of the human's token to the current location of the mouse

            elif event.type == MOUSEBUTTONUP and draggingToken:  #if the human let go of the mouse button, and the draggingToken variable has yet to be changed to False (will let go of the token that is being dragged)
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:  #if the token is being let go at the top of the screen
                    column = int(
                        (tokenx - XMARGIN) / SPACESIZE
                    )  #find the column (integer value) that the token is being dropped onto

                    if isValidMove(
                            board, column
                    ):  #check if the move is valid, player is only able to drop the token if the move is valid
                        animateDroppingToken(
                            board, column, RED
                        )  #use animateDroppingToken function to draw the dropping process of token
                        board[column][getLowestEmptySpace(
                            board, column
                        )] = RED  #place the human's token in the lowest empty row of the appropriate column
                        drawBoard(
                            board
                        )  #update the board, now containing the new token
                        pygame.display.update(
                        )  #update the pygame display to include changes to the board
                        return  #exit the function if a valid move is made
                tokenx, tokeny = None, None  #reset token location variables
                draggingToken = False  #reset dragging variable

# ------ person 3 starts comments ****** Kohinoor
        if tokenx != None and tokeny != None:
            drawBoard(
                board, {
                    'x': tokenx - int(SPACESIZE / 2),
                    'y': tokeny - int(SPACESIZE / 2),
                    'color': RED
                })
        else:
            drawBoard(board)

        if isFirstMove:
            # Show the help arrow for the player's first move.
            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)

        pygame.display.update()
        FPSCLOCK.tick()


def animateDroppingToken(board, column, color):
    """Animates the dropping of the actual token from above the board to the next empty row in specified column

    Args:
        board (list): The board used where the dropping of the token will be animated (only needed for board that is displayed to user)
        column (int): The column in which the token is being dropped
        color (str): Color of token being animated
    """
    x = XMARGIN + column * SPACESIZE  #x-position of where the token is being dropped
    y = YMARGIN - SPACESIZE  #y-position of where the token is being dropped
    dropSpeed = 1.0  #Speed at which the token is dropped

    #Bugged Area of Code
    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(
            dropSpeed
        )  #moves the token down the y-axis at the speed specified (1 pixel per frame)
        dropSpeed += 0.5  #add 0.5 pixels to the drop speed every time this code is ran
        if int(
            (y - YMARGIN) / SPACESIZE
        ) >= lowestEmptySpace:  #if the token object is at the lowest empty space,
            return  #stop the animation
        drawBoard(board, {'x': x, 'y': y, 'color': color})  #
        pygame.display.update(
        )  #update the display of what has changed every frame
        FPSCLOCK.tick(
        )  #called every frame in order to ensure game is running at specified fps


def animateComputerMoving(board, column):
    """Animates the moving of the token from the computer's token to where the token is dropped

    Args:
        board (list): The board used where the movement of token is animated (only needed for board that is displayed to user)
        column (int): The column in which the token is being dropped
    """
    x = BLACKPILERECT.left  #x-position is set to the left pixels of the black pile of tokens
    y = BLACKPILERECT.top  #y-position is set to the top pixels of the black pile of tokens
    speed = 1.0  #speed at which tokens are dropped

    # moving the black tile up
    while y > (
            YMARGIN - SPACESIZE
    ):  #while the token is still under the y-value where the token should be dropped
        y -= int(speed)  #move the token up at the pixels per frame set
        speed += 0.5  #makes the pixels per frame moved get higher every frame
        drawBoard(
            board, {
                'x': x,
                'y': y,
                'color': BLACK
            }
        )  #creates a token on the board at the position where the token was dropped
        pygame.display.update(
        )  #update the display of what has changed every frame
        FPSCLOCK.tick(
        )  #called every frame in order to ensure game is running at specified fps

    # moving the black tile over
    y = YMARGIN - SPACESIZE  #reset y-position as 50 pixels over the y-margin of the board
    speed = 1.0  #reset speed as 1 pixel per frame
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed)  #move the token right at the pixels per frame
        speed += 0.5  #makes the pixels per frame moved get faster every fram
        drawBoard(
            board, {
                'x': x,
                'y': y,
                'color': BLACK
            }
        )  #creates a token on the board at the position where the token was dropped
        pygame.display.update(
        )  #update the display of what has changed every frame
        FPSCLOCK.tick(
        )  #called every frame in order to ensure game is running at specified fps
    # dropping the black tile
    animateDroppingToken(
        board, column,
        BLACK)  #Starts the dropping animation from where the token was moved


def getComputerMove(board):
    """Gets the best move for the computer to play out of all potential moves

    Args:
        board (list): The board used where the movement of token is animated (only needed for board that is displayed to user)
    """
    potentialMoves = getPotentialMoves(
        board, BLACK, DIFFICULTY
    )  #calls the getPotentialMoves() function and uses the board to calculate all of black's possible moves, DIFFICULTY moves into the future
    # get the best fitness from the potential moves
    bestMoveFitness = -1  #default best move fitness is -1
    for i in range(
            BOARDWIDTH):  #loop through this for all rows across the board
        if potentialMoves[i] > bestMoveFitness and isValidMove(
                board, i
        ):  #if the move is better than the default move fitness and is a valid move
            bestMoveFitness = potentialMoves[
                i]  #make that the best move fitness
    # continue loop until the best move(s) are found
    bestMoves = [
    ]  #create a list for all moves with the highest and same bestMoveFitness value
    for i in range(len(potentialMoves)):  #for all potential moves
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(
                i
            )  #search through the possible moves and make add all the best moves (ones with the highest bestMoveFitness) into a list
    return random.choice(
        bestMoves)  #select randomly between all of the best possible moves


def getPotentialMoves(board, tile, lookAhead):
    """Gets all potential moves for the computer to play

    Args:
        board (list): The board used where the movement of token is animated (only needed for board that is displayed to user)
        tile (str): The colour of the tile being checked
        lookAhead (int): How many moves the AI should look ahead (associated with the DIFFICULTY integer)
    """
    if lookAhead == 0 or isBoardFull(
            board
    ):  #if there are no more moves to look at or the board is full
        return [0] * BOARDWIDTH  #return 0's along the entire board

    if tile == RED:
        enemyTile = BLACK  #if your tile is red, the enemy tile if black
    else:
        enemyTile = RED  #otherwise enemy tile is red

    # Figure out the best move to make.
    potentialMoves = [
        0
    ] * BOARDWIDTH  #create a list with 0's the size of the rows
    for firstMove in range(BOARDWIDTH):
        dupeBoard = copy.deepcopy(board)  #create a copy of the board
        if not isValidMove(dupeBoard,
                           firstMove):  #check if moves being checked are valid
            continue  #if they are, continue
        makeMove(dupeBoard, tile, firstMove)  #makes a move on the copy board
      # ------ person 4 comments here ****** Iris
        if isWinner(
                dupeBoard, tile
        ):  #look at the deepcopy of the board. If the computer's move is a winning move,
            # a winning move automatically gets a perfect fitness
            potentialMoves[
                firstMove] = 1  # investigate the move fitness ranking system
            break  # don't bother calculating other moves
        else:  # if the move is not a winning move,
            # do other player's counter moves and determine best one
            if isBoardFull(
                    dupeBoard
            ):  # if there are no empty spaces on the copy of the board
                potentialMoves[firstMove] = 0  # the fitness ranking is 0 and the computer will not play the move
            else:  # when the board isn't full
                for counterMove in range(
                        BOARDWIDTH
                ):  # for every available space in the width of the board, consider:
                    dupeBoard2 = copy.deepcopy(
                        dupeBoard)  # make a copy of the board to analyse
                    if not isValidMove(
                            dupeBoard2, counterMove
                    ):  # Is the space you're looking at available to play a piece?
                        continue  # if it is not available, go to the next space.
                    makeMove(
                        dupeBoard2, enemyTile, counterMove
                    )  # the computer pretends the player makes a move in its dupeBoard2
                    if isWinner(dupeBoard2,
                                enemyTile):  # If the player's tile would win,
                        # a losing move automatically gets the worst fitness
                        potentialMoves[firstMove] = -1
                        break  # stop the loop
                    else:  # if the player's tile would not win,
                        # do the recursive call to getPotentialMoves()
                        results = getPotentialMoves(
                            dupeBoard2, tile, lookAhead - 1
                        )  # if the computer can't win from looking at the next 2 potential moves,
                        # it looks at only one move in advance and tries to optimize that
                        potentialMoves[firstMove] += (sum(results) /
                                                      BOARDWIDTH) / BOARDWIDTH
    return potentialMoves  # returns a list of moves


def getLowestEmptySpace(
        board,
        column):  # asks what space the chip can be placed in a certain column
    '''finds the lowest space to put the next piece
  Arguments:
  board: a list where the piece can move
  column: a list that defines all the columns of the playing board
  '''
    # Return the row number of the lowest empty row in the given column.
    for y in range(
            BOARDHEIGHT - 1, -1, -1
    ):  # start at the upper limit of the board and keep checking down in increments of 1 until the last space
        if board[column][
                y] == EMPTY:  # if the coordinate indicated on the board is empty,
            return y  # return the y coordinate that is empty
    return -1


def isValidMove(board,
                column):  # tells where you or the computer can put a chip
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        # if the column is outside the gameboard (left or right of it) or there isn't an empty space,
        return False  # a chip cannot be placed
    return True  # you can place a piece in a valid space


def isBoardFull(board):  # has the entire board been filled?
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH
                   ):  # checking each x coordinate (column) in the game board
        for y in range(BOARDHEIGHT
                       ):  # checking each y coordinate (row) in the game board
            if board[x][y] == EMPTY:  # if the coordinate is empty,
                return False  # the board is not yet full
    return True  # otherwise, every spot is full


def isWinner(board, tile):  # checks for 4 in a row
    # check horizontal spaces
    for x in range(
            BOARDWIDTH - 3
    ):  # starting from the right most column, keep checking columns to the left until the fourth column
      
        for y in range(BOARDHEIGHT):  # checking each row
            if board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile and board[x + 3][y] == tile:
                # keep checking each tile to the left. If they correspond with the tile specified,
                return True  # it's a four in a row!
      
    # check vertical spaces
    for x in range(BOARDWIDTH):  # checking each column,
        for y in range(
                BOARDHEIGHT - 3
        ):  # starting from the bottom most row, keep checking rows above until the fourth row
            if board[x][y] == tile and board[x][y + 1] == tile and board[x][
                    y + 2] == tile and board[x][
                        y +
                        3] == tile:  # keep checking each tile above. If they correspond with the tile specified,
                return True  # it's a four in a row!
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        # starting from the right most column, keep checking columns to the left until the fourth column
        for y in range(
                3, BOARDHEIGHT
        ):  # checking from the thrid row to the sixth from the bottom
            if board[x][y] == tile and board[x + 1][y - 1] == tile and board[
                    x + 2][y - 2] == tile and board[x + 3][
                        y -
                        3] == e:  # keep checking each tile to the left and down. If they correspond with the tile specified,
                return True  # it's a four in a row!
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        # starting from the right most column, keep checking columns to the left until the fourth column
        for y in range(
                BOARDHEIGHT - 3
        ):  # starting from the bottom most row, keep checking rows above until the fourth row
            if board[x][y] == tile and board[x + 1][y + 1] == tile and board[
                    x + 2][y + 2] == tile and board[x + 3][y + 3] == tile:
                # keep checking each tile to the left and up. If they correspond with the tile specified,
                return True  # it's a four in a row
    return False  #if none of these tests work, there is no winner yet.


if __name__ == '__main__':  # if "__main__" is the name of the file, run the file.
    main()
# if the variable __name__ is set as "__main__" then the interpreter will run the module containing main()

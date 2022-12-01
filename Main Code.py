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

import random, copy, sys, pygame
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6 # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

DIFFICULTY = 2 # how many moves to look ahead. (>2 is usually too much)

SPACESIZE = 50 # size of the tokens and individual board spaces in pixels

FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'


def main():
    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
    global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
    global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Four in a Row')

    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    REDTOKENIMG = pygame.image.load('4row_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('4row_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('4row_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

    HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
    COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
    TIEWINNERIMG = pygame.image.load('4row_tie.png')
    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    ARROWIMG = pygame.image.load('4row_arrow.png')
    ARROWRECT = ARROWIMG.get_rect()
    ARROWRECT.left = REDPILERECT.right + 10
    ARROWRECT.centery = REDPILERECT.centery

    isFirstGame = True

    while True:
        runGame(isFirstGame)
        isFirstGame = False


def runGame(isFirstGame):
    if isFirstGame:
        # Let the computer go first on the first game, so the player
        # can see how the tokens are dragged from the token piles.
        turn = COMPUTER
        showHelp = True
    else:
        # Randomly choose who goes first.
        if random.randint(0, 1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN
        showHelp = False

    # Set up a blank board data structure.
    mainBoard = getNewBoard()

    while True: # main game loop
        if turn == HUMAN:
            # Human player's turn.
            getHumanMove(mainBoard, showHelp)
            if showHelp:
                # turn off help arrow after the first move
                showHelp = False
            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG
                break
            turn = COMPUTER # switch to other player's turn
        else:
            # Computer player's turn.
            column = getComputerMove(mainBoard)
            animateComputerMoving(mainBoard, column)
            makeMove(mainBoard, BLACK, column)
            if isWinner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG
                break
            turn = HUMAN # switch to other player's turn

        if isBoardFull(mainBoard):
            # A completely filled board means it's a tie.
            winnerImg = TIEWINNERIMG
            break

# ------- second person starts here *********
    while True:
        # the while True loop keep repeating the code inside it until the player clicks the mouse or quits.
        drawBoard(mainBoard)  #create the mainboard
        DISPLAYSURF.blit(winnerImg, WINNERRECT) # "blit" stands for Block Transfer, it copy winner image from the source file to the display surface
      
        pygame.display.update() # update/refresh the display, make the surface appear on the user's monitor
      
        FPSCLOCK.tick() #update the clock once per frame
      
        #this is a for loop that handles events
        for event in pygame.event.get():  # for each event that we get from the queue
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            #QUIT happens when the user closes the game window by pressing the [X] button
            #KEYUP means when a key is released, K_ESCAPE is the escape key. So when the user presses the escape key, the game would close         
              pygame.quit() #quit the game, uninitialize pygame modules
              sys.exit() #exit the system

            elif event.type == MOUSEBUTTONUP: # MOUSEBUTTONUP is when the mouse button is released (after the player drags token to the top of a stack)
                return #return and comes out of the function runGame

def makeMove(board, player, column):
    '''
    board (list) - tracking what's on the game board
    player (str) - this differentiates between the human player and the computer
    column (int) - this is the column that the token will be placed on (or attempted to be placed on)
    
    This function determines whether or not the person or the computer can add a token to a column.
    It makes sure that the token is placed at the lowest possible space in the column by using getLowestEmptySpace.
    If there is no space in the column selected by the player, then the variable "lowest" would equal -1, and the move cannot be made. Otherwise, the player's token will be put into the lowest empty space in the selected column.
    '''
    lowest = getLowestEmptySpace(board, column) # lowest checking if there is an empty space in that column to fit the token
    if lowest != -1: #if there is space to fit the token
        board[column][lowest] = player #the lowest row of the selected column of the board will be changed to a token (with the player's colour)

def drawBoard(board, extraToken=None):
    '''
    This function creates the display for the game board. 
    It creates rectangles barriers for the tokens, extra tokens, board image, and token piles.
  
    board (list) - tracking what's on the game board
    extraToken=None - each time the board is drawn, the amount of extra token is reset to zero (another extra token will be generated if the player drags a token from their stack)
    '''
    DISPLAYSURF.fill(BGCOLOR)  #the background colour fills the display screen

    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE) #create a variable spaceRect to store rectangle coordinates of around each token
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT): #nested for loops iterating each column and row from the game board
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE),
                                 YMARGIN + (y * SPACESIZE)) #fit a rectangle to each space in the columns and rows, use ".topleft" to align them
            if board[x][y] == RED: #if that space on the board is assigned to a token from the human player
                DISPLAYSURF.blit(REDTOKENIMG, spaceRect) #display the human token image in the rectangle space
            elif board[x][y] == BLACK: #if that space on the board is assigned to a token from the computer 
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect) #display the computer token image in the rectangle space

    # when the human player or computer drag a token, an extra token will be created
    if extraToken != None: #if there should exist an extra token
        if extraToken['color'] == RED: #if the extra token from the human player
            DISPLAYSURF.blit(
                REDTOKENIMG,
                (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE)) #draw an extra token image to the appropriate location on the display surface
        elif extraToken['color'] == BLACK: #if the extra token is from the computer
            DISPLAYSURF.blit(
                BLACKTOKENIMG,
                (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE)) #draw an extra token image to the appropriate location on the display surface

    # draw board over the tokens, so that the blue board structure image appears above the tokens
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT): #nested for loops iterating each column and row from the game board
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE),
                                 YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect) #draw a single square picture of the game board onto each space of the board, and align image with ".topleft"

    # display the starting piles of tokens
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT)  # human player's tokens on the left, at the space of the pile rectangle
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)  # computer's tokens on the right, at the space of the pile rectangle

def getNewBoard():
  '''
  This function create a new empty board.
  '''
    board = [] #the board variable is assigned to an empty list
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT) #add zero for each entry in each column of the matrix
    return board #return the new board, with the proper dimensions and all zeros entries

def getHumanMove(board, isFirstMove):
    '''
    This function controls the human player's movement of the token.
    It includes the process of dragging and dropping a token to place it on the board.

    board (list) - tracking what's on the game board
    isFirstMove(bool) - if True, then this is the first move of the human in this game, will need to display the instruction image
    '''
    draggingToken = False #default state is not dragging a token
    tokenx, tokeny = None, None #default state of the location of the token being dragged
    while True:
        for event in pygame.event.get():  #handling each event that we get from the queue
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): #similar to before, close the game if the play clicks the [X] button of the game window or press the escape key
                pygame.quit()
                sys.exit()
              
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos): #if the mouse button is pressed down, and draggingToken state has yet to be activated, and the mouse clicks the human player's token pile
                draggingToken = True #change the state of the draggingToken variable from False to True
                tokenx, tokeny = event.pos #the location of the token is set to where the user clicked the mouse
              
            elif event.type == MOUSEMOTION and draggingToken: #if the mouse button is pressed down, and draggingToken state has already been activated
                tokenx, tokeny = event.pos # update the position of the human's token to the current location of the mouse
              
            elif event.type == MOUSEBUTTONUP and draggingToken: #if the human let go of the mouse button, and the draggingToken variable has yet to be changed to False (will let go of the token that is being dragged)
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN: #if the token is being let go at the top of the screen
                    column = int((tokenx - XMARGIN) / SPACESIZE) #find the column (integer value) that the token is being dropped onto
                    
                    if isValidMove(board, column): #check if the move is valid, player is only able to drop the token if the move is valid
                        animateDroppingToken(board, column, RED) #use animateDroppingToken function to draw the dropping process of token
                        board[column][getLowestEmptySpace(board, column)] = RED #place the human's token in the lowest empty row of the appropriate column
                        drawBoard(board) #update the board, now containing the new token
                        pygame.display.update() #update the pygame display to include changes to the board
                        return #exit the function if a valid move is made
                tokenx, tokeny = None, None #reset token location variables
                draggingToken = False #reset dragging variable
                
# ------ person 3 starts comments ******
        if tokenx != None and tokeny != None:
            drawBoard(board, {'x':tokenx - int(SPACESIZE / 2), 'y':tokeny - int(SPACESIZE / 2), 'color':RED})
        else:
            drawBoard(board)

        if isFirstMove:
            # Show the help arrow for the player's first move.
            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)

        pygame.display.update()
        FPSCLOCK.tick()


def animateDroppingToken(board, column, color):
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE
    dropSpeed = 1.0

    #the bug from buggy was here, it is fixed
    #the code used to be "lowestEmptySpace = column" which will cause the token to drop through the entire column.
    #the fix uses the getlowestEmptySpace function to get the token to drop to exactly the lowest empty space on the board (but not past it).
    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()


def animateComputerMoving(board, column):
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 1.0
    # moving the black tile up
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = YMARGIN - SPACESIZE
    speed = 1.0
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed)
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    animateDroppingToken(board, column, BLACK)


def getComputerMove(board):
    potentialMoves = getPotentialMoves(board, BLACK, DIFFICULTY)
    # get the best fitness from the potential moves
    bestMoveFitness = -1
    for i in range(BOARDWIDTH):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    # find all potential moves that have this best fitness
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, tile, lookAhead):
    if lookAhead == 0 or isBoardFull(board):
        return [0] * BOARDWIDTH

    if tile == RED:
        enemyTile = BLACK
    else:
        enemyTile = RED

    # Figure out the best move to make.
    potentialMoves = [0] * BOARDWIDTH
    for firstMove in range(BOARDWIDTH):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, firstMove):
            continue
        makeMove(dupeBoard, tile, firstMove)

# ------ person 4 comments here ******
        if isWinner(dupeBoard, tile):
            # a winning move automatically gets a perfect fitness
            potentialMoves[firstMove] = 1
            break # don't bother calculating other moves
        else:
            # do other player's counter moves and determine best one
            if isBoardFull(dupeBoard):
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(BOARDWIDTH):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    makeMove(dupeBoard2, enemyTile, counterMove)
                    if isWinner(dupeBoard2, enemyTile):
                        # a losing move automatically gets the worst fitness
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        # do the recursive call to getPotentialMoves()
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def isValidMove(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


def isWinner(board, tile):
    # check horizontal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False


if __name__ == '__main__':
    main()

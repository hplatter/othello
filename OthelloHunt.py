import turtle
import math
import copy
import time
import random

# Constants
boardsize = 600
margin = 75
mainwidth = 8
cells = 8
cellsize = (boardsize - 2 * margin) / cells
edgeBL = -boardsize/2+margin
edgeTR = boardsize/2-margin
playerColors = {
    'w': 'white',
    'b': 'black'
}

# Turtle Initialization
t = turtle.Turtle()
movesT = turtle.Turtle()
textT = turtle.Turtle()
s = turtle.Screen()
s.bgcolor('forest green')
s.setup(boardsize, boardsize)
t.hideturtle()
movesT.hideturtle()
textT.hideturtle()
textT.color('black')
movesT.shapesize(0.5, 0.5)
movesT.shape('circle')
movesT.penup()
textT.penup()
s.tracer(0, 0)

# Data Structure Setup
gameBoard = [[0 for _ in range(cells)] for _ in range(cells)]
gameBoard[3][3] = 'w'
gameBoard[3][4] = 'b'
gameBoard[4][4] = 'w'
gameBoard[4][3] = 'b'
currentPlayer = 'b'
moveDir = {
    'L': [0, -1],
    'R': [0, 1],
    'U': [-1, 0],
    'D': [1, 0],
    'UL': [-1, -1],
    'DL': [1, -1],
    'DR': [1, 1],
    'UR': [-1, 1]
}


# Dev
def printBoard(board):
    [print([str(loc) for loc in line]) for line in board]


# Functions
def whichRow(y):
    row = cells-math.ceil((y+boardsize/2-margin)/cellsize)
    if row >= 0 and row < cells:
        return row


def whichColumn(x):
    col = math.ceil((x+boardsize/2-margin)/cellsize)-1
    if col >= 0 and col < cells:
        return col


def yFromRow(row):
    return (row * cellsize + cellsize / 2 + margin) - boardsize / 2


def xFromColumn(column):
    return -((column * cellsize + cellsize / 2 + margin) - boardsize / 2)


def validChain(chain):
    valid = False
    if len(chain) > 1:
        if not chain[0] == chain[1] and not chain[0] == 0:
            for item in chain[1:]:
                if item == 0:
                    return False
                if item == chain[0]:
                    return True
    return valid


def updateBoard(board, player, row, col, movesOverride=False):
    if not movesOverride:
        moves = validMove(board, player, row, col)
    else:
        moves = movesOverride
    if(moves):
        board[row][col] = player
        for dir in moves:
            for i in range(1, cells):
                if board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] == player or board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] == 0:
                    break
                else:
                    board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] = player
    return board


def calculateScore(board, player):
    score = 0
    for row in board:
        for col in row:
            if col == player:
                score += 1
    return score


def validMove(board, player, row, col):
    newBoard = copy.deepcopy(board)
    if not board[row][col] == 0:
        return False
    newBoard[row][col] = player
    fullCol = [newBoard[i][col] for i in range(cells)]
    diagPosA = []
    diagNegA = []
    diagPosB = []
    diagNegB = []
    validMoves = []
    for i in range(-cells + 1, 1):
        if row + i >= 0 and col + i >= 0 and row + i < cells and col + i < cells:
            diagPosA.append(newBoard[row + i][col + i])
        if row - i >= 0 and col + i >= 0 and row - i < cells and col + i < cells:
            diagNegA.append(newBoard[row - i][col + i])
    for i in range(0, cells):
        if row + i >= 0 and col + i >= 0 and row + i < cells and col + i < cells:
            diagPosB.append(newBoard[row + i][col + i])
        if row - i >= 0 and col + i >= 0 and row - i < cells and col + i < cells:
            diagNegB.append(newBoard[row - i][col + i])
    if validChain(newBoard[row][:col + 1][::-1]):
        validMoves.append('L')
    if validChain(newBoard[row][col:]):
        validMoves.append('R')
    if validChain(fullCol[:row + 1][::-1]):
        validMoves.append('U')
    if validChain(fullCol[row:]):
        validMoves.append('D')
    if validChain(diagPosA[::-1]):
        validMoves.append('UL')
    if validChain(diagNegA[::-1]):
        validMoves.append('DL')
    if validChain(diagPosB):
        validMoves.append('DR')
    if validChain(diagNegB):
        validMoves.append('UR')

    if len(validMoves) > 0:
        return validMoves
    else:
        return False


def nextBoard(board, player, move, movesOverride=False):
    board = copy.deepcopy(board)
    return updateBoard(board, player, move[0], move[1], movesOverride)


def allValidMoves(board, player):
    output = []
    zeros = 0
    for rowIndex in range(cells):
        for colIndex in range(cells):
            if board[rowIndex][colIndex] == 0:
                zeros += 1
                if validMove(board, player, rowIndex, colIndex):
                    output.append([rowIndex, colIndex])
    if zeros > 0:
        return output
    else:
        return 'Winner'


def flipCurrentPlayer():
    global currentPlayer
    textT.goto(0, -boardsize / 2 + margin / 2)
    if currentPlayer == 'b':
        currentPlayer = 'w'
        textT.write('White\'s Move', move=True, align="center", font=('Helvetica Neue', '16', 'bold'))
    else:
        currentPlayer = 'b'
        textT.write('Black\'s Move', move=True, align="center", font=('Helvetica Neue', '16', 'bold'))


def drawBoard():
    t.width(mainwidth)
    t.penup()
    t.goto(edgeBL, edgeBL)
    t.pendown()
    t.color('black')
    t.goto(edgeTR, edgeBL)
    t.goto(edgeTR, edgeTR)
    t.goto(edgeBL, edgeTR)
    t.goto(edgeBL, edgeBL)

    t.width(mainwidth/2)
    for cell in range(1,cells+1):
        t.penup()
        t.goto(edgeBL + (cell * cellsize), edgeTR)
        t.pendown()
        t.goto(edgeBL + (cell * cellsize), edgeBL)
        t.penup()
        t.goto(edgeBL, edgeTR - (cell * cellsize))
        t.pendown()
        t.goto(edgeTR, edgeTR - (cell * cellsize))


def stampPlayer(row, column, player):
    t.goto(yFromRow(row), xFromColumn(column))
    t.color(player)
    t.stamp()


def drawPieces():
    for rowIndex in range(cells):
        for colIndex in range(cells):
            if not gameBoard[rowIndex][colIndex] == 0:
                stampPlayer(colIndex, rowIndex, playerColors[gameBoard[rowIndex][colIndex]])

gameRunning=()

def drawMoves():
    moves = allValidMoves(gameBoard, currentPlayer)
    if moves == 'Winner':
        textT.goto(0, -boardsize/2 + margin/4)
        winner = playerColors['b']
        if calculateScore(gameBoard, 'w') > calculateScore(gameBoard, 'b'):
            winner = playerColors['w']
        textT.write('The winner is ' + winner + '!', move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
        gameRunning=False
    elif len(moves) > 0:
        for move in moves:
            movesT.goto(yFromRow(move[1]), xFromColumn(move[0]))
            movesT.color(playerColors[currentPlayer])
            movesT.stamp()
    else:
        textT.goto(0, -boardsize/2 + margin/4)
        textT.write('No valid moves, skipped ' + playerColors[currentPlayer] + '\'s turn.', move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
        draw()
        flipCurrentPlayer()
        postDraw()


def drawScore():
    t.goto(-cellsize, boardsize/2 - margin/2)
    t.color('black')
    t.stamp()
    t.color('white')
    t.goto(-cellsize, boardsize/2 - margin/2 - 8)
    t.write(calculateScore(gameBoard, 'b'), move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
    t.goto(cellsize, boardsize/2 - margin/2)
    t.color('white')
    t.stamp()
    t.color('black')
    t.goto(cellsize, boardsize/2 - margin/2 - 8)
    t.write(calculateScore(gameBoard, 'w'), move=True, align="center", font=('Helvetica Neue', '16', 'normal'))


def draw():
    movesT.clear()
    textT.clear()
    t.penup()
    t.shape('circle')
    t.shapesize(2, 2)
    drawScore()
    drawPieces()


def postDraw():
    drawMoves()


def move(row, col):
    global gameBoard
    if (row or row == 0) and (col or col == 0):
        moveCheck = validMove(gameBoard, currentPlayer, row, col)
        if moveCheck:
            gameBoard = nextBoard(gameBoard, currentPlayer, [row, col], moveCheck)
            draw()
            flipCurrentPlayer()
            postDraw()
        else:
            print('Invalid Move')
            return 'Invalid Move'


def click(x,y):
    move(whichRow(y), whichColumn(x))

#Hannah's Code
def beginAutomation():
    i=0
    #winner='w'
    while i<((cells*cells)-4):
        moveTo=eval(Evaluate(gameBoard,currentPlayer))
        move((moveTo[0]),(moveTo[1]))
        if gameRunning==False:
            break
        #time.sleep(.001)
        i+=1
        moveTo=random.choice(allValidMoves(gameBoard,currentPlayer))
        move((moveTo[0]),(moveTo[1]))
        if gameRunning==False:
            break
        #time.sleep(.001)
        i+=1
    return "game over"

def tempMove(board,row, col):
    if (row or row == 0) and (col or col == 0):
        moveCheck = validMove(board, currentPlayer, row, col)
        if moveCheck:
            board = nextBoard(board, currentPlayer, [row, col], moveCheck)
            return board
        else:
            print('Invalid Move')
            return 'Invalid Move'

def f(n):
    i=0
    #corners
    if n== (0,0) or  n==(0,cells-1) or  n== (cells-1,0) or  n== (cells-1,cells-1):
        i+=500
    #near the conrners
    if n== (1,0) or n== (1,1) or n== (0,1) or  n==(0,cells-2) or n==(1,cells-2) or n==(1,cells-1) or  n== (cells-2,0) or n== (cells-2,1) or n==(cells-1,1) or  n== (cells-2,cells-1) or  n== (cells-2,cells-2) or  n== (cells-1,cells-2):
        i-=500
    if n[0]==0 or (cells-1):
        i+=200
    if n[1]==0 or (cells-1):
        i+=200
    tempBoard=copy.deepcopy(gameBoard)
    tempOScore=calculateScore(tempBoard, currentPlayer)
    tempBoard=tempMove(tempBoard,n[0],n[1])
    tempNScore=calculateScore(tempBoard, currentPlayer)
    tempPoint=(tempNScore)-(tempOScore)
    i+=tempPoint
    return i

def Evaluate(gameBoard,currentPlayer):
    evalList={}
    if len(allValidMoves(gameBoard,currentPlayer)) == 0:
        return "Game Over"
    if type(allValidMoves(gameBoard,currentPlayer))==list:
        for each in allValidMoves(gameBoard,currentPlayer):
            evalList[str(each)]=(f((each[0],each[1])))
        i=0
        if (calculateScore(gameBoard, 'b')+calculateScore(gameBoard, 'w'))>16:
            maxVal=max(evalList.values())
        else:
            maxVal=min(evalList.values())
        for n in evalList:
            if evalList[n]==maxVal:
                return n
    else:
        return False
winner='b'

#def minimax(player,board):
#    if i=2 or gameRunning==False:
#        return currentPlayer
#    children = allValidMoves(gameBoard, currentPlayer)
#    minimaxChildren=[]
#    for each in children:
#        nextBoard(gameBoard,currentPlayer,each)
#        minimaxChildren.append(minimax(currentPlayer,gameBoard))
#    if winner==currentPlayer:
#        print (minimaxChildren)
#        return max(minimaxChildren)
#    else:
#        print (minimaxChildren)
#        return min(minimaxChildren)

def terminalNode(board, player):
    moves = allValidMoves(board, player)
    if len(moves)==0 or moves=="Winner":
        return True

def evalBoard(board, player):
    score=calculateScore(board, player)
    if player== board[0][0] or  player ==board[0][cells-1] or  player == board[cells-1][0] or  player == board[cells-1][cells-1]:
        score += 100
    if player== board[1][0] or player== board[1][1] or player== board[0][1] or  player==board[0][cells-2] or player==board[1][cells-2] or player==board[1][cells-1] or  player== board[cells-2][0] or player== board[cells-2][1] or player==board[cells-1][1] or  player== board[cells-2][cells-1] or  player== board[cells-2][cells-2] or  player== board[cells-1][cells-2]:
        score-=500
    score+=(calculateScore(board,player)-calculateScore(gameBoard,player))
    return score

def notPlayer(player):
    if player == 'b':
        return 'w'
    if player == 'w':
        return 'b'
    
def abminimax(board, player, A=-math.inf, B=math.inf, depth=0, maxTurn=False):
    print(player)
    if depth==2:
        return calculateScore(board,player)+evalBoard(board,player)
    if terminalNode(board, player):
        if calculateScore(board,player)>32:
            return math.inf
        else:
            return -math.inf
    moves=allValidMoves(board, player)
    depth +=1
    if maxTurn:
        for each in moves:
            score=abminimax(nextBoard(board,player, each),notPlayer(player),A,B,depth,not maxTurn)
            if score>A:
                A=score
            if A>=B:
                return A
        return A
    else:
        for each in moves:
            score=abminimax(nextBoard(board,player, each),notPlayer(player),A,B,depth,not maxTurn)
            print(score)
            if score<B:
                B=score
            if A>=B:
                return B
        return B


def evalMiniMax(board,player):
    moves={}
    for each in allValidMoves(board,player):
        moves[(abminimax(nextBoard(board,player,each),player))]=each
    return moves[max(moves)]

s.onclick(click)


drawBoard()
draw()
postDraw()

abminimax(gameBoard,currentPlayer)

from decimal import Decimal
weights = [[99, -8, 8, 6, 6, 8, -8, 99],
           [-8, -24, -4, -3, -3, -4, -24, -8],
           [8, -4, 7, 4, 4, 7, -4, 8],
           [6, -3, 4, 0, 0, 4, -3, 6],
           [6, -3, 4, 0, 0, 4, -3, 6],
           [8, -4, 7, 4, 4, 7, -4, 8],
           [-8, -24, -4, -3, -3, -4, -24, -8],
           [99, -8, 8, 6, 6, 8, -8, 99]]

def readFile(filepath):
    file = open(filepath)
    player = file.readline().strip('\n')
    depth = file.readline().strip('\n')
    board = []
    for line in file:
        line = line.strip('\n').strip('\r')
        board.append([line])
    return player, depth, board

def findmin(board, depth, player, alpha, beta):
    pass

def findmax(board, depth, player, alpha, beta):
    pass

def getvalidaction(board, player):
    pass

def calvalue(board, player):
    value = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == player:
                value += weights[i][j]
    return value


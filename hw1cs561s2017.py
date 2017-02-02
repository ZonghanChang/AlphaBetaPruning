from decimal import Decimal
weights = [[99, -8, 8, 6, 6, 8, -8, 99],
           [-8, -24, -4, -3, -3, -4, -24, -8],
           [8, -4, 7, 4, 4, 7, -4, 8],
           [6, -3, 4, 0, 0, 4, -3, 6],
           [6, -3, 4, 0, 0, 4, -3, 6],
           [8, -4, 7, 4, 4, 7, -4, 8],
           [-8, -24, -4, -3, -3, -4, -24, -8],
           [99, -8, 8, 6, 6, 8, -8, 99]]

row_name = [1, 2, 3, 4, 5, 6, 7, 8]
column_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
directions = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
blank = '*'
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
    opponent = 'O' if player == 'X' else 'X'
    valid_pos = list()
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == blank:
                cur = [i, j]
                for direction in directions:
                    while True:
                        next = [direction[0] + cur[0], direction[1] + cur[1]]
                        if next[0] < 0 or next[1] < 0 or next[0] >= len(board) or next[1] >= len(board[0]):
                            break
                        if board[next[0]][next[1]] == player and cur == [i, j]:
                            break
                        if board[next[0]][next[1]] == blank:
                            break
                        if board[next[0]][next[1]] == player:
                            valid_pos.append((i, j))
                        cur = next

    return valid_pos

def calvalue(board, player):
    value = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == '*':
                pass
            elif board[i][j] == player:
                value += weights[i][j]
            else:
                value -= weights[i][j]
    return value


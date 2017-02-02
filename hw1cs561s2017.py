from decimal import Decimal
from copy import deepcopy

def readFile(filepath):
    file = open(filepath)
    player = file.readline().strip('\r\n')
    depth = int(file.readline().strip('\r\n'))
    board = list()
    for line in file:
        line = line.strip('\r\n')
        row = list()
        for c in line:
            row.append(c)
        board.append(row)
    return player, depth, board

def findmax(board, depth, max_depth, player, alpha, beta, parent):
    opponent = 'O' if player == 'X' else 'X'
    if depth > max_depth:
        value = calvalue(board, player)
        # print str(column_name[parent[1]]) + str(row_name[parent[0]]), depth - 1, value, alpha, beta
        return value
    valid_pos = getvalidaction(board, player)
    v = Decimal("-Infinity")
    for pos in valid_pos:
        print str(column_name[pos[1]]) + str(row_name[pos[0]]), depth, v, alpha, beta
        copy = deepcopy(board)
        copy[pos[0]][pos[1]] = player
        turncell(copy, pos, opponent, player)
        v = max(v, findmin(copy, depth + 1, max_depth, player, alpha, beta, pos))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def findmin(board, depth, max_depth, player, alpha, beta, parent):
    opponent = 'O' if player == 'X' else 'X'
    if depth > max_depth:
        value = calvalue(board, player)
        print str(column_name[parent[1]]) + str(row_name[parent[0]]), depth - 1, value, alpha, beta
        return value
    valid_pos = getvalidaction(board, opponent)
    v = Decimal("Infinity")
    for pos in valid_pos:
        print str(column_name[pos[1]]) + str(row_name[pos[0]]), depth, v, alpha, beta
        copy = deepcopy(board)
        copy[pos[0]][pos[1]] = opponent
        turncell(copy, pos, player, opponent)
        v = min(v, findmax(copy, depth + 1, max_depth, player, alpha, beta, pos))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def turncell(board, cur, turn_from, turn_to):
    ori = cur
    for direction in directions:
        path = list()
        cur = ori
        while True:
            next = [direction[0] + cur[0], direction[1] + cur[1]]
            if next[0] < 0 or next[1] < 0 or next[0] >= len(board) or next[1] >= len(board[0]):
                break
            if board[next[0]][next[1]] == blank:
                break
            if board[next[0]][next[1]] == turn_to:
                for cell in path:
                    board[cell[0]][cell[1]] = turn_to
            path.append(next)
            cur = next


def getvalidaction(board, player):
    valid_pos = list()
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == blank:

                for direction in directions:
                    cur = [i, j]
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
                            break
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


weights = ((99, -8, 8, 6, 6, 8, -8, 99),
           (-8, -24, -4, -3, -3, -4, -24, -8),
           (8, -4, 7, 4, 4, 7, -4, 8),
           (6, -3, 4, 0, 0, 4, -3, 6),
           (6, -3, 4, 0, 0, 4, -3, 6),
           (8, -4, 7, 4, 4, 7, -4, 8),
           (-8, -24, -4, -3, -3, -4, -24, -8),
           (99, -8, 8, 6, 6, 8, -8, 99))

row_name = (1, 2, 3, 4, 5, 6, 7, 8)
column_name = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
blank = '*'
player, depth, board = readFile("input.txt")
findmax(board, 1, depth, player, Decimal("-Infinity"), Decimal("Infinity"), None)
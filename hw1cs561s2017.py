#!/usr/bin/env python

from decimal import Decimal
from copy import deepcopy


class AlphaBetaPruning(object):
    traverse_log = list()

    def readFile(self, filepath):
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

    def appendlog(self, pos, depth, v, alpha, beta):
        if pos is None and depth != 0:
            self.traverse_log.append('pass,%s,%s,%s,%s' % (depth, v, alpha, beta))
        elif depth == 0:
            self.traverse_log.append('root,0,%s,%s,%s' % (v, alpha, beta))
        else:
            self.traverse_log.append('%s%s,%s,%s,%s,%s' % (column_name[pos[1]], row_name[pos[0]], depth, v, alpha, beta))

    def findmax(self, board, depth, max_depth, player, alpha, beta, parent):
        opponent = 'O' if player == 'X' else 'X'
        best_move = None
        valid_pos = self.getvalidaction(board, player)
        if depth > max_depth:
            value = self.calvalue(board, player)
            self.appendlog(parent, depth - 1, value, alpha, beta)
            return value, best_move

        v = Decimal("-Infinity")

        if len(valid_pos) != 0:
            for pos in valid_pos:
                # copy = deepcopy(board)
                # self.turncell(copy, pos, player)
                self.appendlog(parent, depth - 1, v, alpha, beta)

                board[pos[0]][pos[1]] = player
                cells = self.getcells(board, pos, player)
                self.turn_to(board, cells, player)
                temp = self.findmin(board, depth + 1, max_depth, player, alpha, beta, pos)
                self.turn_to(board, cells, opponent)
                board[pos[0]][pos[1]] = blank

                if temp > v:
                    v = temp
                    best_move = pos
                if v >= beta:
                    self.appendlog(parent, depth - 1, v, alpha, beta)
                    return v, best_move
                alpha = max(alpha, v)
        else:
            self.appendlog(parent, depth - 1, v, alpha, beta)
            temp = Decimal("-Infinity")
            if parent is None:
                temp = self.findmin(board, depth + 1, Decimal("-Infinity"), player, alpha, beta, None)
            else:
                temp = self.findmin(board, depth + 1, max_depth, player, alpha, beta, None)
            if temp > v:
                v = temp
            if v >= beta:
                self.appendlog(parent, depth - 1, v, alpha, beta)
                return v, best_move
            alpha = max(alpha, v)
        self.appendlog(parent, depth - 1, v, alpha, beta)
        return v, best_move


    def findmin(self, board, depth, max_depth, player, alpha, beta, parent):
        opponent = 'O' if player == 'X' else 'X'
        valid_pos = self.getvalidaction(board, opponent)
        if depth > max_depth:
            value = self.calvalue(board, player)
            self.appendlog(parent, depth - 1, value, alpha, beta)
            return value

        v = Decimal("Infinity")
        if len(valid_pos) != 0:
            for pos in valid_pos:
                # copy = deepcopy(board)
                # self.turncell(copy, pos, opponent)
                self.appendlog(parent, depth - 1, v, alpha, beta)

                board[pos[0]][pos[1]] = opponent
                cells = self.getcells(board, pos, opponent)
                self.turn_to(board, cells, opponent)
                temp, junk = self.findmax(board, depth + 1, max_depth, player, alpha, beta, pos)
                self.turn_to(board, cells, player)
                board[pos[0]][pos[1]] = blank
                
                v = min(v, temp)
                if v <= alpha:
                    self.appendlog(parent, depth - 1, v, alpha, beta)
                    return v
                beta = min(beta, v)

        else:
            self.appendlog(parent, depth - 1, v, alpha, beta)
            temp = Decimal("Infinity")
            if parent is None:
                temp, junk = self.findmax(board, depth + 1, Decimal("-Infinity"), player, alpha, beta, None)
            else:
                temp, junk = self.findmax(board, depth + 1, max_depth, player, alpha, beta, None)
            v = min(v, temp)

            if v <= alpha:
                self.appendlog(parent, depth - 1, v, alpha, beta)
                return v
            beta = min(beta, v)
        self.appendlog(parent, depth - 1, v, alpha, beta)
        return v

    def turn_to(self, board, cells, turn_to):
        for cell in cells:
            board[cell[0]][cell[1]] = turn_to

    def getcells(self, board, cur, turn_to):
        ori = cur
        cells = list()
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
                        cells.append(cell)
                    break
                path.append(next)
                cur = next
        return cells

    def turncell(self, board, cur, turn_to):
        ori = cur
        board[ori[0]][ori[1]] = turn_to
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
                    break
                path.append(next)
                cur = next
        return board

    def getvalidaction(self, board, player):
        valid_pos = list()
        visited = set()
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
                                if (i, j) in visited:
                                    break
                                valid_pos.append((i, j))
                                visited.add((i, j))
                                break
                            cur = next
        return valid_pos

    def calvalue(self, board, player):
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

alphabeta = AlphaBetaPruning()
row_name = (1, 2, 3, 4, 5, 6, 7, 8, '', '')
column_name = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'root', 'pass')
directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
blank = '*'
player, depth, board = alphabeta.readFile("input.txt")

v, best_move = alphabeta.findmax(board, 1, depth, player, Decimal("-Infinity"), Decimal("Infinity"), (8, 8))
if best_move is not None:
    board = alphabeta.turncell(board, best_move, player)
outfile = open('output.txt', 'w')
for line in board:
    for c in line:
        outfile.write(c)
    outfile.write('\n')
outfile.write('Node,Depth,Value,Alpha,Beta\n')
for log in alphabeta.traverse_log[0: -1]:
    outfile.write(log)
    outfile.write('\n')
outfile.write(alphabeta.traverse_log[-1])

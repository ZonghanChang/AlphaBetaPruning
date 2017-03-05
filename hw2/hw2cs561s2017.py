#!/usr/bin/env python

from copy import deepcopy

a = dict()
symbol = 'b'
a[symbol] = 1
print a


class Clause:
    positive_symbol = set()
    negtive_symbol = set()

    def add_positive(self, symbol):
        self.positive_symbol.add(symbol)

    def add_negtive(self, symbol):
        self.negtive_symbol.add(symbol)

class Model:
    assigments = dict()

    def __init__(self, values):
        self.assigments.update(values)

    def union(self, symbol):
        m = Model()
        m.assigments.update(self.assigments)
        m.assigments[symbol] = b
        return m

    def union_inplace(self, symbol, b):
        self.assigments[symbol] = b
        return self

    def satisfies(self, clauses):
        for c in clauses:
            pass

    def determin_value(self, clause):
        for item in clause:
            if item in self.assigments:
                return True

def every_clause_true():
    pass
def some_clause_false():
    pass

def dpll(clauses, symbols, model):
    if every_clause_true(clauses, model):
        return True
    if some_clause_false(clauses, model):
        return False


file = open("input.txt", "r")
first_line = file.readline().strip('\r\n').split()
guests = int(first_line[0])
tables = int(first_line[1])
sentence = list()
for i in range(guests):
    in_table_clause = set()
    for j in range(tables):
        in_table_clause.add((True, (i + 1, j + 1)))
        for k in range(j + 1, tables):
            in_onetable_clause = set()
            in_onetable_clause.add((False, (i + 1, j + 1)))
            in_onetable_clause.add((False, (i + 1, k + 1)))
            sentence.append(in_onetable_clause)
    sentence.append(in_table_clause)

print guests, tables

for line in file:
    line = line.strip('\r\n')
    tokens = line.split()
    if tokens[-1] == 'E':
        a = int(tokens[0])
        b = int(tokens[1])
        for i in range(tables):
            enemy_clause = set()
            enemy_clause.add((False, (a, i + 1)))
            enemy_clause.add((False, (b, i + 1)))
            sentence.append(enemy_clause)
    elif tokens[-1] == 'F':
        a = int(tokens[0])
        b = int(tokens[1])
        for i in range(tables):
            for j in range(tables):
                if i != j:
                    friend_clause = set()
                    friend_clause.add((False, (a, i + 1)))
                    friend_clause.add((False, (b, j + 1)))
                    sentence.append(friend_clause)

print sentence

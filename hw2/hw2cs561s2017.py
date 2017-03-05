#!/usr/bin/env python

from copy import deepcopy


class Clause:
    def __init__(self):
        self.positive_symbol = set()
        self.negtive_symbol = set()

    def add_positive(self, symbol):
        self.positive_symbol.add(symbol)

    def add_negtive(self, symbol):
        self.negtive_symbol.add(symbol)

    def get_positive(self):
        return self.positive_symbol

    def get_negtive(self):
        return self.negtive_symbol


class Model:
    def __init__(self):
        self.assigments = dict()

    def __init__(self, values):
        self.assigments = dict()
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
        for clause in clauses:
            value = self.determin_value(clause)
            if value is None or value is False :
                return False

        return True

    def determin_value(self, clause):

        for positive in clause.get_positive():
            if positive in self.assigments:
                value = self.assigments[positive]
                if value is True:
                    return True

        for negtive in clause.get_negtive():
            if negtive in self.assigments:
                value = self.assigments[negtive]
                if value is False:
                    return True

        return None


def every_clause_true(clauses, model):
    return model.satisfies(clauses)


def some_clause_false(clauses, model):
    for clause in clauses:
        if model.determin_value(clause) is False:
            return True
    return False

def find_pure_symbol(symbols, clauses, model):
    symbols_to_keep = deepcopy(symbols)
    candidate_pure_positive_symbols = set()
    candidate_pure_negtive_symbols = set()
    for clause in clauses:
        if model.determin_value(clause) is True:
            continue
        for p in clause.get_positive():
            if p in symbols_to_keep:
                candidate_pure_positive_symbols.add(p)
        for n in clause.get_negtive():
            if n in symbols_to_keep:
                candidate_pure_negtive_symbols.add(n)

    intersect = candidate_pure_positive_symbols & candidate_pure_negtive_symbols
    candidate_pure_positive_symbols -= intersect
    candidate_pure_negtive_symbols -= intersect

    if len(candidate_pure_positive_symbols) != 0:
        return candidate_pure_positive_symbols.



def dpll(clauses, symbols, model):
    if every_clause_true(clauses, model):
        return True
    if some_clause_false(clauses, model):
        return False
    if len(symbols) == 0:
        return False
    p = symbols[0]
    rest = symbols[1:]
    return dpll(clauses, rest, model.union_inplace(p, True)) or dpll(clauses, rest, model.union_inplace(p, False))


file = open("input4.txt", "r")
first_line = file.readline().strip('\r\n').split()
guests = int(first_line[0])
tables = int(first_line[1])
sentence = list()
symbols = list()
for i in range(guests):
    in_table_clause = Clause()
    for j in range(tables):
        in_table_clause.add_positive((i + 1, j + 1))
        symbols.append((i + 1, j + 1))
        for k in range(j + 1, tables):
            in_onetable_clause = Clause()
            in_onetable_clause.add_negtive((i + 1, j + 1))
            in_onetable_clause.add_negtive((i + 1, k + 1))
            symbols.append((i + 1, j + 1))
            symbols.append((i + 1, k + 1))
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
            enemy_clause = Clause()
            enemy_clause.add_negtive((a, i + 1))
            enemy_clause.add_negtive((b, i + 1))
            symbols.append((a, i + 1))
            symbols.append((b, i + 1))
            sentence.append(enemy_clause)
    elif tokens[-1] == 'F':
        a = int(tokens[0])
        b = int(tokens[1])
        for i in range(tables):
            for j in range(tables):
                if i != j:
                    friend_clause = Clause()
                    friend_clause.add_negtive((a, i + 1))
                    friend_clause.add_negtive((b, j + 1))
                    symbols.append((a, i + 1))
                    symbols.append((b, j + 1))
                    sentence.append(friend_clause)

model = Model(dict())
print dpll(sentence, symbols, model)

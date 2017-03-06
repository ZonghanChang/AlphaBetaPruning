#!/usr/bin/env python

from copy import deepcopy
import random

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

    def is_positive(self, symbol):
        return symbol in self.positive_symbol

    def is_negtive(self, symbol):
        return symbol in self.negtive_symbol

    def is_unit_clause(self):
        return len(self.positive_symbol) + len(self.negtive_symbol) == 1

    def get_symbols(self):
        symbols = list()
        for symbol in self.positive_symbol:
            symbols.append(symbol)
        for symbol in self.negtive_symbol:
            symbols.append(symbol)
        return symbols

class Model:

    def __init__(self, values):
        self.assigments = dict()
        self.assigments.update(values)

    def get_value(self, symbol):
        if symbol in self.assigments:
            return self.assigments[symbol]
        return None

    def union(self, symbol):
        m = Model(self.assigments)
        # m.assigments.update(self.assigments)
        m.assigments[symbol] = b
        return m

    def union_inplace(self, symbol, b):
        self.assigments[symbol] = b
        return self

    def flip(self, symbol):
        if self.assigments[symbol] is True:
            return self.union_inplace(symbol, False)
        if self.assigments[symbol] is False:
            return self.union_inplace(symbol, True)
        return self

    def remove(self, symbol):
        del self.assigments[symbol]

    def satisfies(self, clauses):
        for clause in clauses:
            value = self.determin_value(clause)
            if value is not True:
                return False

        return True

    def determin_value(self, clause):
        has_unassigned = False
        for positive in clause.get_positive():
            if positive in self.assigments:
                value = self.assigments[positive]
                if value is True:
                    return True
            else:
                has_unassigned = True

        for negtive in clause.get_negtive():
            if negtive in self.assigments:
                value = self.assigments[negtive]
                if value is False:
                    return True
            else:
                has_unassigned = True

        if has_unassigned:
            return None

        return False


def every_clause_true(clauses, model):
    return model.satisfies(clauses)


def some_clause_false(clauses, model):
    for clause in clauses:
        value = model.determin_value(clause)
        if value is False:
            return True
    return False


def find_pure_symbol(symbols, clauses, model):

    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if not found_pos and s in c.get_positive():
                found_pos = True
            if not found_neg and s in c.get_negtive():
                found_neg = True
        if found_pos != found_neg:
            return s, found_pos
    return None, None

    # symbols_to_keep = deepcopy(symbols)
    # candidate_pure_positive_symbols = set()
    # candidate_pure_negtive_symbols = set()
    # for clause in clauses:
    #     if model.determin_value(clause) is True:
    #         continue
    #     for p in clause.get_positive():
    #         if p in symbols_to_keep:
    #             candidate_pure_positive_symbols.add(p)
    #     for n in clause.get_negtive():
    #         if n in symbols_to_keep:
    #             candidate_pure_negtive_symbols.add(n)
    #
    # for s in symbols_to_keep:
    #     if s in candidate_pure_positive_symbols and s in candidate_pure_negtive_symbols:
    #         candidate_pure_positive_symbols.remove(s)
    #         candidate_pure_negtive_symbols.remove(s)
    #
    # if len(candidate_pure_positive_symbols) > 0:
    #     return next(iter(candidate_pure_positive_symbols)), True
    #
    # if len(candidate_pure_negtive_symbols) > 0:
    #     return next(iter(candidate_pure_negtive_symbols)), False

    # return None, None

def find_unit_clause(clauses, model):
    unassigned = None
    result = None, None
    for clause in clauses:
        if model.determin_value(clause) is None:
            for symbol in clause.get_symbols():
                value = model.get_value(symbol)
                if value is None:
                    if unassigned is None:
                        unassigned = symbol
                    else:
                        unassigned = None
                        break
            if unassigned is not None:
                positive = clause.is_positive(unassigned)
                result = unassigned, positive
    return result


def dpll(clauses, symbols, model):

    if every_clause_true(clauses, model):
        return True
    if some_clause_false(clauses, model):
        return False

    symbol, value = find_pure_symbol(symbols, clauses, model)
    if symbol is not None:
        symbols.remove(symbol)
        return dpll(clauses, symbols, model.union_inplace(symbol, value))
    symbol = None
    symbol, value = find_unit_clause(clauses, model)
    if symbol is not None:
        symbols.remove(symbol)
        return dpll(clauses, symbols, model.union_inplace(symbol, value))

    copy = deepcopy(symbols)
    p = next(iter(copy))
    copy.remove(p)
    rest = copy
    value_false = dpll(clauses, rest, model.union_inplace(p, False))
    value_true = dpll(clauses, rest, model.union_inplace(p, True))
    model.remove(p)
    return value_false or value_true


def walkSAT(clauses, p, max_flips, symbols):
    model = random_assignment(symbols)
    for i in range(0, max_flips):
        if model.satisfies(clauses):
            return model

        clause = randomly_select_false_clause(clauses, model)
        if random.random() < p:
            model = model.flip(random_select_symbol(clause))
        else:
            model = flip_symbols_maximizes_satisfied_clauses(clause, clauses, model)
    return None


def flip_symbols_maximizes_satisfied_clauses(clause, clauses, model):
    symbols = clause.get_symbols()
    max_clause_satisfied = -1
    result = model
    for symbol in symbols:
        flipped_model = model.flip(symbol)
        clause_satisfied = 0
        for clause in clauses:
            if flipped_model.determin_value(clause) is True:
                clause_satisfied += 1
        if clause_satisfied > max_clause_satisfied:
            result = flipped_model
            max_clause_satisfied = clause_satisfied
    return result


def random_assignment(symbols):
    model = Model(dict())

    for symbol in symbols:
        model.union_inplace(symbol, bool(random.getrandbits(1)))
    return model


def randomly_select_false_clause(clauses, model):
    count = 0
    result = None
    for clause in clauses:
        if model.determin_value(clause) is False:
            count += 1
            if random.randrange(count) == 0:
                result = clause
    return result


def random_select_symbol(clause):
    symbols = clause.get_symbols()
    return symbols[random.randrange(len(symbols))]

file = open("input.txt", "r")
first_line = file.readline().strip('\r\n').split()
guests = int(first_line[0])
tables = int(first_line[1])
sentence = list()
symbols = set()
for i in range(guests):
    in_table_clause = Clause()
    for j in range(tables):
        in_table_clause.add_positive((i + 1, j + 1))
        symbols.add((i + 1, j + 1))
        for k in range(j + 1, tables):
            in_onetable_clause = Clause()
            in_onetable_clause.add_negtive((i + 1, j + 1))
            in_onetable_clause.add_negtive((i + 1, k + 1))
            symbols.add((i + 1, j + 1))
            symbols.add((i + 1, k + 1))
            sentence.append(in_onetable_clause)
    sentence.append(in_table_clause)

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
            symbols.add((a, i + 1))
            symbols.add((b, i + 1))
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
                    symbols.add((a, i + 1))
                    symbols.add((b, j + 1))
                    sentence.append(friend_clause)

model = Model(dict())
symbols_copy = list(symbols)
symbols_copy.sort(key=lambda tup: tup[0])

outfile = open('output.txt', 'w')
if dpll(sentence, symbols, model) is False:
    outfile.write('no')
else:
    outfile.write('yes\n')
    arrangement = walkSAT(sentence, 0.5, 100000, symbols_copy)
    for symbol in symbols_copy:
        if arrangement.assigments[symbol] is True:
            outfile.write(str(symbol[0]) + ' ' + str(symbol[1]) + '\n')
#!/usr/bin/python
import re

class UtilityNode:
    pass

class DecisionNode:
    pass

def processvariable(str, dic):
    tokens = str.split(",")
    for token in tokens:
        pair = token.split("=")
        variable = pair[0].strip()
        value = pair[1].strip()
        dic[variable] = True if value == "+" else False

def prcessprobabilityquery(query):
    queryvariables = dict()
    observedvariables = dict()
    if query.find("|") == -1:
        processvariable(query, queryvariables)
    else:
        tokens = query.split("|")
        processvariable(tokens[0], queryvariables)
        processvariable(tokens[1], observedvariables)
    return queryvariables, observedvariables

def main():
    querys, bn = readfile()
    for query in querys:
        if query[0] == "P":
            queryvariables, observedvariables = prcessprobabilityquery(query[2:-1])
            q = enumeration_ask(queryvariables, observedvariables, bn)


def enumeration_ask(queryvariables, observedvariables, bn):
    distribution = list()
    allvaribles = list(bn.getvariables().reverse())
    for queryvariable in queryvariables:

        observedvariables[queryvariable] = True
        ptrue = enumeration_all(allvaribles, observedvariables, bn)
        observedvariables[queryvariable] = False
        pfalse = enumeration_all(allvaribles, observedvariables, bn)

        distribution.append(ptrue)
        distribution.append(pfalse)
    return 1.0 / sum(distribution)

def enumeration_all(vars, observedvariables, bn):
    if len(vars) == 0:
        return 1.0
    Y = vars.pop()
    if Y in observedvariables:
        pass
    else:
        pass


def readfile():
    file = open("input.txt", "r")
    graph = Graph()
    querys = list()
    while True:
        line = file.readline().strip("\n\r")
        if line.find("******") != -1:
            break
        querys.append(line)

    endofnodes = False

    while True:
        if endofnodes:
            break
        block = list()
        while True:
            line = file.readline().strip("\n\r")
            if not line or line.find("******") != -1:
                endofnodes = True
                break
            if line.find("***") != -1:
                break
            block.append(line)
        graph.addnode(block)

    line = file.readline().strip("\n\r")
    if line:
        utilityparent = line.split("|")[1]
        p = re.compile(r' +')
        utilityparent = p.split(utilityparent.strip())

        while True:
            line = file.readline().strip("\n\r")
            if not line:
                break
            tokens = p.split(line.strip())


    return querys, graph


class Graph:
    def __init__(self):
        self.nodes = dict()
        self.variableset = list()

    def getvariableset(self):
        return self.variableset

    def addutility(self):
        pass

    def addnode(self, block):
        s = block[0]
        if s.find("|") != -1:
            edge = s.split("|")
            node = edge[0].strip()
            parentnodeslist = edge[1].strip().split(" ")
            parentnodesset = set(parentnodeslist)
            for line in block[1:]:
                tokens = line.strip().split(" ")
                p = tokens[0]
                positivelist = list()
                for i in range(1,len(tokens)):
                    if tokens[i] == "+":
                        positivelist.append(parentnodeslist[i - 1])

            self.variableset.append(node)
        else:
            self.variableset.append(s)
            if block[1].find("decision") != -1:
                pass
            else:
                parentnodeslist = list()

if __name__ == '__main__':
    main()
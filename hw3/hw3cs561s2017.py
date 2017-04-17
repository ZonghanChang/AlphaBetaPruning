#!/usr/bin/python
import re

class Node:
    def __init__(self):
        self.parents = list()
        self.probability = dict()
        self.utility = dict()
    def addutility(self, parent, utility):
        self.utility[parent] = utility

    def getutility(self, parent):
        return self.utility[parent]

    def addprobability(self, parent, probability):
        self.probability[parent] = probability

    def getprobability(self, parent):
        return self.probability[parent]

    def addparent(self, parent):
        self.parents.append(parent)

    def hasparent(self, name):
        return name in self.parents


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
            print '%.2f' %q
        elif query[0] == "E":
            pass
        elif query[0] == "M":
            pass

def generateallconditions(result, temp, queryvariables, pos):
    if len(temp) == len(queryvariables):
        result.append(dict(temp))
        return

    temp[queryvariables[pos]] = True
    generateallconditions(result, temp, queryvariables, pos + 1)
    temp[queryvariables[pos]] = False
    generateallconditions(result, temp, queryvariables, pos + 1)
    del temp[queryvariables[pos]]

def enumeration_ask(queryvariables, observedvariables, bn):
    pquery = 0
    distribution = list()
    allvaribles = list(bn.getvariables())
    allvaribles.reverse()
    allconditions = list()
    generateallconditions(allconditions, dict(), list(queryvariables), 0)

    for condition in allconditions:
        o1 = dict(observedvariables)
        for k, v in condition.items():
            o1[k] = v
        p = enumeration_all(allvaribles, o1, bn)
        if cmp(condition, queryvariables) == 0:
            pquery += p
        distribution.append(p)
    return pquery * 1.0 / sum(distribution)

def enumeration_all(vars, observedvariables, bn):
    if len(vars) == 0:
        return 1.0
    Yname = vars.pop()
    Ynode = bn.getnode(Yname)
    templist = list()
    for parent in Ynode.parents:
        if observedvariables[parent]:
            templist.append(parent)

    if Yname in observedvariables:
        if observedvariables[Yname]:
            p = float(Ynode.getprobability(tuple(templist))) * enumeration_all(vars, observedvariables, bn)
            vars.append(Yname)
            return p
        else:
            p = (1 - float(Ynode.getprobability(tuple(templist)))) * enumeration_all(vars, observedvariables, bn)
            vars.append(Yname)
            return p
    else:
        observedvariables[Yname] = True
        ptrue = float(Ynode.getprobability(tuple(templist))) * enumeration_all(vars, observedvariables, bn)
        observedvariables[Yname] = False
        pfalse = (1 - float(Ynode.getprobability(tuple(templist)))) * enumeration_all(vars, observedvariables, bn)
        vars.append(Yname)
        p = ptrue + pfalse
        return p

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
        self.variablelist = list()

    def getnode(self, name):
        return self.nodes[name]

    def getvariables(self):
        return self.variablelist

    def addutility(self):
        pass

    def addnode(self, block):
        s = block[0]
        node = Node()
        nodename = ""
        if s.find("|") != -1:

            edge = s.split("|")
            nodename = edge[0].strip()
            parentnodeslist = edge[1].strip().split(" ")
            for parentnode in parentnodeslist:
                node.addparent(parentnode)
            parentnodesset = set(parentnodeslist)

            for line in block[1:]:
                tokens = line.strip().split(" ")
                p = tokens[0]
                positivelist = list()
                for i in range(1, len(tokens)):
                    if tokens[i] == "+":
                        positivelist.append(parentnodeslist[i - 1])
                node.addprobability(tuple(positivelist), p)
            self.nodes[nodename] = node
            self.variablelist.append(nodename)
        else:
            nodename = s
            if block[1].find("decision") != -1:
                node.addprobability(tuple(), 1)
            else:
                p = block[1].strip()
                node.addprobability(tuple(), p)
            self.nodes[nodename] = node
            self.variablelist.append(s)
if __name__ == '__main__':
    main()
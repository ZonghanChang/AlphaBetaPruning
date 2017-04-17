#!/usr/bin/python
import re
class Utility:
    def __init__(self):
        self.variables = list()
        self.utility = dict()

    def storevariables(self, v):
        self.variables = v

    def addutility(self, name, u):
        self.utility[name] = u

    def getutility(self, name):
        return float(self.utility[name])

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
                node.isutility = True
            else:
                p = block[1].strip()
                node.addprobability(tuple(), p)
            self.nodes[nodename] = node
            self.variablelist.append(s)

class Node:
    def __init__(self):
        self.parents = list()
        self.probability = dict()
        self.utility = dict()
        self.isutility = False

    def addutility(self, parent, utility):
        self.utility[parent] = utility

    def getutility(self, parent):
        return self.utility[parent]

    def addprobability(self, parent, probability):
        self.probability[parent] = probability

    def getprobability(self, parent):
        return float(self.probability[parent])

    def getprobabilitybar(self, parent):
        if self.isutility:
            return 1
        else:
            return 1 - float(self.probability[parent])

    def addparent(self, parent):
        self.parents.append(parent)

    def hasparent(self, name):
        return name in self.parents


def processvariable(str, dic, queryvariablesorder):
    tokens = str.split(",")
    for token in tokens:
        pair = token.split("=")
        variable = pair[0].strip()
        value = pair[1].strip()
        queryvariablesorder.append(variable)
        dic[variable] = True if value == "+" else False

def processpquery(query):
    queryvariablesorder = list()
    queryvariables = dict()
    observedvariables = dict()
    if query.find("|") == -1:
        processvariable(query, queryvariables, queryvariablesorder)
    else:
        tokens = query.split("|")
        processvariable(tokens[0], queryvariables, queryvariablesorder)
        processvariable(tokens[1], observedvariables, list())
    return queryvariablesorder, queryvariables, observedvariables

def calP(query, bn):
    queryvariablesorder, queryvariables, observedvariables = processpquery(query)
    pquery, distribution = enumeration_ask(queryvariablesorder, queryvariables, observedvariables, bn)
    sum = 0
    for k, v in distribution.items():
        sum += v
    return pquery * 1.0 / sum

def processequery(query):
    observedvariables = dict()
    if query.find("|") == -1:
        processvariable(query, observedvariables, list())
    else:
        tokens = query.split("|")
        processvariable(tokens[0], observedvariables, list())
        processvariable(tokens[1], observedvariables, list())
    return observedvariables

def calEU(utility, query, bn):
    queryvariables = dict()
    observedvariables = processequery(query)
    for variable in utility.variables:
        queryvariables[variable] = True
    pquery, distribution = enumeration_ask(utility.variables, queryvariables, observedvariables, bn)
    sum = 0
    eu = 0
    for k, v in distribution.items():
        sum += v
    for k, v in distribution.items():
        eu += utility.getutility(k) * distribution[k] * 1.0 / sum
    return eu

def main():
    querys, bn, utility = readfile()
    for query in querys:
        if query[0] == "P":
            q = calP(query[2:-1], bn)
            print '%.2f' %q
        elif query[0] == "E":
            u = calEU(utility, query[3:-1], bn)
            print int(round(u))
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
def dicttotuple(order, dic):
    res = list()
    for item in order:
        if dic[item]:
            res.append(item)
    return tuple(res)

def enumeration_ask(queryvariablesorder, queryvariables, observedvariables, bn):
    pquery = 0
    distribution = dict()
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
            pquery = p
        t = dicttotuple(queryvariablesorder, condition)
        distribution[t] = p
    return pquery, distribution

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
            p = Ynode.getprobability(tuple(templist)) * enumeration_all(vars, observedvariables, bn)
            vars.append(Yname)
            return p
        else:
            p = Ynode.getprobabilitybar(tuple(templist)) * enumeration_all(vars, observedvariables, bn)
            vars.append(Yname)
            return p
    else:
        observedvariables[Yname] = True
        ptrue = Ynode.getprobability(tuple(templist)) * enumeration_all(vars, observedvariables, bn)
        observedvariables[Yname] = False
        pfalse = Ynode.getprobabilitybar(tuple(templist)) * enumeration_all(vars, observedvariables, bn)
        del observedvariables[Yname]
        vars.append(Yname)
        p = ptrue + pfalse
        return p

def readfile():
    file = open("input.txt", "r")
    graph = Graph()
    utility = Utility()
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
        utility.storevariables(utilityparent)
        while True:
            line = file.readline().strip("\n\r")
            if not line:
                break
            tokens = line.strip().split(" ")
            u = tokens[0]
            positivelist = list()
            for i in range(1, len(tokens)):
                if tokens[i] == "+":
                    positivelist.append(utilityparent[i - 1])
            utility.addutility(tuple(positivelist), u)

    return querys, graph, utility

if __name__ == '__main__':
    main()
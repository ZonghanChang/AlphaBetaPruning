#!/usr/bin/python
import re
class UtilityNode:
    pass

class DecisionNode:
    pass


def main():
    graph = readfile()


def readfile():
    file = open("input.txt", "r")
    graph = Graph()

    while True:
        line = file.readline().strip("\n\r")
        if line.find("******") != -1:
            break

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


    return graph


class Graph:
    def __init__(self):
        self.nodes = dict()

    def addutility(self):
        pass

    def addnode(self, block):
        pass

if __name__ == '__main__':
    main()
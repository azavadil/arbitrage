import urllib2
import math
from collections import deque
import copy

import csv


def makeFile():
    
    file = r"http://quote.yahoo.com/d/quotes.csv?s=EURCAD=X+CADEUR=X+EURUSD=X+USDEUR=X+EURJPY=X+JPYEUR=X+USDCAD=X+CADUSD=X+USDJPY=X+JPYUSD=X+CADJPY=X+JPYCAD=X+&f=sl1&e=.csv"

    fxfile = urllib2.urlopen(file)
    fieldheaders = ["fxpair","fxrate"]
    reader = csv.DictReader(fxfile,fieldnames=fieldheaders)

    return reader

def convertToDictionary(fxCsvReader):

    result = {}
    for row in fxCsvReader:

        pairIdentifier = row["fxpair"]
        fxrate = float(row["fxrate"])

        pairIdentifier = pairIdentifier[0:3] + "_" + pairIdentifier[3:6]
        result[pairIdentifier] = fxrate

    return result
        




def makeGraph(fxData):
    """ (dictionary) -> WgtGraph
    makeGraph takes properly formatted dictionary and returns a WgtGraph
    """ 
    G = WgtGraph()
    for key in fxData.keys():
        tokens = key.split('_')
        if tokens[0] != tokens[1]:
            G.addEdge( DirectedEdge(tokens[0], tokens[1], -math.log(fxData[key])) )
    return G

class DirectedEdge(object):
    """
    DirectedEdge represents a weighted edge. v represents the home vertex. w represents the away vertex
    """

    def __init__(self, v, w, weight):
        self._v = v
        self._w = w
        self._weight = weight

    def fromVertex(self):
        return self._v

    def toVertex(self):
        return self._w

    def weight(self):
        return self._weight

    def __str__(self):
        return "fromVertex: {0}, toVertex: {1}, weight: {2}".format(self._v, self._w, self._weight)

class WgtGraph(object):
    """
    WgtGraph is an adjacency list representation of a weighted digraph. A list of of all outgoing
    edges is maintained for each vertex
    """
    def __init__(self):
        self._numEdges = 0
        self._numVertices = 0
        self._adjList = {}
        
    def addEdge(self, graphEdge):
        """ (DirectedEdge) -> Nonetype
        """
        if not graphEdge.fromVertex() in self._adjList:
            self._adjList[graphEdge.fromVertex()] = []
            self._numVertices += 1
        self._adjList[graphEdge.fromVertex()].append(graphEdge)

        self._numEdges += 1
        
    def neighbors(self, vertex):
        """(str)-> list
        neighbors returns a list of all outgoing edges for the specified vertex
        """
        return self._adjList.get(vertex)

    def vertices(self):
        """()-> list
        vertices returns a list of vertices with outgoing edges
        """ 
        return self._adjList.keys()

    def numVertices(self):
        """()->int"""
        return self._numVertices

    def adjList(self):
        """()->{}"""
        return self._adjList
    
    def __str__(self):
        toString = ""
        for vertex in self.vertices():
            toString += vertex + "\n"
            for edge in self.neighbors(vertex):
                toString += str(edge) + "\n"
        return toString

class WgtDirectedCycle(object):
    """Finds a directed cycle in a weighted digraph"""
    def __init__(self, G):
        self._explored = set()
        self._edgeTo = {}
        self._onStack = set()
        self._cycle = []
        for vertex in G.vertices():
            if vertex not in self._explored: self.dfs(G, vertex)
            

    def dfs(self, G, vertex):
        """(WgtGraph, str)-> Nonetype
        Internal class method. depth first search to find directed cycle
        """ 
        self._onStack.add(vertex)
        self._explored.add(vertex)

        if vertex in G.adjList():
            for edge in G.neighbors(vertex):
                toVertex = edge.toVertex()

                ## short circuit if cycle found
                if self._cycle != []: return 
            
                ## if a new vertex found, recur
                elif toVertex not in self._explored:
                    self._edgeTo[toVertex] = edge
                    self.dfs(G, toVertex)

                elif toVertex in self._onStack:
                    while edge.fromVertex() != toVertex:
                        self._cycle.append(edge)
                        edge = self._edgeTo[edge.fromVertex()]
                    self._cycle.append(edge)

        self._onStack.remove(vertex)

    def hasCycle(self):
        """ () -> bool
        hasCycle returns true if a directed cycle found
        """
        return self._cycle != []

    def cycle(self):
        """ () -> list """ 
        return self._cycle
    

class BellmanFord(object):

    def __init__(self, G, source):
        """ (WgtGraph, str) -> BellmanFord object
        takes a WgtGraph and source vertex and runs the BellmanFord shortest paths algorithm.
        Returns an object that client can query
        """
        self._distTo = dict([(vertex, float('inf')) for vertex in G.vertices()]) 
        self._distTo[source] = 0
        self._edgeTo = {}
        self._onQueue = dict([(vertex, False) for vertex in G.vertices()])
        self._cycle = []
        self._count = 1
        
        self._q = deque()
        self._q.append(source)
        self._onQueue[source] = True

        while(len(self._q) > 0 and not self.hasNegativeCycle()):
            vertex = self._q.popleft()
            self._onQueue[vertex] = False
            self.relax(G, vertex)
            

    def relax(self, G, vertex):
        """(WgtGraph, str) -> Nonetype
        Internal class method
        """
        epsilon = 0.0001
        for edge in G.neighbors(vertex):
            toVertex = edge.toVertex()  
            if self._distTo[toVertex] > self._distTo[vertex] + edge.weight() + epsilon:
                self._distTo[toVertex] = self._distTo[vertex] + edge.weight()
                self._edgeTo[toVertex] = edge
                if not self._onQueue[toVertex]:
                    self._q.append(toVertex)
                    self._onQueue[toVertex] = True
            self._count += 1
            if self._count % 2*G.numVertices() == 0:
                self.findNegativeCycle()

    def findNegativeCycle(self):
        """() -> Nonetype. Internal Class method
        Builds the current shortest paths tree from edgeTo.
        Calls WgtDirectedCycle to determine if a cycle exists
        """
        spt = WgtGraph()
       
        for edge in self._edgeTo.values():
            spt.addEdge(edge)

        finder = WgtDirectedCycle(spt)
        self._cycle = finder.cycle()

    def hasNegativeCycle(self):
        """ () -> bool
        hasNegativeCycle returns true if cycle was found, false otherwise
        """
        return self._cycle != []

    def getCycle(self):
        """ () -> list """ 
        return self._cycle  
  
def main():

    yahooCSV = makeFile()
    fxData = convertToDictionary(yahooCSV)
    
    G = makeGraph(fxData)
    
    bf = BellmanFord(G, G.vertices()[0])

    if bf.hasNegativeCycle():
        result = bf.getCycle()
        print "Start with 100 units {0}".format(result[-1].fromVertex())
        balance = 100
        while result:
            edge = result.pop()
            key = edge.fromVertex() + "_" + edge.toVertex()
            balance = balance * fxData[key]
            print "{0} to {1} @ {2} = {3:.2f} {4}".format(edge.fromVertex(), edge.toVertex(), fxData[key], balance, edge.toVertex())
    else:
        print "No arbitrage found"

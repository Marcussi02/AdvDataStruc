from fileinput import filename
import sys

class DisjointSet:
    def __init__(self,n):
        self.parent = [[-1,None] for _ in range(n)]

    def findSmallest(self,a):
        if self.parent[a] < 0:
            return a
        else:
            subRoot = self.parent[a]
            subRoot = self.findSmallest(subRoot)

    def unionByHeight(self,a, b):
        rootA = self.findSmallest(a)
        rootB = self.findSmallest(b)
        if (rootA==rootB):
            return

        heightA = -self.parent[rootA]
        heightB = -self.parent[rootB]
        if heightA > heightB:
            self.parent[rootB] = rootA
        elif heightB > heightA:
            self.parent[rootA] = rootB
        else:
            self.parent[rootA] = rootB
            self.parent[rootB] = -(heightB+1)

def readFile(fileName):
    #lst = ["V E W", "V E W"...]
    lst = []
    f = open(fileName,"r")
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        lst.append(line)
    return lst

def kruskalMST(lst):
        lst.sort()
        for i in range()
        pass

if __name__ == "__main__":
    argument_01 = sys.argv[1]
    lstVE = filename
    line1 = lstVE[0].split(" ")
    lst = []
    V = line1[0]
    E = line1[1]
    for i in range(1,E+1):
        v,e,w =lstVE[i].split(" ")
        lst.append([w,v,e])
    
    
    
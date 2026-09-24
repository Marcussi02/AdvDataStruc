import sys

class DisjointSet:
    def __init__(self,n):
        # parent[x] < 0 marks a root; its magnitude is the tree height
        self.parent = [-1 for _ in range(n)]

    def findSmallest(self,a):
        if self.parent[a] < 0:
            return a
        else:
            return self.findSmallest(self.parent[a])

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
    # DRAFT: main loop not finished.
    # Plan: sort edges by weight, union endpoints that are in different sets.
    lst.sort()
    raise NotImplementedError("Kruskal main loop is still a draft")

if __name__ == "__main__":
    argument_01 = sys.argv[1]
    lstVE = readFile(argument_01)
    line1 = lstVE[0].split(" ")
    lst = []
    V = int(line1[0])
    E = int(line1[1])
    for i in range(1,E+1):
        v,e,w =lstVE[i].split(" ")
        lst.append([w,v,e])
    
    
    
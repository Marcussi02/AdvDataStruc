"""DRAFT: Ukkonen-style generalised suffix tree - unfinished.

Kept as a record of the design (nodes, edges, global end pointer).
"""


class Node:
    isLeaf = False
    children = [None] * 27
    
class Edge(start,end):
    incoming_edge_info = None
    link = Node()
    start = start
    end = end

class EndMyLife:
    def __init__(self) -> None:
        my_end = 0
    def increment():
        self.end += 1
text = "hello"

def suffix(text):
    i = 1
    while i <= len(text):
        j = 0
        while j < i:
            suffix = text[j:i]

            pointer = tree.traverse(suffix)

            #rule1: extend leaf
            if pointer.isLeaf == True:
                pass
            #rule2: branch
            elif pointer.isLeaf == False and text[i] != text[pointer]:
                pass
            elif text[i] == text[pointer]:
                pass

def ukkonen(str):
    str = str + "$"
    n = len(str)
    construct 
    AN = root
    rem = None
    lastJ = 1
    globalEnd = 1
    for i in range(1, n-1):
        globalEnd = globalEnd + 1
        for j in range(lastJ+1, i+1):
            traverse()
            makeExtension()
            resolveSuffixLinks()
            moveToNextExtension()
    return root
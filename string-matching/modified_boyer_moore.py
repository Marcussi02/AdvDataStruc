import sys

def boyerMoore(txt, pat):
    z = zalgro(txt)
    bc = BC(pat)
    gs = GS(pat)
    mp = MP(pat,z)
    m = len(pat)
    n = len(txt)
    i = 0
    while i < n:
        j = m - 1
        while j >= 0:
            #when k is index of mismatch, BC(k-BC[x]) or GS(m-GS[k+1]) whichever shift more, if GS[k+1] == 0, MP
            #when pat is matched, m-MP[2]
            if txt[i+j] == pat[j]:
                j -= 1
            else:
                k = j-1
                BCShift = bc[ord(pat[k])][k]
                GSShift = gs[j]
                if BCShift > GSShift:
                    i = i + j - BCShift
                    j = m - 1
                else:
                    if GS[k+1] == 0:
                        q = MP[j]
                        i = m - q
                        j = i + m
                    else: #GSShift
                        suffStart = GSShift - 1
                        suffEnd = GSShift - 1 - j
                        i = i + m - GSShift
                        j = m - 1
            #BC GS MP
        shift = 0
        i += shift
    return result

def zalgro(txt):
    zArray = [None] * len(txt)
    zArray[0] = len(txt)
    zBoxLeft = 0
    zBoxRight = 0
    for i in range(1, len(txt)):
        if i > zBoxRight: #case 1
            j = 0
            while i+j < len(txt) and txt[i+j] == txt[j]:
                j += 1
            zBoxLeft = i
            zBoxRight = j
            zArray[i] = j
        else: #case 2
            k = zBoxRight - zBoxLeft - i
            remaining = zBoxRight - i
            if zArray[k] < remaining:
                zArray[i] = zArray[k]
            elif zArray[k] == remaining:
                #start checking from string[i+remaining] with string[zArray[k]+1]
                #if extends over zBox, create new zBox
                j = 0
                while txt[i+remaining+1+j] == txt[remaining+1+j]:
                    j += 1
                if zBoxRight < i + remaining + 1 + j:
                    zBoxLeft = i
                    zBoxRight = i + remaining + 1 + j
                zArray[i] = remaining+j
            else: #zArray[k] > remaining
                zArray[i] = remaining
    return zArray

def BC(pat):
    #bcMatrix[asciicode][posiiton]
    m = len(pat)
    bcMatrix = [[0 for _ in range(m)] for _ in range(95)]
    for i in range(m-1, -1, -1): # length-1, length-2, length-3
        charVal = ord(pat[i])-32
        bcMatrix[charVal][i] = i
        j = i+1
        while j < m and bcMatrix[charVal][j] == 0:
            bcMatrix[charVal][j] = i
            j += 1
    return bcMatrix

def GS(pat):
    m = len(pat)
    revZArray = [None for _ in range(m)]
    revPat = pat[::-1]
    zArray = zalgro(revPat)
    for i in range(m):
        revZArray[i] = zArray[m-1-i]
    GSArray = [0 for _ in range(m+1)]
    for p in range(m-1):
        j = m - revZArray[p] + 1
        GSArray[j] = p
    return GSArray

def MP(pat, zArray):
    m = len(pat)
    MPArray = [None for _ in range(m)]
    for i in range(m-1,-1,-1):
        if zArray[i] + i == m:
            print(pat[i])
            MPArray[i] = zArray[i]
        else:
            print(pat[i])
            MPArray[i] = MPArray[i+1]
    return MPArray

def read_file(filename):
    return filename

def BM(txt, pat):
    print("hello")

# if __name__ == "__main__":
#     argument_00 = sys.argv[0]
#     argument_01 = sys.argv[1]
#     argument_02 = sys.argv[2]

#     BM(read_file(argument_01), read_file(argument_02))
print(zalgro("aabxaabxcaabxaabxay"))
print(MP("fefafafef",zalgro("fefafafef")))
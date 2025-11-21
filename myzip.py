import heapq
import sys
from bitarray import bitarray
def huffman(string):
    lstString = [0 for _ in range(127)]
    heapString = []
    lstBinary = [None for _ in range(127)]
    for i in range(len(string)):
        lstString[ord(string[i])] += 1
    for i in range(127):
        if lstString[i] > 0:
            lstBinary[i] = [chr(i),bitarray()]
            heapString.append([lstString[i],chr(i)])
    heapq.heapify(heapString)
    while len(heapString) > 1:
        pop1 = heapq.heappop(heapString)
        pop2 = heapq.heappop(heapString)
        for i in range(len(pop1[1])):
            char = ord(pop1[1][i])
            lstBinary[char][1].append(0)
        for i in range(len(pop2[1])):
            char = ord(pop2[1][i])
            lstBinary[char][1].append(1)
        comb = [pop1[0]+pop2[0],pop1[1]+pop2[1]]
        heapq.heappush(heapString,comb)
    for i in range(len(lstBinary)):
        if lstBinary[i] != None:
            lstBinary[i][1].reverse()
    return lstBinary

def elias(n):
    outputLst = []
    n += 1
    nBinary = numToBin(n)
    outputLst.append(nBinary)
    nLength = len(nBinary)
    while (nLength > 1):
        nLength -= 1
        nBinary = numToBin(nLength)
        nBinary[0] = 0
        outputLst.append(nBinary)
        nLength = len(nBinary)
    output = bitarray()
    for i in range(len(outputLst)-1,-1,-1):
        output.extend(outputLst[i])
    return output    

def numToBin(n):
    output = bitarray()
    while n > 0 :
        if (n / 2).is_integer():
            output.append(0)
        else:
            output.append(1)
        n = n //2
    output.reverse()
    return output

def numTo8Bit(n):
    output = bitarray()
    while n > 0 :
        if (n / 2).is_integer():
            output.append(0)
        else:
            output.append(1)
        n = n //2
    while len(output) < 8:
        output.append(0)
    output.reverse()
    return output

# print(numToBin(5))
# print(elias(5))

def decElias(bin):
    i = 0
    if bin[i] == 0:
        binLength = 2
        i = 1
    else:
        return 1
    while bin[i] == 0:
        bin[i] = 1
        sumBinLength = 0
        for l in range(binLength):
            sumBinLength += bin[i+l]*2**(binLength-1-l)
        sumBinLength += 1
        i += binLength
        binLength = sumBinLength
    # binLength is the length of the number
    binNum = bitarray()
    for j in range(binLength):
        binNum.append(bin[i+j])
    num = binToNum(binNum) - 1
    return num

def binToNum(bin):
    output = 0
    n = len(bin)
    for i in range(n):
        output += bin[i]*2**(n-1-i)
    return output

def encode(filename, w, l):
    lenBin = elias(len(filename))
    filenameBin = bitarray()
    for i in range(len(filename)):
        charBin = numTo8Bit(ord(filename[i]))
        filenameBin.extend(charBin)
    filesizeBin = elias(12) # needs to be changed
    f = open(filename,'r')
    word = f.readline()
    f.close()
    wordLst = huffman(word)
    huffmanLst = []
    for i in range(len(wordLst)):
        if wordLst[i] != None:
            huffmanLst.append(wordLst[i])
    lenHuffmanBin = elias(len(huffmanLst))
    huffmanBin = bitarray()
    for i in range(len(huffmanLst)):
        huffmanBin.extend(numTo8Bit(ord(huffmanLst[i][0])))
        huffmanBin.extend(elias(len(huffmanLst[i][1])))
        huffmanBin.extend(huffmanLst[i][1])

    lstLZ77 = lz77(word, w, l)
    lz77Bin = bitarray()
    for i in range(len(lstLZ77)):
        lz77Bin.extend(elias(lstLZ77[i][0]))
        lz77Bin.extend(elias(lstLZ77[i][1]))
        j = 0
        while huffmanLst[j][0] != lstLZ77[i][2]:
            j += 1
        lz77Bin.extend(huffmanLst[j][1])
    output = bitarray()
    output.extend(lenBin)
    output.extend(filenameBin)
    output.extend(filesizeBin)
    output.extend(lenHuffmanBin)
    output.extend(huffmanBin)
    output.extend(lz77Bin)
    f = open(filename+".bin", "wb")
    output.tofile(f)
    f.close()

def lz77(txt,w,l):
    txt += "$"
    lstLZ77 = []
    windowIndex, lookIndex = 0, 1
    lstLZ77.append([0,0,txt[0]])
    while lookIndex < len(txt)-1:
        if lookIndex + l - 1 < len(txt) - 1:
            lookEndIndex = lookIndex + l- 1
        else:
            lookEndIndex = len(txt) - 1
        windowEndIndex = lookIndex-1
        windowText = ""
        lookText = ""
        for x in range(windowIndex,windowEndIndex+1):
            windowText += txt[x]
        for x in range(lookIndex,lookEndIndex+1):
            lookText += txt[x]
        zLst = zalgo(windowText + lookText,len(windowText),len(lookText))
        longestSubstring = 0
        for i in range(len(zLst)):
            if zLst[i] >= longestSubstring:
                longestSubstring = zLst[i]
                offset = len(windowText) - i
        lookIndex += longestSubstring + 1
        if lookIndex - w >= 0:
            windowIndex = lookIndex - w
        else:
            windowIndex = 0
        lstLZ77.append([offset,longestSubstring,txt[lookIndex-1]])
    return lstLZ77

def zalgo(txt, lenWindow, lenLook):
    zArray = [None] * lenWindow #intialise zArray
    zBoxLeft = -1
    zBoxRight = -1
    k = 0
    for i in range(lenWindow):
        if i > zBoxRight: # case 1 if it is outside the zBox
            startPointer = i #length of matching prefix string
            endPointer = lenWindow
            while endPointer < len(txt) and txt[startPointer] == txt[endPointer]: # matching the characters from the prefix and suffix of i
                startPointer += 1
                endPointer += 1
            endPointer -= 1 # endPointer now contains index of last matching
            zBoxLeft = i # assigned zBox for left and right
            # zBoxRight = endPointer
            zArray[i] = startPointer - i # store the length of matching suffix
        else:
            k = lenWindow + i - zBoxLeft #calculated index of the prefix in comparison to the suffix one 
            remaining = zBoxRight - i + 1 #calculated remaining characters in the zBox
            if zArray[k] > remaining: # case 2a
                zArray[i] = remaining
            elif zArray[k] < remaining: # case 2b
                zArray[i] = zArray[k]
            else: #zArray[k] == remaining case 2c
                startPointer = 0 + remaining 
                endPointer = i + remaining
                while endPointer < len(txt) and txt[startPointer] == txt[endPointer]: # matching the suffix with the prefix outside the zBox
                    startPointer += 1
                    endPointer += 1
                endPointer -= 1
                if endPointer > zBoxRight: # if end pointer is out zBox, create new zBox
                    zBoxLeft = i
                    zBoxRight = endPointer
                zArray[i] = startPointer 
    return zArray

# if __name__ == "__main__":
#     argument_01 = sys.argv[1]
#     argument_02 = sys.argv[2]
#     argument_03 = sys.argv[3]
#     bin = encode(argument_01)
encode("x.asc",6,4)
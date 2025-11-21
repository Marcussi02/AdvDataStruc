import sys
from bitarray import bitarray
def decElias(bin, i):
    if bin[i] == 0:
        binLength = 2
        i += 1
    else:
        return 0, i+1
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
    return num, i + binLength

def binToNum(bin):
    output = 0
    n = len(bin)
    for i in range(n):
        output += bin[i]*2**(n-1-i)
    return output

def bit8ToNum(bin):
    output = 0
    for i in range(8):
        output += bin[i]*2**(8-1-i)
    return output

def decHuffman(bin, numChar,i):
    huffmanLst = []
    for j in range(numChar):
        charBin = bitarray()
        for j in range(8):
            charBin.append(bin[i+j])
        char = chr(bit8ToNum(charBin))
        i += 8
        lenHuffman, i = decElias(bin, i)
        huffmanBin = bitarray()
        for k in range(lenHuffman):
            huffmanBin.append(bin[i+k])
        huffmanLst.append([char,huffmanBin])
        i += lenHuffman
    return huffmanLst,i

def decLZ77(bin, i, filesize, huffman):
    lstLZ77 = []
    wordCount = 0
    while wordCount < filesize:
        offset, i = decElias(bin, i)
        length, i = decElias(bin, i)
        char, i = findChar(bin, i, huffman)
        lstLZ77.append([offset,length,char])
        wordCount += length + 1
    word = ""
    word += lstLZ77[0][2]
    for j in range(1, len(lstLZ77)):
        tup = lstLZ77[j]
        for k in range(tup[1]):
            word += word[len(word)-tup[0]]
        word += tup[2]
    return word, i

def findChar(bin, i, huffman):
    j = 0
    potChar = str(bin[i+j])
    # print(huffman)
    while True:
        for x in range(len(huffman)):
            if bitarray(potChar) == huffman[x][1]:
                char = huffman[x][0]
                i += len(huffman[x][1])
                return char, i
        j += 1
        potChar += str(bin[i+j])

def decHeader(bin):
    # i is the starting index of the next decoding section
    lenHeader, i = decElias(bin, 0)
    fileName = ''
    for _ in range(lenHeader):
        charBin = bitarray()
        for j in range(8):
            charBin.append(bin[i+j])
        fileName += (chr(bit8ToNum(charBin)))
        i += 8
    filesize, i = decElias(bin, i)
    numChar, i = decElias(bin, i)
    huffmanLst, i = decHuffman(bin, numChar, i)
    word, i = decLZ77(bin, i, filesize, huffmanLst)
    f = open(fileName, "w")
    f.write(word)
    f.close()

def decode(filename):
    f = open(filename,"rb")
    while True:
        binaryValue = f.read(-1)
        if not binaryValue:
            break
        bin = binaryValue
    decHeader(bin)

# if __name__ == "__main__":
#     argument_01 = sys.argv[1]
#     decode(argument_01)

decHeader(bitarray("000110011110000010111001100001011100110110001100111010001000110000101010110001001100011000110110111101001001000100000101000001000001001"))
import random
import string
import sys
# True = prime, False = composite
def millerRabinRandomisedPrimality(n):
    if n % 2 == 0 or n == 1:
        return False
    if n == 2 or n == 3:
        return True
    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t//2
    lstRandom = random.sample(range(2,n-1),n-3)
    for i in range(n-3):
        a = lstRandom[i]
        if a**(n-1) % n != 1:
            return False
        for j in range(1,s):
            previous = (a**(2**(j-1)*t))%n
            current = previous**2 % n
            if current == 1:
                break
            if (current == 1) and abs(previous) != 1:
                return False
    return True

def primeOfThree(n):
    if n <= 7 or n % 2 == 0:
        return []
    lstPrimes = []
    for i in range(n):
        if i%2 == 1 and millerRabinRandomisedPrimality(i):
            lstPrimes.append(i)
    for i in range(len(lstPrimes)):
        for j in range(len(lstPrimes)):
            for k in range(len(lstPrimes)):
                if lstPrimes[i] + lstPrimes[j] + lstPrimes[k] == n:
                    return [lstPrimes[i], lstPrimes[j], lstPrimes[k]]
    # lstDP = [[0,[]] for _ in range(n+1)]
    # lstDP[0][0] = 1    
    # for i in range(len(lstPrimes)-1,-1,-1):
    #     for j in range(len(lstDP)-1):
    #         if lstPrimes[i] + lstDP[j][0] <= j and len(lstDP[j][1]) <= 3:
    #             lstDP[j][1].append(lstPrimes[i])
    #             lstDP[j][0] += lstPrimes[i]
    # print(lstPrimes)
    # print(lstDP)
    # for i in range(len(lstPrimes)-1,-1,-1):
    #     if lstPrimes[i] + lstDP[11-lstPrimes[i]][0] == 11 and len(lstDP[11-lstPrimes[i]][1]) == 2:
    #         lstDP[11-lstPrimes[i]][1].append(lstPrimes[i])
    #         return lstDP[11-lstPrimes[i]][1]
    return []

def outputFile(N):
    f = open("output_threeprimes.txt", "w")
    lst = primeOfThree(N)
    output = "{0} {1} {2}".format(lst[0],lst[1],lst[2])
    f.write(output)
    f.close()

# if __name__ == "__main__":
#     argument_01 = sys.argv[1]
#     outputFile(argument_01)
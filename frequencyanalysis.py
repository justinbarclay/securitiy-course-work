def prompt(phrase):
    # grab a file handle based on user input
    filename = input(phrase)
    if len(filename) < 1:
        return ""
    return open(filename)

def printFreq(freq, total):
    # given a dictionary and the length of the source of the dictionary, print out the freuncy of all items in the dictionary
    for key, value in freq.items():
        print(str(key) + ": " + str(value/float(total)))

def genArray(fileHandle):
    #flatMaps the byte file into a single array
    byteArray = []
    for line in encrypted:
        byteArray += line

    return byteArray

def findXMostNGrams(nGrams, x):
    #iterates over a dictionary and returns the x most frequent items in the dictionary as a list of tuples
    if x > len(nGrams):
        return "X is too big"

    xHighest = []
    for i in range(x):
        highest = (0, 0)
        for key, value in nGrams.items():
            if value > highest[1]:
                highest = (key, value)
        nGrams.pop(highest[0])
        xHighest.append(highest)
    return xHighest

def countNGrams(byteArray, size):
    # Given a byte array, it returns a dict of a count of all unique nGrams of a specific size in the array
    start = 0
    end = size
    length =len(byteArray)
    nGrams = {}
    
    if size < 1:
        return "size needs to be greater then one"
    if size > length:
        return "size should be smaller than the length of the file"

    while(end < length):
        nGram = ""
        for num in byteArray[start:end]:
            nGram += "/" + hex(num)
        if nGram in nGrams.keys():
            nGrams[nGram] += 1.0
        else:
            nGrams[nGram] = float(1)
        start += 1
        end += 1
    return nGrams

def getCount(array):
    # given an array, returns a dict of a count of all unique items in the array 
    count = {}
    for num in array:
        if hex(num) in count.keys():
            count[hex(num)] += 1.0
        else:
            count[hex(num)] = float(1)
    return count


if __name__ == "__main__":
    #Examples of how to use some of the functions
    encrypted = open("./cipher_text/ciphertext1", "rb")


    byteArray = genArray(encrypted)
    count = getCount(byteArray)
    threeGrams = countNGrams(byteArray,3)

    print(findXMostNGrams(threeGrams, 20))

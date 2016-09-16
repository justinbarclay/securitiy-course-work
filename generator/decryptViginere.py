import sys

def prompt(phrase):
    filename = input(phrase)
    if len(filename) < 1:
        return ""
    return open(filename, "rb")

def splitHex(char):
    toHex = int(char)
    upperHalf = toHex >> 4
    lowerHalf = toHex & 15
    return upperHalf, lowerHalf

def findMatch(hexMap, byte, column):
    for index, row in enumerate(hexMap):
        if row[column] == byte:
            return index

def findPlain(cipher, key):
    hexMap = [
        [0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe], 
        [0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0], 
        [0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7], 
        [0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa],  
        [0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4],      
        [0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3],     
        [0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1], 
        [0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf], 
        [0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2],                             
        [0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5],                             
        [0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb],                             
        [0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6],                              
        [0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8],                              
        [0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9],                              
        [0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd],                              
        [0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc] 
    ]
    kh, kl = splitHex(key)
    ch, cl = splitHex(cipher)

    return ((findMatch(hexMap, ch, kl) << 4) + findMatch(hexMap, cl, kh))


def vigDecryptText(cipherText, key):
    decrypted = []
    keyLen = len(key)
    # print(keyLen)
    for index, char in enumerate(cipherText):
        decrypted.append(findPlain(char, key[index % keyLen]))
    return decrypted

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

if __name__ == "__main__":
    # The user may pass in a keyfile and ciphertext file throught the command line
    # as decryptViginere keyfile ciphertext
    # if these arguments aren't passed in, it will then prompt the user for
    # the names
    if len(sys.argv) == 3: 
        keyFile = open(sys.argv[1], "rb")
        cipherTextFile = open(sys.argv[2], "rb")
    else:
        keyPhrase = "What is the name of the key file? (please note, only the first line will be read for the key) "
        keyFile = prompt(keyPhrase)
        cipherTextPhrase = "What is the name of the file you would like to decrypt? "
        cipherTextFile = prompt(cipherTextPhrase)

    if type(keyFile) == str and type(cipherTextFile) == str and (len(keyFile) < 1 or len(cipherTextFile) < 1):
        print("\nKey file or plaintext file does not exist\n")
    else:
        mainList = []
        keys = []
        for line in keyFile:
            keys += line
        splitKeys = chunks(keys, 7)
        
        for line in cipherTextFile:
            mainList += line
        i=1
        for key in splitKeys:
            print(key)
            name = "decrypted" + str(i) + ".txt"
            encryptedText = vigDecryptText(mainList, key)
            encrypted = open(name, "wb")
            encrypted.write(bytes(encryptedText))
            encrypted.close()
            i += 1

import sys
import secrets
import string
import hexane as Hexane

def XorCipher(data, key, bool):

    keylen = len(key)
    mapper = map(ord, key)
    intKey = list(mapper)
    array = []

    if bool == "false":
        return bytes(bytearray(((data[i] ^ intKey[i % keylen]) for i in range(0, len(data)) )))
    elif bool == "true":
        for element in data:
            string = bytes(bytearray(((ord(element[i]) ^ intKey[i % keylen]) for i in range(0, len(element)) )))
            array.append(string)
        return array

def ReadFile(inFile):
    try:
        with open(inFile, 'rb') as inFileHandle:

            global imagebytes
            imagebytes = bytearray(inFileHandle.read())
            inFileHandle.close()

        print(" * Input file loaded successfully")

    except IOError:
        print(" ! Error reading input file [{{ {} }}]".format(inFile))
        quit()

    return imagebytes

def WriteFile(outFile, encData):
    try:
        with open(outFile, 'wb') as outFileHandle:
            outFileHandle.write(encData)
            outFileHandle.close()

        print(" * Data written to output successful")

    except IOError:
        print(" ! Error writting data to file [{{ {} }}]".format(outFile))
        quit()

def JoinHex(array):

    encoded = []
    for element in array:
        hex = element.hex()
        string = r"0x" + r"0x".join(hex[n : n +2] + "," for n in range(0, len(hex), 2))
        encoded.append(string + "0x00")

    print("Hex-encoding strings finished")
    return encoded

def ShellForCpp(data):
    every = 60
    lines = []

    for i in range(0, len(data), every):
        lines.append( '"' + data[i : i +every] + '"')
    multiline = '\n'.join(lines)
    return multiline

def RandomKey():
    password = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(24)))
    key = str(password)
    return key


def main():

    inFile = sys.argv[1]
    outFile = sys.argv[2]

    if len(sys.argv) != 3:
        print("Usage: python.exe sodium.py <input_file> <output_file> optional:\"encode\"")
        sys.exit(1)

    masterKey = RandomKey()
    imagebytes = ReadFile(inFile)

    encryptedData = XorCipher(imagebytes, masterKey, "false")
    encryptedApi = XorCipher(Hexane.ApiList, masterKey, "true")

    payloadName = "output.txt"
    apiName = "Hexane.hpp"

    print( " + Writting encrypted payload")
    WriteFile(outFile, encryptedData)
    print( " + Encoding Api strings")

    encodedApi = JoinHex(encryptedApi)
    api = open(apiName, 'w')
    HexaneFormat = Hexane.Hexane.format(*encodedApi )

    api.write(HexaneFormat)

    output = open(payloadName, 'w')
    output.close()

    key = open("keystore.txt", 'w+')
    key.write(masterKey)
    key.close()

    print(" + Key written to keystore")
    print(" + Encoded/Xored data written to {0}".format(payloadName))
    print(" + Key: {0}".format(masterKey))

if __name__ == '__main__':
    main()

# https://github.com/x64nik/shell2xor/blob/main/shell2xor.py
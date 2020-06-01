from BackendSide.Utility.CryptoHash import CryptoHash


HexBinaryTable = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def HexToBinary(hexString):
    binary = ''

    for character in hexString:
        binary += HexBinaryTable[character]

        return binary


def main():
    number = 451
    hexNumber = hex(number)[2:]
    print(f'hexNumber:{hexNumber}')

    binaryNumber = HexToBinary(hexNumber)
    print(f'BinaryNumber:{binaryNumber}')

    originalNumber = int(binaryNumber, 2)
    print(f'OriginalNumber:{originalNumber}')

    hex_to_binary_crypto_hash = HexToBinary(CryptoHash('test-data'))
    print(f'hex_to_binary_crypto_hash: {hex_to_binary_crypto_hash}')


if __name__ == '__main__':
    main()

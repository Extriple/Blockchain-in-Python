import hashlib
# json.dumps () pobiera obiekt json i zwraca ciąg znaków.
import json


# każdy pojedynczy przedmiot na naszej argumentowanej liście w celu wygenerowania zupełnie nowej listy.
# Zdefiniujmy więc tę funkcję nad funkcją skrótu kryptograficznego.
# I będziemy wywoływać ten ciąg przez to, że będzie miał jeden argument danych i wynik pokazania przez
# zwróci Jason, który zrzuca dane, a następnie przekażemy ciąg znaków metodą
# sam jako pierwszy argument funkcji mapy.


def CryptoHash(*args):
    """
    Return sha256 hash of the arg.

    Zwracamy Sha256
    """

    stringArgs = sorted( map(lambda data: json.dumps(data), args) )
    JoinData = ''.join(stringArgs)

    return hashlib.sha256(JoinData.encode('utf-8')).hexdigest()


def main():
    print(f"CryptoHash('one', '2', '[3]'):{CryptoHash('one', 2, [3])}")
    print(f"CryptoHash('2', 'one', '[3]'):{CryptoHash(2, 'one', [3])}")


if __name__ == '__main__':
    main()

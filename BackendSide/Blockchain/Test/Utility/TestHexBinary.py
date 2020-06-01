from BackendSide.Utility.HexToBinary import HexToBinary


# Podczas gdy twierdzimy, że ta ostateczna konwersja powinna być teraz równa pierwotnej liczbie i
# zakłada się, że jeśli odzyskamy oryginalny numer.
# Cóż więc jest hex, że konwersja binarna pomiędzy działa poprawnie.
# W końcu przeszliśmy od liczby całkowitej do reprezentacji ciągu szesnastkowego do reprezentacji ciągu binarnego
# z powrotem z łańcucha binarnego na liczbę całkowitą i na pewno jesteśmy równi oryginałowi

def textHexToBinary():
    originalNumber = 789
    hexNumber = hex(originalNumber)[2:]
    binaryNumber = HexToBinary(hexNumber)

    assert int(binaryNumber, 2) == originalNumber

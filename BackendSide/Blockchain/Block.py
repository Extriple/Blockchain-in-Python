import time
from BackendSide.Utility.CryptoHash import CryptoHash
from BackendSide.Utility.HexToBinary import HexToBinary
from BackendSide.config import MINE_RATE

# Struktura
GENESIS_DATA = {
    'timestamp': 1,
    'lasthash': 'GenesisLastHash',
    'hash': 'GenesisHash',
    'data': [],
    'dificulty': 3,
    'nonce': 'GenesisNonce'

}


class Block:
    """
    Block: unit of storage// jednostka przechowywania.
    Store transaction is a blockchain and support with cryptocurrency

    Blok: jednostka pamięci // jednostka zbioru.
    Transakcja sklepu to blockchain i obsługa kryptowaluty
    """

    def __init__(self, timestamp, lasthash, hash, data, dificulty, nonce):
        self.timestamp = timestamp
        self.lasthash = lasthash
        self.hash = hash
        self.data = data
        self.dificulty = dificulty
        self.nonce = nonce

    # Zwracamy bloki
    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp},'
            f'lasthash: {self.lasthash},'
            f'hash: {self.hash},'
            f'data: {self.data}, '
            f'dificulty:{self.dificulty}, '
            f'nonce:{self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes

        Serializuj blok do słownika jego atrybutów
        """
        return self.__dict__

    @staticmethod
    def mineBlock(lastBlock, data):
        """
        Mine a block based on the given lastblock and data.
        Until a block hash is found that meets the leading 0 proof of work requirement

        Wydobądź blok na podstawie podanego ostatniego bloku i danych.
        Do momentu znalezienia skrótu blokowego, który spełnia wiodące wymaganie 0 dowodu pracy

        """
        # Uzyskujemy czas w nanosekundach oraz tworzymy lasthash
        timestamp = time.time_ns()
        lasthash = lastBlock.hash
        dificulty = Block.adjustDificulty(lastBlock, timestamp)
        nonce = 0
        hash = CryptoHash(timestamp, lasthash, data, dificulty, nonce)

        # Zasadniczo mówimy, że będziemy wykonywać pętlę, dopóki nie uzyskamy wartości skrótu gdzie
        # podłańcuch od zera do poziomu trudności pod względem wycinka jego znaków jest równy zero

        while HexToBinary(hash)[0:dificulty] != '0' * dificulty:
            nonce += 1
            timestamp = time.time_ns()
            dificulty = Block.adjustDificulty(lastBlock, timestamp)
            hash = CryptoHash(timestamp, lasthash, data, dificulty, nonce)

        return Block(timestamp, lasthash, hash, data, dificulty, nonce)

    @staticmethod
    def genesis():
        """
        Generate Genesis block

        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(blockJson):
        """
        Deserialize a blocks json. Back into a block instance
        """
        return Block(**blockJson)

    # Metoda powiązana z MINE_RATE
    @staticmethod
    def adjustDificulty(lastBlock, newTimestamp):
        """
         Calculate the adjust dificulty accornding to the MINE_RATE.
         Increase the difficulty for quickly mine blokcs.
         Decrease the difficulty for slowly mine blocks.

         Oblicz poziom korekty trudności zgodnie z MINE_RATE.
         Zwiększ trudność szybkiego wydobywania bloków.
         Zmniejsz trudność powolnego wydobywania bloków.
        """
        if (newTimestamp - lastBlock.timestamp) < MINE_RATE:
            return lastBlock.dificulty + 1
        if (lastBlock.dificulty - 1) > 0:
            return lastBlock.dificulty - 1
        return 1

    @staticmethod
    def isValidBlock(lastBlock, block):
        """
        Validate block by enforcing the following rules:
        1. The block must have the proper lastHash reference
        2. The block must meet the proof of work requirement
        3. The difficult must only adjust by 1
        4. The block hash must be a valid combination od the block field


        Sprawdź poprawność bloku, egzekwując następujące reguły:
         1. Blok musi mieć poprawne odniesienie lastHash
         2. Blok musi spełniać wymagania dotyczące proof of work
         3. Difficulty musi się dostosować tylko o 1
         4. Skrót blokowy musi być prawidłową kombinacją pola bloku
        """

        if block.lasthash != lastBlock.hash:
            raise Exception('The block lastHash must be correct')

        if HexToBinary(block.hash)[0:block.dificulty] != '0' * block.dificulty:
            raise Exception('proof of work requirement was not met')

        if abs(lastBlock.dificulty - block.dificulty) > 1:
            raise Exception('difficulty must only adjust by 1')
        reworkHash = CryptoHash(
            block.timestamp,
            block.lasthash,
            block.data,
            block.nonce,
            block.dificulty
        )

        if block.hash != reworkHash:
            raise Exception('The block hash must be correct')


def main():
    genesisBlock = Block.genesis()
    badBlock = Block.mineBlock(genesisBlock, 'foo')
    badBlock.lasthash = 'evilData'

    try:
        Block.isValidBlock(genesisBlock, badBlock)
    except Exception as e:
        print(f'isValidBlock:{e}')

    genesisBlock = Block.genesis()
    block = Block.mineBlock(genesisBlock, 'foo')
    print(block)


if __name__ == '__main__':
    main()

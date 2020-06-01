from BackendSide.Blockchain.Block import Block
from BackendSide.Wallet.Transaction import Trasaction
from BackendSide.Wallet.wallet import Wallet
from BackendSide.config import MINING_REWARD_INPUT


class Blockchain:
    """
    Blockchain: public ledger of the transaction
    Implemented list of blocks = set data of transcation

    Blockchain: publiczna księga transakcji
    Zaimplementowana lista bloków = zestaw danych transakcji
    """

    # Uzyskujemy dostęp do wszystkich instacji w klasie blockchaina
    def __init__(self):
        self.chain = [Block.genesis()]

    # Funckja, która będzie dodawała nowe blocki
    def addBlock(self, data):
        self.chain.append(Block.mineBlock(self.chain[-1], data))

    # Zwracamy blockchain
    def __repr__(self):
        return f'Blockchain:{self.chain}'

    def replaceChain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
        1.The incoming chain is longer than the local one
        2. The incoming chain is formatted properly

        Zastąp łańcuch lokalny łańcuchem przychodzącym, jeśli mają zastosowanie następujące warunki:
         1. Łańcuch przychodzący jest dłuższy niż łańcuch lokalny
         2. Łańcuch przychodzący jest poprawnie sformatowany
         """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')

        try:
            Blockchain.isValidChain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chainJson):
        """
        Deserialize a list of serialized blocks into a Blockchain
        The results will contain a chain list of Block instance

        Deserializuj listę zserializowanych bloków w Blockchain
        Wyniki będą zawierać listę łańcuchową instancji bloku
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda blockJson: Block.from_json(blockJson), chainJson))
        return blockchain

    @staticmethod
    def isValidChain(chain):
        """
        Validate the incomin chain.
        Enforce the following rules of the blockchain:
        1. The chain must start with the genesis block
        2.Blocks must be formatted correctly

        Sprawdź poprawność łańcucha dochodów.
         Egzekwuj następujące reguły blockchain:
         1. Łańcuch musi zaczynać się od bloku genezy
         2. Bloki muszą być poprawnie sformatowane
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            lastBlock = chain[i - 1]
            Block.isValidBlock(lastBlock, block)

        Blockchain.isValidTransactionChain(chain)

    @staticmethod
    def isValidTransactionChain(chain):
        """
        Enforce the rules of a chain composed of blocks of transaction'
         -Each transaction must only appear once in the chain
         -There can only be one mining reward per block
         -Each transaction must be valid

         Egzekwuj reguły łańcucha złożonego z bloków transakcji ”
          -Każda transakcja może pojawić się tylko raz w łańcuchu
          -Może być tylko jedna nagroda za wydobycie na blok
          -Każda transakcja musi być ważna
        """
        transactionIDS = set()

        for i in range(len(chain)):
            block = chain[i]
            hasMiningReward = False

            for transaction_json in block.data:
                transaction = Trasaction.from_json(transaction_json)

                if transaction.id in transactionIDS:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transactionIDS.add(transaction.id)

                if transaction.id == MINING_REWARD_INPUT:
                    if hasMiningReward:
                        raise Exception('There can only be one mining reward per block',
                                        f'Check block with hash:{block.hash}')

                    hasMiningReward = True

                else:

                    historicBlockchain = Blockchain()
                    historicBlockchain.chain = chain[0:i]
                    hitoricBalance = Wallet.calculateBalance(
                        historicBlockchain,
                        transaction.input['address']
                    )

                    if hitoricBalance != transaction.input['amount']:
                        raise Exception(f'Transaction{transaction.id} has an invalid input amount',
                                        'input amount')

                Trasaction.isValidTransaction(transaction)


def main():
    blockchain = Blockchain()
    blockchain.addBlock('one')
    blockchain.addBlock('two')

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')


if __name__ == '__main__':
    main()

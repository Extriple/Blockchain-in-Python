import uuid
import time

from BackendSide.Wallet.wallet import Wallet
from BackendSide.config import MINING_REWARD, MINING_REWARD_INPUT


class Trasaction:
    """
    Doc of and exchange in currency from a sender to one or more recipients

    Dokumenty i wymiana w walucie od nadawcy do jednego lub większej liczby odbiorców
    """

    def __init__(self, senderWallet=None, recipient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.createOutput(
            senderWallet,
            recipient,
            amount
        )
        self.input = input or self.createInput(senderWallet, self.output)

    def createOutput(self, senderWallet, recipient, amount):
        """
        Sturct the output data for the transaction

        Utwórz dane wyjściowe dla transakcji
        """
        if amount > senderWallet.balance:
            raise Exception('Amount exceeds balance')

        output = {recipient: amount, senderWallet.address: senderWallet.balance - amount}
        return output

    def createInput(self, senderWallet, output):
        """
        Struct the input data for the transc
        Sign the transac and include the sender's public key and address

        Utwórz dane wejściowe dla tranc
        Podpisz transakcję i podaj klucz publiczny i adres nadawcy
        """
        return {
            'timestamp': time.time_ns(),
            'amount': senderWallet.balance,
            'address': senderWallet.address,
            'public_key': senderWallet.public_key,
            'signature': senderWallet.sign(output)

        }

    def update(self, senderWallet, recipient, amount):
        if amount > self.output[senderWallet.address]:
            raise Exception('Amount exceeds balance')
        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

            self.output[senderWallet.address] = \
                self.output[senderWallet.address] - amount

            self.input = self.createInput(senderWallet, self.output)

    def to_json(self):
        """
        Serialize the transaction
        """
        return self.__dict__

    @staticmethod
    def from_json(transactionJson):
        """
        Deserialize a transaction's json representation back into a Transaction instance
        """
        return Trasaction(**transactionJson)

    @staticmethod
    def isValidTransaction(transaction):
        """
        Validate a transac
        Raise a exception for invalid transaction

        Sprawdź poprawność transakcji
        Podnieś wyjątek dla nieprawidłowej transakcji
        """

        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return

        outputTotal = sum(transaction.output.values())

        if transaction.input['amount'] != outputTotal:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
                transaction.input['public_key'],
                transaction.output,
                transaction.input['signature']
        ):
            raise Exception('Invalid signature')

    @staticmethod
    def rewardTransaction(minerWallet):
        """
        Generate a reward transaction that award the miner

        Wygeneruj transakcję premiową, która nagrodzi górnika
        """
        output = {minerWallet.address: MINING_REWARD}

        return Trasaction(input=MINING_REWARD_INPUT, output=output)


def main():
    transaction = Trasaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.__dict__}')

    transactionJson = transaction.to_json()
    restoreTransaction = Trasaction.from_json(transactionJson)
    print(f'restoreTransaction.__dict__:{restoreTransaction.__dict__}')


if __name__ == '__main__':
    main()

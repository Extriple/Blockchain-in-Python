import json
import uuid

from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey

from BackendSide.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


class Wallet:
    """
    An individual wallet for a miner
    Keeps track of the miner's balance
    Allows a miner to authorize transaction

    Indywidualny portfel dla górnika
    Śledzi bilans górnika
    Pozwala górnikowi autoryzować transakcję
    """

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        self.public_key: EllipticCurvePublicKey = self.private_key.public_key()
        self.serializePublicKey()

    @property
    def balance(self):
        return Wallet.calculateBalance(self.blockchain, self.address)

    def sign(self, data):
        """
        Generate the sign based on the data using the local private key

        Wygeneruj znak na podstawie danych przy użyciu lokalnego klucza prywatnego
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256())))

    def serializePublicKey(self):
        """
        Reset the public key to it's serialized version

        Zresetuj klucz publiczny do wersji zserializowanej
        """

        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verificaion a sign based on the original public key and data

        Weryfikacja znaku na podstawie oryginalnego klucza publicznego i danych
        """

        deserializePublicKey = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()

        )

        (r, s) = signature

        try:
            deserializePublicKey.verify(encode_dss_signature(r, s),
                                        json.dumps(data).encode('utf-8'),
                                        ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculateBalance(blockchain, address):
        """
        Calculate the balance of the given address considering the transaction data within the blockchain
        The balance is found by adding the output values that belong to the address since the most recent transaction
         by the address

         Oblicz saldo podanego adresu, uwzględniając dane transakcji w łańcuchu bloków
         Saldo można znaleźć, dodając wartości wyjściowe, które należą do adresu od ostatniej transakcji
          według adresu
        """

        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    # Time the address conducts a new transaction it resets
                    # it's balance
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

            return balance


def main():
    wallet = Wallet()
    print(f'wallet.__dict__:{wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature:{signature}')

    shouldBeValid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should be valid:{shouldBeValid}')
    shouldBeInvalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'shouldBeInvalid:{shouldBeInvalid}')


if __name__ == '__main__':
    main()

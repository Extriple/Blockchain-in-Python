from BackendSide.Wallet.wallet import Wallet
from BackendSide.Blockchain.Blockchain import Blockchain
from BackendSide.config import STARTING_BALANCE
from BackendSide.Wallet.Transaction import Trasaction


def testVerifyValidSing():
    data = {'foo': 'testData'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)


def testVerifyInvalidSing():
    data = {'foo': 'testData'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)


def testCalculateBalance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculateBalance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Trasaction(wallet, 'recipient', amount)
    blockchain.addBlock(transaction.to_json())

    assert Wallet.calculateBalance(blockchain, wallet.address) == STARTING_BALANCE - amount

    recoveryAmount1 = 25
    recoveryTransaction1 = Trasaction(Wallet(), wallet.address, recoveryAmount1)

    recoveryAmount2 = 43
    recoveryTransaction2 = Trasaction(Wallet(), wallet.address, recoveryAmount2)

    blockchain.addBlock([recoveryTransaction1.to_json(), recoveryTransaction2.to_json()])

    assert Wallet.calculateBalance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount + recoveryAmount1 + recoveryAmount2

from BackendSide.Wallet.TransactionPool import TransactionPool
from BackendSide.Wallet.Transaction import Trasaction
from BackendSide.Wallet.wallet import Wallet
from BackendSide.Blockchain.Blockchain import Blockchain


def testSetTransaction():
    transactionPool = TransactionPool()
    transaction = Trasaction(Wallet(), 'recipient', 1)
    transactionPool.setTransaction(transaction)

    assert transactionPool.transcationMap[transaction.id] == transaction


def testClear():
    transactionPool = TransactionPool()
    transaction1 = Trasaction(Wallet(), 'recipient', 1)
    transaction2 = Trasaction(Wallet(), 'recipient', 2)

    transactionPool.setTransaction(transaction1)
    transactionPool.setTransaction(transaction2)

    blockchain = Blockchain()
    blockchain.addBlock([transaction1.to_json(), transaction2.to_json()])

    assert transaction1.id in transactionPool.transcationMap
    assert transaction2.id in transactionPool.transcationMap

    transactionPool.clearTransaction(blockchain)

    assert not transaction1.id in transactionPool.transcationMap
    assert not transaction2.id in transactionPool.transcationMap

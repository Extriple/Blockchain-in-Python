import pytest

from BackendSide.Blockchain.Blockchain import Blockchain
from BackendSide.Blockchain.Block import GENESIS_DATA
from BackendSide.Wallet.Transaction import Trasaction
from BackendSide.Wallet.wallet import Wallet


def TestBlockchain():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def testAddBlock():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.addBlock(data)

    assert blockchain.chain[-1].data == data


# Sprawdzanie poprawności łańcucha to proces zapewniający prawidłowe sformatowanie danych
# zewnętrznego łańcucha blokowego. Aby łańcuch bloków był prawidłowy, istnieje wiele reguł do egzekwowania.
# Na początek, każdy blok musi być ważny, z odpowiednim hashem opartym na polach bloku, poprawnie dostosowaną trudnością,
# dopuszczalną liczbą wiodących zer w haszu dla wymogu dowodu pracy i więcej. Podobnie w samym łańcuchu bloków musi rozpoczynać się od bloku genezy,
# a ostatni skrót każdego bloku musi odnosić się do skrótu bloku, który pojawił się przed nim.

# Wymiana łańcucha to proces zastępowania bieżących danych łańcucha blokowego danymi przychodzącego łańcucha blokowego.
# Jeśli przychodzący łańcuch bloków jest dłuższy i ważny, powinien zastąpić bieżący łańcuch bloków.
# Umożliwi to rozprzestrzenienie się prawidłowego łańcucha bloków z nowymi blokami w docelowej sieci bloków, stając się prawdziwym łańcuchem bloków,
# na który zgodzą się wszystkie węzły sieci bloków.

@pytest.fixture
def Blockchain3Blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.addBlock([Trasaction(Wallet(), 'recipient', i).to_json()])
        return blockchain


def testIsValidChain(Blockchain3Blocks):
    Blockchain.isValidChain(Blockchain3Blocks.chain)


def testIsValidChainBadGenesis(Blockchain3Blocks):
    Blockchain3Blocks.chain[0].hash = 'evil_hash'

    with pytest.raises(Exception, match='The genesis block must be valid'):
        Blockchain.isValidChain(Blockchain3Blocks.chain)


# nowe instancje łańcuch blokowy jest równy kropce łańcucha blokowego trzy bloki raczej łańcucha blokowego trzy bloki
# lista łańcuchów kropkowych, ponieważ mimo wszystko, jeśli łańcuch zastępujący działał, powinniśmy zastąpić to blokowaniem
# łańcuch z dłuższą listą łańcuchów z instancji trzech bloków łańcucha.

def testReplaceChain(Blockchain3Blocks):
    blockchain = Blockchain()
    blockchain.replaceChain(Blockchain3Blocks.chain)

    assert blockchain.chain == Blockchain3Blocks.chain


def testReplaceChainNotLonger(Blockchain3Blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match='The incoming chain must be longer'):
        Blockchain3Blocks.replaceChain(blockchain.chain)


def testReplaceChainBadChain(Blockchain3Blocks):
    blockchain = Blockchain()
    Blockchain3Blocks.chain[1].hash = 'evil_hash'

    with pytest.raises(Exception, match='The incoming chain is invalid'):
        blockchain.replaceChain(Blockchain3Blocks.chain)


def testValidTransactionChain(Blockchain3Blocks):
    Blockchain.isValidTransactionChain(Blockchain3Blocks.chain)


def testisValidTransactionChainDuplicate(Blockchain3Blocks):
    transaction = Trasaction(Wallet(), 'recipient', 1).to_json()

    Blockchain3Blocks.addBlock([transaction, transaction])

    with pytest.raises(Exception, match='is not unique'):
        Blockchain.isValidTransactionChain(Blockchain3Blocks.chain)


def testIsValidTransactionChainMultiRewards(Blockchain3Blocks):
    rewardOne = Trasaction.rewardTransaction(Wallet()).to_json()
    rewardTwo = Trasaction.rewardTransaction(Wallet()).to_json()

    Blockchain3Blocks.addBlock([rewardOne, rewardTwo])

    with pytest.raises(Exception, match='one mining reward per block'):
        Blockchain.isValidTransactionChain(Blockchain3Blocks.chain)


def testIsValidTransactionChainBadTransaction(Blockchain3Blocks):
    badTransaction = Trasaction(Wallet(), 'recipient', 1)
    badTransaction.input['signature'] = Wallet().sign(badTransaction.output)
    Blockchain3Blocks.addBlock([badTransaction.to_json()])

    with pytest.raises(Exception):
        Blockchain.isValidTransactionChain(Blockchain3Blocks)


def testIsValidTransactionChainBadHistoricBalance(Blockchain3Blocks):
    wallet = Wallet()
    badTransaction = Trasaction(wallet, 'recipient', 1 )
    badTransaction.output[wallet.address] = 9000
    badTransaction.input['amount'] = 9001
    badTransaction.input['signature'] = wallet.sign(badTransaction.output)

    Blockchain3Blocks.addBlock([badTransaction.to_json()])

    with pytest.raises(Exception, match='has an invalid input amount'):
        Blockchain.isValidTransactionChain(Blockchain3Blocks.chain)

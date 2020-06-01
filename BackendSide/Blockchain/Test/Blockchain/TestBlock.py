import time
import pytest

from BackendSide.Blockchain.Block import Block, GENESIS_DATA
from BackendSide.config import MINE_RATE, SEC
from BackendSide.Utility.HexToBinary import HexToBinary


# Zacznijmy od stworzenia nowej metody testowania dla funkcji bloku mine, aby najpierw zbudować blok wewnątrz
# Są dwa argumenty, że musisz podać ostatni obiekt bloku, a następnie dane.
# Zadeklarujmy więc zmienną dla ostatniego bloku i ustawmy ją na wynik wywołania wartości statycznej
# A co powiesz na ciąg z danymi testowymi.
# Tak więc dane są ciągiem, który jest danymi kreski testowej.
# Następnie stwórzmy zmienną dla samego bloku wynikowego z wywołania.

def testMineBlock():
    lastBlock = Block.genesis()
    data = 'test-data'
    block = Block.mineBlock(lastBlock, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.lasthash == lastBlock.hash
    assert HexToBinary(block.hash)[0:block.dificulty] == '0' * block.dificulty


# Jeśli chodzi o sam obiekt bloku, należy sprawdzić kilka kluczowych aspektów jego pola danych
# dopasuj dane podane do funkcji bloku kopalni, więc dodaj instrukcję wyszukiwania i wstaw zablokowaną
# dane są równe zadeklarowanej zmiennej danych, naprawdę ważną jest upewnienie się, że ostatnie pole skrótu
# dopasowuje skrót z ostatniego bloku.

def testGenesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    # uzyskujemy atrybut
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


#     testy Proof of Work dificulty
def testQuicklyMineBlock():
    lastBlock = Block.mineBlock(Block.genesis(), 'foo')
    mineBlock = Block.mineBlock(lastBlock, 'bar')

    assert mineBlock.dificulty == lastBlock.dificulty + 1


def testSlowlyMineBlock():
    lastBlock = Block.mineBlock(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SEC)
    mineBlock = Block.mineBlock(lastBlock, 'bar')

    assert mineBlock.dificulty == lastBlock.dificulty - 1


def testMineBlockDicifultyLimitRaTE_1():
    lastblock = Block(
        time.time_ns(),
        'testLastHash',
        'testHash',
        'testData',
        1,
        0
    )

    time.sleep(MINE_RATE / SEC)
    mineBlock = Block.mineBlock(lastblock, "bar")

    assert mineBlock.dificulty == 1


@pytest.fixture
def lastBlock():
    return Block.genesis()


@pytest.fixture
def block(lastBlock):
    return Block.mineBlock(lastBlock, 'test-data')


def testIsValidBlock(lastBlock, block):
    Block.isValidBlock(lastBlock, block)


def testIsValidBlockBadLastHash(lastBlock, block):
    block.lasthash = 'evil_LastHash'

    with pytest.raises(Exception, match='lastHash must be correct'):
        Block.isValidBlock(lastBlock, block)


def testIsValidBadProofOfWork(lastBlock, block):
    block.hash = 'fff'

    with pytest.raises(Exception, match='proof of work requirement was not met'):
        Block.isValidBlock(lastBlock, block)


def testIsValidBlockJumpDifficulty(lastBlock, block):
    jumpDifficulty = 10
    block.dificulty = jumpDifficulty
    block.hash = f'{"0" * jumpDifficulty}111abc'

    with pytest.raises(Exception, match='difficulty must only adjust by 1'):
        Block.isValidBlock(lastBlock, block)


def testIsValidBlockBadHash(lastBlock, block):
    block.hash = '0000000000000000bbbabc'

    with pytest.raises(Exception, match='block hash must be correct'):
        Block.isValidBlock(lastBlock, block)

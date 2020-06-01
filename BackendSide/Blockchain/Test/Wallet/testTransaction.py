import pytest

from BackendSide.Wallet.Transaction import Trasaction
from BackendSide.Wallet.wallet import Wallet
from BackendSide.config import MINING_REWARD_INPUT, MINING_REWARD


def testTransaction():
    senderWallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Trasaction(senderWallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[senderWallet.address] == senderWallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == senderWallet.balance
    assert transaction.input['address'] == senderWallet.address
    assert transaction.input['public_key'] == senderWallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def testTransactionExceedsBalance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Trasaction(Wallet(), 'recipient', 9001)


def testTransactionUpdateBalance():
    senderWallet = Wallet()
    transc = Trasaction(senderWallet, 'recipient', 50)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        transc.update(senderWallet, 'new_recipient', 9001)


def testTransactionUpdate():
    senderWallet = Wallet()
    firstRecipiemt = 'firstRecipient'
    firstAmount = 50
    transaction = Trasaction(senderWallet, firstRecipiemt, firstAmount)

    nextRecipient = 'nextRecipient'
    nextAmount = 75
    transaction.update(senderWallet, nextRecipient, nextAmount)

    assert transaction.output[nextRecipient] == nextAmount
    assert transaction.output[senderWallet.address] == \
           senderWallet.balance - firstAmount - nextAmount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    toFirstAgainAmount = 25
    transaction.update(senderWallet, firstRecipiemt, toFirstAgainAmount)

    assert transaction.output[firstRecipiemt] == \
           firstAmount + toFirstAgainAmount
    assert transaction.output[senderWallet.address] == \
           senderWallet.balance - firstAmount - nextAmount - toFirstAgainAmount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def testValidTransaction():
    Trasaction.isValidTransaction(Trasaction(Wallet(), 'recipient', 50))


def testValidTransactionWithInvalidOutput():
    senderWallet = Wallet()
    transaction = Trasaction(senderWallet, 'recipient', 50)
    transaction.output[senderWallet.address] = 9001
    with pytest.raises(Exception, match='Invalid transaction output values'):
        Trasaction.isValidTransaction(transaction)


def testValidTransactionWithInvalidSignature():
    transaction = Trasaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature'):
        Trasaction.isValidTransaction(transaction)


def testRewardTransaction():
    minerWallet = Wallet()
    transaction = Trasaction.rewardTransaction(minerWallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[minerWallet.address] == MINING_REWARD


def testValidRewardTransaction():
    rewardTransc = Trasaction.rewardTransaction(Wallet())
    Trasaction.isValidTransaction(rewardTransc)


def testValidRewardTransactionExtraRecipient():
    rewardTransc = Trasaction.rewardTransaction(Wallet())
    rewardTransc.output['extraRecipient'] = 60

    with pytest.raises(Exception, match='Invalid mining reward'):
        Trasaction.isValidTransaction(rewardTransc)


def testInvalidRewardTransactionInvalidAmount():
    minerWallet = Wallet()
    rewardTransaction = Trasaction.rewardTransaction(minerWallet)
    rewardTransaction.output[minerWallet.address] = 9001

    with pytest.raises(Exception, match='Invalid mining reward'):
        Trasaction.isValidTransaction(rewardTransaction)

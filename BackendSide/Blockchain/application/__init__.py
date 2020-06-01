import os
import random
import requests

from flask import Flask, jsonify, request
from BackendSide.Blockchain.Blockchain import Blockchain
from BackendSide.Wallet.Transaction import Trasaction
from BackendSide.Wallet.wallet import Wallet
from BackendSide.Wallet.TransactionPool import TransactionPool
from BackendSide.PubNubSub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain)
transactionPool = TransactionPool()
pubsub = PubSub(blockchain, transactionPool)


@app.route('/')
def Default():
    return 'Welcome to blockchain'


@app.route('/blockchain')
def routeBlockchain():
    return jsonify(blockchain.to_json())


@app.route('/wallet/transaction', methods=['POST'])
def routeWalletTransacation():
    # {'recipient': 'foo', 'amount': 15}
    transactionData = request.get_json()
    transaction = transactionPool.existingTransaction(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            transactionData['recipient'],
            transactionData['amount']
        )
    else:
        transaction = Trasaction(wallet,
                                 transactionData['recipient'],
                                 transactionData['amount'])

    pubsub.broadcastTransaction(transaction)

    return jsonify(transaction.to_json())


@app.route('/wallet/info')
def routeWalletInfo():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


@app.route('/blockchain/mine')
def routeBlockchainMine():
    transactionData = transactionPool.transactionData()
    transactionData.append(Trasaction.rewardTransaction(wallet).to_json())
    blockchain.addBlock(transactionData)
    block = blockchain.chain[-1]
    pubsub.broadcastBlock(block)
    transactionPool.clearTransaction(blockchain)

    return jsonify(block.to_json())


ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == True:
    PORT = random.randint(5001, 6000)

    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    resultBlockchain = Blockchain.fromJson(result.json())
    try:
        blockchain.replaceChain(resultBlockchain.chain)
        print('\n-- Successful synchronized the local chain')
    except Exception as e:
        print(f'\n-- Error synchornized:{e}')

app.run(port=PORT)

import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from BackendSide.Blockchain.Block import Block
from BackendSide.Wallet.Transaction import Trasaction

SubscribeKey = 'sub-c-c0d3079e-9c6a-11ea-84ed-1e1b4c21df71'
PublishKey = 'pub-c-4294add4-b142-463d-b043-c0ddbdcd8173'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-c0d3079e-9c6a-11ea-84ed-1e1b4c21df71'
pnconfig.publish_key = 'pub-c-4294add4-b142-463d-b043-c0ddbdcd8173'
pubnub = PubNub(pnconfig)

Channels = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION':'TRANSACTION'
}


class Listener(SubscribeCallback):

    def __init__(self, blockchain, transactionPool):
        self.blockchain = blockchain
        self.transactionPool = transactionPool

    def msg(self, pubnub, msgObject):
        print(f'\n-- Channel: {msgObject.channel} | Message:{msgObject.msg}')

        if msgObject.channel == Channels['BLOCK']:
            block = Block.from_json(msgObject.msg)
            potentialChain = self.blockchain.chain[:]
            potentialChain.append(block)

            try:
                self.blockchain.replaceChain(potentialChain)
                self.transactionPool.clearTransaction(self.blockchain)
                print('\n -- Succesful replacing the chain')
            except Exception as e:
                print(f'\n -- Did not replace chain:{e}')

        elif msgObject.channel == Channels['TRANSACTION']:
            transaction = Trasaction.from_json(msgObject.msg)
            self.transactionPool.setTransaction(transaction)
            print(f'\n-- Set the new transaction in the transaction pool')



class PubSub():
    """
    Handles the publish layer of the app
    Provides community between then nodes of the blockchain network

    Obsługuje warstwę publikowania aplikacji
    Zapewnia społeczność między następnie węzłami sieci blockchain
    """

    def __init__(self, blockchain, transactionPool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(Channels.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transactionPool))

    def publish(self, channel, msg):
        """
        Publish the msg obj to the channel
        """
        self.pubnub.publish().channel(channel).message(msg).sync()

    def broadcastBlock(self, block):
        """
        Broadcast a block obj to all nodes
        """
        self.publish(Channels['BLOCK'], block.to_json())

    def broadcastTransaction(self, transaction):
        """
        Broadcast transaction to all nodes
        """
        self.publish(Channels['TRANSACTION'], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)

    pubsub.publish(Channels['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()

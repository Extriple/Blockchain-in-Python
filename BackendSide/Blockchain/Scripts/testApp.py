import request
import time

from BackendSide.Wallet.wallet import Wallet

URL = 'http://localhost:5000'


def getBlockchain():
    return request.GET(f'{URL}/blockchain').json()


def getBlockchainMine():
    return request.GET(f'{URL}/blockchain/mine').json()


def postWalletTransaction(recipient, amount):
    return request.POST(f'{URL}/wallet/transaction', json={'recipient': recipient, 'amount': amount}).json()


def getWalletInfo():
    return request.GET(f'{URL}/wallet/info').json()


startBlockchain = getBlockchain()
print(f'start_the_Blockchain:{startBlockchain()}')

recipient = Wallet().address

postWalletTransaction1 = postWalletTransaction(recipient, 21)
print(f'\n postWalletTransaction_1:{postWalletTransaction1}')

time.sleep(1)
postWalletTransaction2 = postWalletTransaction(recipient, 13)
print(f'\n postWalletTransaction_2:{postWalletTransaction2}')

time.sleep(1)
mineBlockValue = getBlockchainMine()
print(f'\n minedBlock:{mineBlockValue}')


walletInfo = getWalletInfo()
print(f'\nwalletInfo{walletInfo}')
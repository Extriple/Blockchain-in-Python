import time

from BackendSide.Blockchain.Blockchain import Blockchain
from BackendSide.config import SEC

blockchain = Blockchain()

times = []

for i in range(1000):
    startTime = time.time_ns()
    blockchain.addBlock(i)
    endTime = time.time_ns()
    # Czas kopania
    timeMine = endTime - startTime / SEC
    # Pojedyńczy element dla czasu kopania
    times.append(timeMine)

    averageTime = sum(times) / len(times)

    print(f'New block difficulty:{blockchain.chain[-1].dificulty}')
    print(f'Time mine to new block:{timeMine}s')
    print(f'Average Time to add a new block:{averageTime}s\n')




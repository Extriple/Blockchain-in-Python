from BackendSide.Utility.CryptoHash import CryptoHash


def testCryptoHash():
    # tym przypadku powiemy, że powinien utworzyć ten sam skrót z argumentami różnych typów danych w dowolnym
    assert CryptoHash(1, [2], 'three') == CryptoHash('three', 1, [2])
    assert CryptoHash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'

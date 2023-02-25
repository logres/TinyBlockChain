from source.blockchain import (
    Transaction, UnspentTransaction, TransactionOutput, Block, BlockChain, TransactionPool)


def test_transaction():
    transaction = Transaction([], [])
    assert transaction.hash is not None
    assert transaction.verify()
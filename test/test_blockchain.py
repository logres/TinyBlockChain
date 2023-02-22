from source.blockchain import (
    Transaction, UnspentTransaction, TransactionOutput, Block, BlockChain, TransactionPool)


def test_transaction():
    input = [UnspentTransaction('1', 0, '1'), UnspentTransaction('2', 1, '2')]
    output = [TransactionOutput('1', 100), TransactionOutput('2', 200)]
    transaction = Transaction(input, output)


def test_block():
    input = [UnspentTransaction('1', 0, '1'), UnspentTransaction('2', 1, '2')]
    output = [TransactionOutput('1', 100), TransactionOutput('2', 200)]
    transaction = Transaction(input, output)
    block = Block(is_genius=True)
    block2 = Block(block, [transaction])


def test_blockchain():
    input = [UnspentTransaction('1', 0, '1'), UnspentTransaction('2', 1, '2')]
    output = [TransactionOutput('1', 100), TransactionOutput('2', 200)]
    transaction = Transaction(input, output)
    blockchain = BlockChain()
    blockchain.add_block([transaction])


def test_transaction_pool():
    tp = TransactionPool()
    tx = Transaction([], [])
    tp.add_transaction(tx)
    tp.get_transactions()

from .blockchain import BlockChain, Block, Transaction, TransactionPool
from .my_cryptography import generate_key_pair

class Node:
    # 区块链节点功能分为两个部分：
    # 1. 发送交易、维护交易池、验证交易、打包交易（挖矿）
    # 2. 同步区块链、验证区块、广播区块

    def __init__(self) -> None:
        self.transaction_pool = TransactionPool()
        self.blockchain = BlockChain()
        (self.private_key,self.public_key) = generate_key_pair()
        self.address = self.public_key.address()

    def add_block(self)-> Block:
        return self.blockchain.add_block(self.transaction_pool.get_transactions())
    
    def add_transaction(self,transaction: Transaction) -> bool:
        return self.transaction_pool.add_transaction(transaction)

    def verify():
        return True

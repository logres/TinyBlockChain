import json, hashlib, time
from .my_cryptography import PrivateKey, PublicKey, Address, generate_key_pair
from collections import namedtuple

from typing import Optional

UnspentTransaction = namedtuple('UnspentTransaction', ['transaction_hash', 'index', 'public_key','signature'])
TransactionOutput = namedtuple('TransactionOutput', ['public_key_hash','amount'])

class Transaction:

    def __init__(self, input: list[UnspentTransaction], output: list[TransactionOutput]) -> None:
        self._input = input
        self._output = output
        self._in_size = len(input)
        self._out_size = len(output)
        self._hash = self.calculate_hash()
    
    def hash_content(self) -> str:
        return {
            'in_size': self._in_size,
            'out_size': self._out_size,
            'input': [(unspent_transaction.transaction_hash,unspent_transaction.index,unspent_transaction.signature) for unspent_transaction in self._input],
            'output': [(transaction_output.address, transaction_output.amount) for transaction_output in self._output]
        }
    
    def verify(self):
        # TODO: 验证交易有效性——输入输出值一致
        return sum([transaction_output.amount for transaction_output in self._output]) == sum([unspent_transaction.amount for unspent_transaction in self._input])

    def calculate_hash(self) -> str:
        return hashlib.sha3_256(json.dumps(self.hash_content()).encode()).hexdigest()

    @property
    def hash(self):
        return self._hash
    
    def show(self):
        print('-'*10, 'Transaction', '-'*10)
        print('Transaction Hash:', self._hash)
        print('Input:')
        for unspent_transaction in self._input:
            print('Transaction Hash:', unspent_transaction.transaction_hash)
            print('Index:', unspent_transaction.index)
            print('Signature:', unspent_transaction.signature)
        print('Output:')
        for transaction_output in self._output:
            print('Address:', transaction_output.address)
            print('Amount:', transaction_output.amount)
        print("-"*20)

class TransactionPool:
    # 有序的交易池

    def __init__(self) -> None:
        self._transactions = []
        # self._transaction_mapper = {}

    def add_transaction(self, transaction: Transaction) -> bool:
        # TODO: 验证交易有效性 检查双花等等
        # if transaction.hash in self._transaction_mapper:
        #     return
        self._transactions.append(transaction)
        # self._transaction_mapper[transaction.hash] = transaction
        return True

    def get_transactions(self):
        # TODO: 增加数量参数
        return self._transactions[:10]

    def update(self,block: "Block"):
        # TODO: 根据收到的区块更新交易池
        for transaction in block.transactions:
            if transaction.hash in self._transaction_mapper:
                self._transactions.remove(transaction)
                del self._transaction_mapper[transaction.hash]
    
    def show(self):
        for transaction in self._transactions:
            transaction.show()

class MerkleTree:
    # 默克尔树，用于构建区块中的交易树

    def __init__(self, transactions: list[Transaction]) -> None:
        self._tree = self.construct_tree(transactions)
    
    def construct_tree(self,transactions: list[Transaction]):
        if len(transactions) == 0:
            _tree = [['0'*64]]
            return _tree
        _tree = []
        bottom_layer = [transaction.hash for transaction in transactions]
        _tree.append(bottom_layer)
        previous_layer = _tree[-1]
        while len(previous_layer) > 1:
            current_layer = []
            for i in range(0, len(previous_layer), 2):
                if i + 1 < len(previous_layer):
                    current_layer.append(hashlib.sha3_256((previous_layer[i] + previous_layer[i+1]).encode()).hexdigest())
                else:
                    current_layer.append(previous_layer[i])
            _tree.append(current_layer)
            previous_layer = _tree[-1]
        return _tree

    @property
    def root(self):
        return self._tree[-1][0]
    
    @property
    def transactions(self):
        return self.transactions
    
    def show(self):
        for layer in self._tree:
            print(layer)


class Block:
    # 区块，区块链的基本单位

    difficulty = 2

    def __init__(self, previous_block: Optional["Block"] = None, transactions: list[Transaction] = [], is_genius=False) -> None:
        '''
        区块头：
        previous_block_hash: 前一个区块的hash
        nonce: 随机数
        difficulty: 难度
        merkle_root: 交易树的根
        timestamp: 时间戳
        index: 区块高度

        区块体：
        transactions: 交易列表
        merkle_tree: 默克尔树

        方法：
        mine: 挖矿——计算nonce
        calculate_hash: 计算区块的hash
        '''
        print(previous_block)
        if not is_genius:
            self._hash = None
            self._previous_block_hash = previous_block.hash # hash
            self._difficulty : int = Block.difficulty # hash
            self._nonce = None # hash
            self._timestamp = int(round(time.time()*1000)) # hash
            self._index = previous_block.index + 1
            self._merkle_tree = MerkleTree(transactions) # hash.hash
            self._transactions = transactions

            if not self.mine():
                raise Exception('Mining Failed')
            self._hash = self.calculate_hash()
        else:
            self._hash = '0'*64
            self._previous_block_hash = None
            self._difficulty : int = Block.difficulty
            self._nonce = None
            self._timestamp = int(round(time.time()*1000))
            self._index = 0
            self._merkle_tree = MerkleTree(transactions)
            self._transactions = transactions

    def mine(self):
        for nonce in range(1, 2**32):
            self._nonce = nonce
            if self.calculate_hash().startswith('0' * self._difficulty):
                return True
        print('Mining Failed')
        self._nonce = None
        return False

    def hash_content(self) -> str:
        return {
            'previous_block_hash': self._previous_block_hash,
            'index': self._index,
            'nonce': self._nonce,
            'difficulty': self._difficulty,
            'merkle_root': self._merkle_tree.root,
            'timestamp': self._timestamp,
        }

    def calculate_hash(self):
        return hashlib.sha3_256(json.dumps(self.hash_content()).encode()).hexdigest()
    
    def show(self):
        print('-'*10, 'Block', '-'*10)
        print('previous_block_hash:', self._previous_block_hash)
        print('nonce:', hex(self._nonce))
        print('difficulty:', '0x' + self._difficulty*'0' + 'f'*(64-self._difficulty) )
        print('merkle_root:', self._merkle_tree.root)
        print('timestamp:', self._timestamp)
        print('hash:', self._hash)
        print('-'*20)
    
    def verify(self):
        if self.is_genius():
            return True
        if self._hash != self.calculate_hash():
            return False
        if not self._hash.startswith('0' * self._difficulty):
            return False
        return True

    def is_genius(self):
        return self._index == 0

    @property
    def hash(self):
        return self._hash
    
    @property
    def transactions(self):
        return self._transactions
    
    @property
    def index(self):
        return self._index

class BlockChain:
    # 区块链，分布式网络的核心

    def __init__(self) -> None:
        genius_block = Block(is_genius=True)
        self._blocks = [genius_block]
        self._hash2block = {genius_block.hash:genius_block}
        self._hash2transaction = {}
    
    def add_block(self, transactions: list[Transaction]) -> bool:
        new_block = Block(self.last_block, transactions)
        self._blocks.append(new_block)
        self._hash2block[new_block.hash] = new_block
        return True

    def get_transaction(self,transaction_hash):
        return self._blocks.get_transaction(transaction_hash)
    
    @property
    def last_block(self):
        return self._blocks[-1]
    
    def __len__(self):
        return len(self._blocks)

    def show(self):
        for block in self._blocks:
            block.show()
    
    def verify_transaction(self, transaction: Transaction):
        # 如何校验交易合法性
        # 1. 为交易涉及的输入USTX提供使用人的公钥与对该交易使用私钥产生的签名
        #  1.1 计算公钥hash是否等于USTX中的公钥hash（地址）
        #  1.2 使用公钥解密签名，得到交易hash，与交易hash是否相等
        for unspent_transaction in self.unspent_transactions:
            transaction_hash = unspent_transaction.transaction_hash
            transaction_index = unspent_transaction.transaction_index
            public_key : PublicKey= unspent_transaction.public_key
            signature = unspent_transaction.signature
            # 校验公钥哈希
            input_transaction: TransactionOutput = get_transaction(transaction_hash).out_put[transaction_index]
            if input_transaction.public_key_hash != public_key.hash():
                return False
            if not public_key.verify(message=transaction_hash,signature=signature):
                return False
        return True






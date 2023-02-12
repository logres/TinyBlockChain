import json, hashlib, time
from .my_cryptography import PrivateKey, PublicKey, Address, generate_key_pair
from collections import namedtuple

UnspentTransaction = namedtuple('UnspentTransaction', ['transaction_hash', 'index', 'signature'])
TransactionOutput = namedtuple('TransactionOutput', ['address', 'amount'])

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
        self._transaction_mapper = {}

    def add_transaction(self, transaction: Transaction):
        # TODO: 验证交易有效性 检查双花等等
        # if transaction.hash in self._transaction_mapper:
        #     return
        self._transactions.append(transaction)
        self._transaction_mapper[transaction.hash] = transaction

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

    def __init__(self, previous_block_hash: str, transactions: list[Transaction]) -> None:
        self._hash = None
        self._previous_block_hash = previous_block_hash # hash
        self._difficulty = Block.difficulty # hash
        self._nonce = None # hash
        self._timestamp = int(round(time.time()*1000)) # hash


        self._merkle_tree = MerkleTree(transactions) # hash.hash
        self._transactions = transactions

        if not self.mine():
            raise Exception('Mining Failed')
        self._hash = self.calculate_hash()

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

    @property
    def hash(self):
        return self._hash
    
    @property
    def transactions(self):
        return self._transactions

class BlockChain:
    # 区块链，分布式网络的核心

    def __init__(self) -> None:
        self._blocks = [Block('0'*32, [Transaction([], [])])]
        self._block_mapper = {self._blocks[0].hash: self._blocks[0]}
    
    def add_block(self, block: Block):
        self._blocks.append(block)
        self._block_mapper[block.hash] = block
    
    def get_block(self, block_hash: str):
        return self._block_mapper[block_hash]

    def show(self):
        for block in self._blocks:
            block.show()



from source.blockchain import (
    Transaction, UnspentTransaction, TransactionOutput, Block, BlockChain, TransactionPool)
from source.my_cryptography import (PrivateKey,PublicKey,generate_key_pair)
# class TransactionMaker:

#     def __init__(self) -> None:
#         pass

#     def create_transaction(self):
#         a = UnspentTransaction()
#         return Transaction()

import json

with open('default_user.json','r',encoding='utf-8') as f:
    default_users = json.load(f) 

def test_block_chain():
    user1 = default_users["0"]
    user1_private_key = PrivateKey(user1['private_key'])
    user1_public_key = PublicKey(user1['public_key'])
    user2 = default_users['1']
    user2_private_key = PrivateKey(user2['private_key'])
    user2_public_key = PublicKey(user2['public_key'])
    block_chain = BlockChain()
    first_block = block_chain._blocks[0]
    first_transaction = block_chain._blocks[0].transactions[0]
    utxo = UnspentTransaction(first_transaction.hash,0,user1_public_key.public_key,
                              user1_private_key.sign(bytes.fromhex(first_transaction.hash)))
    output = TransactionOutput(user2_public_key.public_key_hash,10)
    new_transaction = Transaction([utxo],[output])
    new_block = Block(first_block,[new_transaction])
    res = block_chain.add_block(block=new_block)
    print(res)

test_block_chain()
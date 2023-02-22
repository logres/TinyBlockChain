from .blockchain import BlockChain, Block, Transaction, TransactionPool
import asyncio, threading
from .my_cryptography import PrivateKey, PublicKey, Address, generate_key_pair

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


    # def ui_task(self):
    #     while True:
    #         _input = input(self.address.address+"\n"+"Input Command: ")
    #         if _input.startswith('transaction'):
    #             round = int(_input.split(" ")[1]) if len(_input.split(" ")) > 1 else 1
    #             for _ in range(round):
    #                 transaction = Transaction([],[])
    #                 self.transaction_pool.add_transaction(transaction)
    #             # self.broadcast_transaction()
    #         elif _input.startswith('check'):
    #             content = _input.split(" ")[1] if len(_input.split(" ")) > 1 else 'blockchain'
    #             if content == 'blockchain':
    #                 self.blockchain.show()
    #             elif content == 'transaction':
    #                 self.transaction_pool.show()

    # async def mine_task(self):
    #     while True:
    #         if len(self.transaction_pool.get_transactions()) >= 10:
    #             print("new Block")
    #             block = self.construct_block()
    #             self.blockchain.add_block(block)
    #             # await self.broadcast_block()
    #             self.transaction_pool.update(block)
    #         await asyncio.sleep(1)

    # def background_task(self):
    #     event_loop = asyncio.new_event_loop()
    #     # event_loop.create_task(self.listen_task())
    #     event_loop.create_task(self.mine_task())
    #     event_loop.run_forever()

    # def run(self):
    #     # TODO: 启动节点
    #     # 启用一个线程以asyncio执行监听与打包
    #     background_thread = threading.Thread(target=self.background_task)
    #     background_thread.setDaemon(True)
    #     background_thread.start()
    #     # 在主线程中进行UI操作、发起交易等操作
    #     self.ui_task()

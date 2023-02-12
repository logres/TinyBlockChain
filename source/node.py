from .blockchain import BlockChain, Block, Transaction, TransactionPool
import asyncio, threading, time, yaml
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

        # with open('config.yml', 'r') as f:
        #     config = yaml.load(f, Loader=yaml.FullLoader)
        # self.neighbors = [(address_port.split(":")[0],int(address_port.split(":")[1])) for address_port in config['neighbors']]
        # self.node_address = self.neighbors[index]
        # self.neighbors.pop(index)

    def construct_block(self)-> Block:
        return Block(self.blockchain._blocks[-1].hash, self.transaction_pool.get_transactions())

    def verify_block(self, block: Block):
        return block.hash == block.calculate_hash()
    
    def get_transaction(self, transaction_hash: str):
        return self._transaction_mapper[transaction_hash]

    def get_block(self, block_hash: str):
        return self._block_mapper[block_hash]

    # def register_node(self, node):
    #     self.neighbors.append(node)

    # def broadcast_transaction(self):
    #     print("broadcast transaction")
    #     for neighbor in self.neighbors:
    #         pass

    # async def broadcast_block(self):
    #     print("broadcast block")
    #     for neighbor in self.neighbors:
    #         pass
    
    def ui_task(self):
        while True:
            _input = input(self.address.address+"\n"+"Input Command: ")
            if _input.startswith('transaction'):
                round = int(_input.split(" ")[1]) if len(_input.split(" ")) > 1 else 1
                for _ in range(round):
                    transaction = Transaction([],[])
                    self.transaction_pool.add_transaction(transaction)
                # self.broadcast_transaction()
            elif _input.startswith('check'):
                content = _input.split(" ")[1] if len(_input.split(" ")) > 1 else 'blockchain'
                if content == 'blockchain':
                    self.blockchain.show()
                elif content == 'transaction':
                    self.transaction_pool.show()

    # async def handle(self, reader, writer):
    #     data = await reader.read(100)
    #     message = data.decode()
    #     if message == 'block':
    #         block = Block.from_json(message)
    #         if self.verify_block(block):
    #             self.blockchain.add_block(block)
    #             await self.broadcast_block()
    #             self.transaction_pool.update(block)
    #     elif message == 'transaction':
    #         transaction = Transaction.from_json(message)
    #         self.transaction_pool.add_transaction(transaction)
    #         await self.broadcast_transaction()
    #     else:
    #         writer.close()

    # async def listen_task(self):
    #     server = await asyncio.start_server(self.handle, *self.node_address)
    #     async with server:
    #         await server.serve_forever()

    async def mine_task(self):
        while True:
            if len(self.transaction_pool.get_transactions()) >= 10:
                print("new Block")
                block = self.construct_block()
                self.blockchain.add_block(block)
                # await self.broadcast_block()
                self.transaction_pool.update(block)
            await asyncio.sleep(1)

    def background_task(self):
        event_loop = asyncio.new_event_loop()
        # event_loop.create_task(self.listen_task())
        event_loop.create_task(self.mine_task())
        event_loop.run_forever()

    def run(self):
        # TODO: 启动节点
        # 启用一个线程以asyncio执行监听与打包
        background_thread = threading.Thread(target=self.background_task)
        background_thread.setDaemon(True)
        background_thread.start()
        # 在主线程中进行UI操作、发起交易等操作
        self.ui_task()

Node().run()
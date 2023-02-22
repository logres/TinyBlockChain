from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from source.node import Node

node = Node()

app = FastAPI()

class Client:
    def __init__(self, address, peer, app):
        self.address = address
        self.peer = peer
        self.app = app
    
    def run(self):
        uvicorn.run(app=self.app, host=self.address[0], port=self.address[1])

class UnspentTransaction(BaseModel):
    transaction_hash: str
    index: int
    signature: str

class TransactionOutput(BaseModel):
    address: str
    amount: int

class Transaction(BaseModel):
    input: list[UnspentTransaction]
    output: list[TransactionOutput]

class Block(BaseModel):
    hash: str
    previous_hash: str
    timestamp: int
    nonce: int
    transactions: list[Transaction]

@app.post('/api/local_transaction')
async def local_transaction(transaction: Transaction):
    if node.add_transaction(transaction):
        return {'message': 'success'}
    return {'message': 'fail'}

@app.post("/api/transaction")
async def receive_transaction(transaction: Transaction):
    pass

@app.post("/api/block")
async def receive_block(block: Block):
    if node.add_block(block):
        return {'message': 'success'}
    return {'message': 'fail'}

@app.get("/api/blockchain")
async def asked_for_blockchain():
    pass

@app.get("/api/make_peer")
async def make_peer():
    return client.peer + [client.address]

if __name__ == '__main__':
    address = ('127.0.0.1', 9999)
    client = Client(address, [], app)
    client.run()
# ImmuTexChain – A Persistent, Visual NFT Blockchain
# Features: Full backend + persistent storage + HTML explorer + API

import hashlib
import json
import time
import os
from uuid import uuid4
from flask import Flask, jsonify, request, render_template_string

# ------------------- Persistent Blockchain Storage ------------------- #

CHAIN_FILE = 'chain.json'

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 3

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), [], "0")
        return [genesis_block]

    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, metadata_uri):
        nft_id = str(uuid4())
        self.unconfirmed_transactions.append({
            'nft_id': nft_id,
            'sender': sender,
            'recipient': recipient,
            'metadata_uri': metadata_uri
        })
        return nft_id

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block().hash
        if previous_hash != block.previous_hash:
            return False
        if not proof.startswith('0' * Blockchain.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block()
        new_block = Block(len(self.chain), time.time(), self.unconfirmed_transactions, last_block.hash)
        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.unconfirmed_transactions = []
            return new_block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            data = json.load(f)
        return [Block(**block) for block in data]

# ------------------- Flask App ------------------- #

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    html = """
    <html><head><title>ImmuTexChain</title><style>
    body { font-family: sans-serif; background: #f0f0f0; padding: 20px; }
    .block { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 0 6px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>ImmuTexChain Explorer</h1>
    {% for block in chain %}
    <div class="block">
      <h2>Block #{{ block.index }}</h2>
      <p><b>Timestamp:</b> {{ block.timestamp }}</p>
      <p><b>Hash:</b> {{ block.hash }}</p>
      <p><b>Prev Hash:</b> {{ block.previous_hash }}</p>
      <p><b>Nonce:</b> {{ block.nonce }}</p>
      <ul>
      {% for tx in block.transactions %}
        <li>{{ tx.nft_id }}: {{ tx.sender }} → {{ tx.recipient }} ({{ tx.metadata_uri }})</li>
      {% endfor %}
      </ul>
    </div>
    {% endfor %}
    </body></html>
    """
    chain_data = [block.__dict__ for block in blockchain.chain]
    return render_template_string(html, chain=chain_data)

@app.route('/mint', methods=['POST'])
def mint():
    data = request.get_json()
    if not all(k in data for k in ('sender', 'recipient', 'metadata_uri')):
        return jsonify({'error': 'Missing fields'}), 400
    nft_id = blockchain.add_transaction(data['sender'], data['recipient'], data['metadata_uri'])
    return jsonify({'message': 'NFT added to pool', 'nft_id': nft_id})

@app.route('/mine')
def mine():
    result = blockchain.mine()
    return jsonify({'message': f'Block #{result} mined' if result else 'No transactions to mine'})

@app.route('/chain')
def get_chain():
    return jsonify([block.__dict__ for block in blockchain.chain])

if __name__ == '__main__':
    app.run(debug=True, port=5000)

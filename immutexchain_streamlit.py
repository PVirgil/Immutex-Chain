# immutexchain_streamlit.py – Streamlit UI for ImmuTexChain NFT Blockchain

import streamlit as st
import hashlib
import json
import time
import os
from uuid import uuid4

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

# Streamlit App UI
st.set_page_config(page_title="ImmuTexChain Explorer", layout="centered")
st.title("🔗 ImmuTexChain – Visual NFT Blockchain")

blockchain = Blockchain()

menu = ["View Chain", "Mint NFT", "Mine Block"]
choice = st.sidebar.radio("Navigate", menu)

if choice == "View Chain":
    for block in reversed(blockchain.chain):
        with st.expander(f"Block #{block.index}"):
            st.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            st.write(f"**Hash:** {block.hash}")
            st.write(f"**Previous Hash:** {block.previous_hash}")
            st.write(f"**Nonce:** {block.nonce}")
            st.markdown("**Transactions:**")
            for tx in block.transactions:
                st.markdown(f"- `{tx['nft_id']}`: **{tx['sender']}** → **{tx['recipient']}** (*{tx['metadata_uri']}*)")

elif choice == "Mint NFT":
    st.subheader("Mint a New NFT Transaction")
    sender = st.text_input("Sender")
    recipient = st.text_input("Recipient")
    metadata_uri = st.text_input("Metadata URI")
    if st.button("Mint NFT"):
        if sender and recipient and metadata_uri:
            nft_id = blockchain.add_transaction(sender, recipient, metadata_uri)
            st.success(f"NFT {nft_id} queued for mining")
        else:
            st.error("Please fill all fields")

elif choice == "Mine Block":
    st.subheader("Mine a Block")
    if st.button("Mine Now"):
        mined = blockchain.mine()
        if mined is not False:
            st.success(f"✅ Block #{mined} mined and added to the chain")
        else:
            st.warning("No transactions to mine")

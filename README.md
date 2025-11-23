# 🔗 ImmuTexChain

**ImmuTexChain** is a custom-built, persistent blockchain designed for minting and exploring NFTs with full visual transparency. Unlike traditional blockchain projects focused on tokens or mining rewards, ImmuTexChain emphasizes traceability, integrity, and human-readable interaction.

Deployed with **Vercel**, it offers a sleek interface for users to mint NFTs, mine blocks, and explore the blockchain history — all while maintaining the immutable qualities of a proof-of-work chain.

---

## ⚙️ Features

- 🔐 **Persistent Storage**: Saves the blockchain to `vercel.json` to ensure continuity across sessions.
- 🖼️ **NFT Transaction Support**: Mint NFTs by specifying sender, recipient, and metadata URI.
- 🔨 **Proof-of-Work Mining**: Each block is validated via PoW, ensuring consistency and immutability.
- 📜 **Visual Chain Explorer**: Clean, expandable block viewer with readable transaction history.
- 🚀 **Vercel UI**: No APIs or backend complexity — just launch and interact via the web UI.

---

## 🛠️ Technologies

- Python 3
- Vercel
- Built-in libraries: `hashlib`, `json`, `time`, `uuid`, `os`

---

## 📂 File Structure

```
immutexchain/
│
├── immutexchain_app.py          # Main blockchain + Vercel interface
├── vercel.json                  # Persistent blockchain storage
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

---

## 🧪 Functional Overview

### 🔁 Mint NFT
- Input `Sender`, `Recipient`, and `Metadata URI`
- Mints a new transaction into the pending pool
- Wait for it to be mined into a block

### ⛏️ Mine Block
- Validates all pending transactions via PoW
- Adds a new block to the chain
- Clears the transaction pool after successful mining

### 📜 View Chain
- Visualize all blocks and their contents
- Expand each block to view metadata, hash, nonce, and transactions

---

## 📈 Future Enhancements

- Transaction signatures and block validators
- NFT metadata preview (image/audio rendering)
- Chain export/import between peers
- Analytics: chain growth, transaction volume, minting frequency

---

Built to explore how NFTs and blockchain can be made **transparent, educational, and user-driven** without centralized platforms or token economics.

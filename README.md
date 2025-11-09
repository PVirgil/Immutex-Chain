# 🔗 ImmuTexChain
**ImmuTexChain** is a fully self-hosted, immutable NFT blockchain built entirely in Python using Flask. It features proof-of-work consensus, RESTful endpoints, persistent JSON storage, and a visual HTML explorer — all deployed with zero-cost infrastructure on Koyeb.

Designed for developers, educators, and NFT enthusiasts, ImmuTexChain offers a lightweight and transparent blockchain environment for experimentation and minting, without gas fees or third-party dependencies.

---

## 🚀 Live Demo

👉 [Visit the Live Blockchain Explorer]([https://.koyeb.app](https://colourful-xena-paytonvirgil-e5f8550d.koyeb.app)

---

## 🔧 Features

- ✅ Custom Proof-of-Work blockchain engine
- 🎨 NFT minting with unique IDs and metadata URIs
- ⛏ Manual mining to confirm NFT transactions
- 💾 Persistent storage using `chain.json`
- 🌍 Visual HTML blockchain explorer (via `/`)
- 🔌 RESTful API (`/mint`, `/mine`, `/chain`)
- 🆓 Free cloud deployment (via Koyeb)

---

## 🛠 Tech Stack

- **Backend:** Python 3, Flask
- **Storage:** Local JSON file (`chain.json`)
- **Deployment:** Gunicorn + Koyeb (free-tier cloud)
- **Frontend:** HTML-rendered Flask templates

---

## 🌐 API Reference

### `GET /`
Returns an HTML page rendering all blocks and NFT transactions visually.

### `POST /mint`
Mint a new NFT.  
**Body JSON:**
```json
{
  "sender": "wallet1",
  "recipient": "wallet2",
  "metadata_uri": "https://example.com/nft/metadata.json"
}
```

### `GET /mine`
Mines all unconfirmed NFT transactions into a new block.

### `GET /chain`
Returns full blockchain data as JSON.

---

## 💾 Data Persistence

The blockchain is saved to a `chain.json` file, ensuring all data survives restarts or redeployments. This makes ImmuTexChain ideal for ongoing projects or demonstrations without data loss.

---

## 📊 Use Cases

- Blockchain education and workshops
- NFT prototyping without Ethereum
- Testbed for consensus and storage logic
- Custom or private NFT minting with no fees

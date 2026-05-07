# BlockCheque

### Blockchain-Based Cheque Verification & Clearance System

BlockCheque is a secure and transparent cheque verification system built using **Django, Ethereum Blockchain, Solidity, QR Codes, and OpenCV**. It helps users and banks generate, verify, and clear cheques with immutable blockchain records, reducing fraud and ensuring trust in cheque transactions.

---

## 🚀 Features

* 👤 **User & Bank Registration/Login**
* 📝 **Cheque Generation with QR Code**
* 🔍 **QR Code Scanning & Verification**
* ⛓️ **Blockchain Storage for Immutable Records**
* 🏦 **Bank Clearance System**
* 📊 **Cheque Status Tracking (Pending / Cleared)**
* 🔒 **Fraud Prevention & Transparency**

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Django

### Blockchain

* Solidity
* Ethereum
* Web3.py
* Truffle / Ganache

### Additional Tools

* OpenCV
* PyQRCode

---

## 📂 Project Structure

```bash
BlockCheque/
│
├── MIPL-PY-30-ChequeVerification/
│   ├── ChequeApp/          # Main Django application
│   ├── Cheque/             # Django project settings
│   ├── hello-eth/          # Truffle smart contract setup
│   ├── Cheque.sol          # Solidity smart contract
│   ├── Cheque.json         # Compiled ABI
│   ├── manage.py           # Django management script
│   └── runServer.bat       # Run server script
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/EbenezerJoshua/BlockCheque.git
cd BlockCheque
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Ethereum Local Blockchain

Install and run:

* Ganache
* Truffle

### 5️⃣ Deploy Smart Contract

```bash
truffle migrate
```

### 6️⃣ Run Django Server

```bash
python manage.py runserver
```

---

## 🔄 How It Works

### User Side

1. Register/Login
2. Generate cheque
3. QR code is created
4. Cheque data stored on blockchain

### Bank Side

1. Login
2. Scan cheque QR code
3. Verify blockchain data
4. Clear cheque securely

---

## 📸 Core Workflow

**Generate → Scan → Verify → Clear → Immutable Record**

---

## 🔐 Why BlockCheque?

Traditional cheque systems are vulnerable to:

* Fraud
* Duplicate clearance
* Data tampering

BlockCheque solves this using blockchain by ensuring:

* Transparency
* Security
* Tamper-proof verification
* Real-time cheque status

---

## 📦 Dependencies

```txt
Django==2.1.7
web3==4.7.2
PyQRCode==1.2.1
pypng==0.0.21
opencv-python==4.1.1.26
opencv-contrib-python==4.3.0.36
requests==2.28.1
urllib3==1.26.18
```

---

## 🎯 Future Improvements

* Multi-bank integration
* Mobile app support
* Cloud blockchain deployment
* OCR cheque data extraction
* AI fraud detection

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repository and submit pull requests.

---

## 📜 License

This project is for educational and research purposes.

---

## 👨‍💻 Author - Ebenezer Joshua

Developed with innovation to modernize cheque security using blockchain.

# BlockCheque Architecture & Codebase Report

## 1. Executive Summary
BlockCheque is a decentralized application (DApp) that digitizes the cheque generation and clearance process. It replaces traditional paper cheques and centralized databases with QR codes and an Ethereum-based blockchain. The core innovation of this project is that it uses a **Django backend** to serve the web interface and process logic, but **relies entirely on a Solidity Smart Contract** as its primary database for both user authentication and cheque records.

## 2. High-Level Architecture
The architecture follows a classic Client-Server-Blockchain model:

*   **Frontend (Client):** Rendered server-side using Django HTML templates, vanilla CSS, and JavaScript.
*   **Backend (Server):** A Python Django application (`ChequeApp`). It handles form submissions, generates QR codes, reads QR codes using OpenCV, sends email notifications, and acts as the bridge to the blockchain.
*   **Blockchain (Database/Storage):** A local Ethereum node (expected to be Ganache) running a Solidity Smart Contract (`Cheque.sol`). The contract stores all state, including registered users, bank accounts, and cheque hash values.

**Communication Flow:**
`Browser` <--(HTTP)--> `Django Views` <--(Web3.py RPC)--> `Ethereum Node (Ganache)`

## 3. Codebase Structure
The repository is localized in the `/code/` directory, which contains the entire application.

### The Django Project & App
*   **`code/manage.py`**: The standard Django entry point for running the server and administrative commands.
*   **`code/Cheque/`**: The Django project configuration folder (contains `settings.py`, root `urls.py`, etc.).
*   **`code/ChequeApp/`**: The main application folder where all the logic resides.
    *   **`views.py`**: **The heart of the application.** It contains all backend logic. There are no Django models used; instead, `views.py` connects directly to the smart contract via `web3.py`.
    *   **`urls.py`**: Maps web routes (e.g., `/BankLoginAction`, `/GenerateCheque`) to their respective functions in `views.py`.
    *   **`models.py`**: Notably empty. The application bypasses Django's ORM and database in favor of the blockchain.
    *   **`templates/`**: Contains all the HTML files (`index.html`, `UserScreen.html`, `BankScreen.html`, etc.).
    *   **`static/`**: Contains CSS (`style.css`), images, and a `files/` directory where generated QR codes are temporarily and permanently stored as `.png` files.

### The Blockchain Component
*   **`code/Cheque.sol`**: The Solidity smart contract. It defines two main structs: `user` (stores username, email, password, role) and `cheque` (stores the QR code hash and status).
*   **`code/Cheque.json`**: The compiled Application Binary Interface (ABI) of the smart contract, used by Python to understand how to interact with the deployed contract.
*   **`code/hello-eth/`**: A Truffle project directory containing the setup (`truffle-config.js`) and migration scripts (`2_deploy_contracts.js`) required to compile and deploy `Cheque.sol` to a local blockchain.

## 4. How the Core Mechanisms Work

### A. User Authentication (Registration & Login)
1.  When a user registers, `views.py` calls `contract.functions.createUser()` to store their username, password, and role ("User" or "Bank") directly on the blockchain.
2.  When logging in, `views.py` fetches the total user count from the blockchain, loops through **every single user**, and checks if the provided username, password, and role match. 

### B. Cheque Generation
1.  A user selects a Bank, a Receiver, and an Amount.
2.  `views.py` creates a string formatted as `sender#bank#receiver#amount#date`.
3.  The `pyqrcode` library generates a QR code image from this string, which is saved as `test.png`.
4.  The application calculates a **SHA-256 hash** of the QR code image file.
5.  The image is renamed to `<sha256hash>.png` and stored in the `static/files/` directory.
6.  The hash string is sent to the blockchain via `contract.functions.createCheque()` with a "Pending" status.

### C. Cheque Verification & Clearance
1.  A Bank logs in and views the dashboard.
2.  The application fetches all cheques from the blockchain. For each cheque, it uses **OpenCV (`cv2.QRCodeDetector`)** to scan the corresponding `<sha256hash>.png` image from the static folder and decodes the `sender#bank...` string to display the data.
3.  When the Bank clicks "Clear Cheque", `views.py` calls `contract.functions.updateStatus()` to change the blockchain status to "Cleared".
4.  The application then uses Python's `smtplib` to send a notification email (via a hardcoded Gmail SMTP account) to both the Sender and the Receiver.

## 5. Key Architectural Observations
*   **Stateless Django**: The Django backend is entirely stateless. It relies on the Ethereum node for all data persistence. `db.sqlite3` exists but is unused by the core app.
*   **Hardcoded Contract Address**: In `views.py`, the deployed contract address (`0xe419ABC4F29c9157417a834e1ac92081153e61b9`) is hardcoded. If the contract is redeployed (e.g., on a fresh Ganache workspace), this address must be manually updated in the code for the app to work.
*   **Off-Chain Data**: The actual details of the cheque (Amount, Receiver, etc.) are *not* stored on the blockchain. They are embedded in the QR code image, which is stored locally on the server. Only the *hash* of the image is stored on the blockchain. This acts as proof of integrity, preventing tampering with the QR code.
*   **Security/Performance**: User authentication loops through the entire user base on the blockchain sequentially, which works fine for a local prototype but would be a performance bottleneck in production. Passwords are also stored in plain text on the blockchain.

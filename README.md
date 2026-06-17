# Institutional Certificate Verification for Fraud Detection through a Blockchain-Based Framework (BCVFD)

## Overview

The Blockchain-Based Certificate Verification and Fraud Detection (BCVFD) framework is a secure and decentralized system designed to verify institutional certificates and detect certificate forgery using blockchain technology. The framework leverages Ethereum smart contracts, SHA-256 cryptographic hashing, QR-code-based verification, and a Flask web application to ensure certificate authenticity, integrity, and transparency.

Instead of storing complete certificates on-chain, BCVFD stores only the SHA-256 hash of each certificate, reducing storage overhead while preserving privacy and tamper resistance.

---

## Research Publication

This repository accompanies the research work:

**Institutional Certificate Verification for Fraud Detection through a Blockchain-Based Framework (BCVFD)**

The repository is provided to support reproducibility and further research in blockchain-enabled certificate verification systems.

---

## Key Features

* Blockchain-based certificate verification
* SHA-256 certificate integrity validation
* Ethereum smart contract integration
* QR-code-based certificate authentication
* Tamper detection through hash comparison
* Lightweight on-chain storage
* Flask web-based user interface
* Fraud detection for modified and fabricated certificates

---

## System Architecture

```text
Institution Administrator
          |
          v
   Certificate Upload
          |
          v
      SHA-256 Hashing
          |
          v
 Ethereum Smart Contract
          |
          v
      Blockchain
          |
          v
      QR Code Generation
          |
          v
Student / Certificate Holder
          |
          v
Verifier Uploads or Scans QR Code
          |
          v
Hash Recalculation and Comparison
          |
          v
Valid / Invalid Certificate Decision
```

---

## Technology Stack

### Backend

* Python
* Flask

### Blockchain

* Ethereum
* Solidity
* Ganache
* Web3.py

### Security

* SHA-256 Cryptographic Hashing

### Additional Tools

* QR Code Generation
* MetaMask
* Remix IDE

---

## Project Structure

```text
├── Main.py
├── RunWebCam.py
├── CertificateVerification.json
├── templates/
├── static/
├── certificate_templates/
├── CertificateVerification/
└── README.md
```

---

## Installation

### Prerequisites

* Python 3.x
* Ganache
* MetaMask
* Node.js (optional)
* Ethereum development environment


### Clone Repository

```bash
git clone https://github.com/Dulal-CSEcode/Institutional-Certificate-Verification-for-Fraud-Detection-through-a-Blockchain-Based-Framework.git
cd BCVFD
````


### Install Dependencies

```bash
pip install flask
pip install web3
pip install pyqrcode
pip install pypng
```

Or

```bash
pip install -r requirements.txt
```

---

## Blockchain Setup

### Step 1: Start Ganache

Launch Ganache and create a local Ethereum workspace.

Example:

```text
RPC Server:
http://127.0.0.1:7545
```

### Step 2: Deploy Smart Contract

Deploy the Solidity contract using Remix IDE or Truffle.

Update:

```python
deployed_contract_address = "0x9895084d88973BA054173364a87EF843DBCc9319"
```

inside:

```python
Main.py
```

### Step 3: Update ABI File

Place the generated ABI JSON file as:

```text
CertificateVerification.json
```

---

## Running the Application

```bash
python Main.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Workflow

### Certificate Issuance

1. Administrator uploads certificate.
2. SHA-256 hash is generated.
3. Hash is stored on Ethereum blockchain.
4. QR code is generated.
5. Certificate is issued.

### Certificate Verification

1. Verifier uploads certificate or scans QR code.
2. SHA-256 hash is recomputed.
3. Blockchain-stored hash is retrieved.
4. Hashes are compared.
5. Verification result is displayed.

---

## Experimental Results

Experiments were conducted using a local Ethereum simulation environment (Ganache).

| Metric                            | Result     |
| --------------------------------- | ---------- |
| Certificate Issuing Time          | ~7 seconds |
| Certificate Verification Time     | ~2 seconds |
| Certificate Issuing Gas Cost      | 48,000     |
| Certificate Verification Gas Cost | 28,000     |

Note: Results were obtained in a controlled Ganache-based Ethereum simulation environment and may differ under public blockchain deployments.

---

## Security Considerations

The framework stores only certificate hashes rather than complete certificate files, reducing privacy exposure and blockchain storage requirements.

Current implementation focuses on:

* Certificate integrity verification
* Tamper detection
* Fraudulent certificate identification

Future versions will incorporate:

* Certificate revocation
* Multi-signature authorization
* Decentralized identity integration
* Cross-institution governance

---



















<!--
## Limitations

* Evaluated in a local Ganache environment
* No certificate revocation mechanism
* Single-administrator deployment model
* Limited multi-institution interoperability
* No large-scale public blockchain evaluation

---

## Future Work

* Integration with IPFS
* Layer-2 blockchain deployment
* Multi-institution governance framework
* User-centered usability evaluation
* Real-world deployment and benchmarking

---

## License

This project is provided for academic and research purposes.

---

## Citation

If you use this repository in your research, please cite:

```bibtex
@article{BCVFD2026,
  title={Institutional Certificate Verification for Fraud Detection through a Blockchain-Based Framework},
  author={Hossain, Md. Dulal and others},
  year={2026}
}
```
-->











---

## Contact

#Md. Dulal Hossain,

Officer & Research Assistant, 

Canadian University of Bangladesh

Email: [dulal.md.cse@gmail.com](mailto:dulal.md.cse@gmail.com)

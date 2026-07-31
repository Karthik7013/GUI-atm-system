
# ATM Management Application

This project is a Python-based ATM management application with a graphical user interface (GUI-Tkinter). It uses SQLite for database storage and follows a layered architecture (models, repositories, services, UI).

## Technologies

<img width="50px" src="https://ik.imagekit.io/ybyfbcvb8/python.png?updatedAt=1692968478421"/> <img width="50px" src="https://ik.imagekit.io/ybyfbcvb8/62c46cd2a75b8945b1696713.png?updatedAt=1692968811131"/>

## Architecture

- **models/** — Database initialization and schema definitions
- **repositories/** — Data access layer (user and transaction repositories)
- **services/** — Business logic layer (auth, account, transaction services)
- **utils/** — Shared utilities (validators, security, exceptions, logging)
- **ui/** — Reusable UI components (dialogs, input fields)
- **config.py** — Application configuration (colors, paths, window size)

## Features

- User registration with strong PIN validation
- Login with hashed PIN verification
- Withdraw money (multiples of 100)
- Deposit money
- Transfer money between accounts
- Balance enquiry
- PIN change
- Transaction history
- Audit logging

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

## Modules Used

- Tkinter — Graphical user interface (GUI)
- sqlite3 — Database connectivity
- re — Password/PIN validation
- PIL — Loading images and icons
- datetime — Transaction timestamps

     

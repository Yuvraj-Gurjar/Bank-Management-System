# 🏦 Bank Management System

A robust, interactive **Bank Management System** built with Python and Streamlit (UI), along with a standalone HTML/Tailwind web dashboard. The system manages core banking operations including account creation, deposits, withdrawals, profile updates, and account deletions with persistent data storage.

---

## ✨ Features

- **Dashboard & System Metrics:** Real-time summary displaying total registered users, total vault capital, average customer balance, and a search/view directory of users.
- **Unique Account ID Generation:** Custom algorithm generating secure 8-character account IDs consisting of 3 random letters, 3 digits, and 2 special characters.
- **Account Creation:** Strict validation ensuring account holders are 18+ years old and set a secure 4-digit PIN.
- **Deposit Operations:** Accepts valid deposits (limit: ₹1 to ₹10,000 per transaction) and updates balances instantly.
- **Withdrawal Operations:** Ensures sufficient balance before permitting cash withdrawals.
- **Profile Management:** Allows updating sensitive details (Name, Email, PIN) while preserving immutable core records (Account ID, Age, Balance).
- **Account Deletion:** Confirmation mechanism to permanently erase records from the system.
- **Data Persistence:** Automatically stores user data in local `data.json` (Streamlit version) or browser `localStorage` (Web Dashboard version).

---

## 📁 Project Structure

```text
Bank-Management-Project/
│
├── app.py              # Main Streamlit web application
├── index.html          # Alternative web UI (Tailwind CSS + Pure JS)
├── data.json           # JSON Database (Auto-generated upon first run)
└── README.md           # Project Documentation
```

---

## 🛠️ Prerequisites & Setup

### 1. Clone or Download Project
Ensure all files are placed in your working project folder.

### 2. Create & Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Installation

Install required dependencies using `pip`:

```bash
pip install streamlit
```

---

## 🚀 Running the Application

### Option 1: Streamlit Dashboard (Python)

Run the following command in your activated terminal:

```bash
streamlit run app.py
or
python -m streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.

### Option 2: HTML/JS Single-File Interface

Double-click `index.html` or open it in any web browser. No Python environment is required for this lightweight frontend version.

---

## 📄 JSON Database Schema (`data.json`)

```json
[
    {
        "name": "Jane Doe",
        "age": 25,
        "email": "jane@example.com",
        "pin": 1234,
        "accountNo": "aBc123!@",
        "balance": 5000
    }
]
```

---

## 🛡️ Business Rules & Safeguards

| Action | Constraint / Requirement |
| :--- | :--- |
| **Account Creation** | Age must be $\ge 18$; PIN must be exactly 4 digits. |
| **Deposit** | Deposit amount must be between ₹1 and ₹10,000. |
| **Withdrawal** | Balance cannot fall below ₹0. |
| **Profile Updates** | Age, Account Number, and Balance cannot be modified. |

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for bug fixes or new features (such as transfer operations or transaction logs).
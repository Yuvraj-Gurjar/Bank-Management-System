import json
import random
import string
from pathlib import Path
import streamlit as st

# Set page layout and title
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


class Bank:
    database = 'data.json'

    @classmethod
    def load_data(cls):
        """Loads data from the JSON file."""
        if Path(cls.database).exists():
            try:
                with open(cls.database, 'r') as fs:
                    content = fs.read().strip()
                    return json.loads(content) if content else []
            except Exception as err:
                st.error(f"Error loading database: {err}")
                return []
        return []

    @classmethod
    def save_data(cls, data):
        """Saves data back to the JSON file."""
        try:
            with open(cls.database, 'w') as fs:
                json.dumps(data)
                json.dump(data, fs, indent=4)
        except Exception as err:
            st.error(f"Error saving data: {err}")

    @staticmethod
    def generate_account_no():
        """Generates a random account number (3 letters, 3 digits, 2 special chars)."""
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchr = random.choices("!@#$%^&*()", k=2)
        acc_id = alpha + num + spchr
        random.shuffle(acc_id)
        return "".join(acc_id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        """Creates a new user account."""
        data = cls.load_data()
        
        if age < 18:
            return False, "Age must be 18 or above to create an account."
        if len(str(pin)) != 4 or not str(pin).isdigit():
            return False, "PIN must be exactly 4 digits."
        
        acc_no = cls.generate_account_no()
        new_account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": int(pin),
            "accountNo": acc_no,
            "balance": 0
        }
        
        data.append(new_account)
        cls.save_data(data)
        return True, new_account

    @classmethod
    def get_account(cls, acc_number, pin):
        """Retrieves an account matching account number and PIN."""
        data = cls.load_data()
        for user in data:
            if user['accountNo'] == acc_number and user['pin'] == int(pin):
                return user, data
        return None, data

    @classmethod
    def deposit_money(cls, acc_number, pin, amount):
        user, data = cls.get_account(acc_number, pin)
        if not user:
            return False, "Invalid Account Number or PIN."
        
        if amount <= 0 or amount > 10000:
            return False, "Amount must be greater than 0 and up to 10,000."
        
        user['balance'] += amount
        cls.save_data(data)
        return True, f"Successfully deposited ₹{amount:.2f}. New Balance: ₹{user['balance']:.2f}"

    @classmethod
    def withdraw_money(cls, acc_number, pin, amount):
        user, data = cls.get_account(acc_number, pin)
        if not user:
            return False, "Invalid Account Number or PIN."
        
        if amount <= 0:
            return False, "Please enter a valid amount greater than 0."
        if user['balance'] < amount:
            return False, f"Insufficient balance. Current balance is ₹{user['balance']:.2f}"
        
        user['balance'] -= amount
        cls.save_data(data)
        return True, f"Successfully withdrew ₹{amount:.2f}. Remaining Balance: ₹{user['balance']:.2f}"

    @classmethod
    def update_details(cls, acc_number, pin, new_name, new_email, new_pin):
        user, data = cls.get_account(acc_number, pin)
        if not user:
            return False, "Invalid Account Number or PIN."
        
        if new_name.strip():
            user['name'] = new_name.strip()
        if new_email.strip():
            user['email'] = new_email.strip()
        if new_pin.strip():
            if len(new_pin.strip()) == 4 and new_pin.strip().isdigit():
                user['pin'] = int(new_pin.strip())
            else:
                return False, "New PIN must be exactly 4 digits."
        
        cls.save_data(data)
        return True, "Account details updated successfully!"

    @classmethod
    def delete_account(cls, acc_number, pin):
        user, data = cls.get_account(acc_number, pin)
        if not user:
            return False, "Invalid Account Number or PIN."
        
        data.remove(user)
        cls.save_data(data)
        return True, "Account deleted successfully."


# App Header
st.markdown('<div class="main-header">🏦 Bank Management Portal</div>', unsafe_allow_html=True)

# Navigation Menu
menu = ["Dashboard / Overview", "Create Account", "Deposit Money", "Withdraw Money", "View Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

st.sidebar.markdown("---")
st.sidebar.info("📌 **Note**: Storage persists in local `data.json`.")


# -------------------- DASHBOARD --------------------
if choice == "Dashboard / Overview":
    st.subheader("📊 System Overview")
    data = Bank.load_data()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Accounts Registered", value=len(data))
    with col2:
        total_balance = sum(item['balance'] for item in data) if data else 0
        st.metric(label="Total Funds Deposited", value=f"₹{total_balance:,.2f}")
    with col3:
        avg_balance = total_balance / len(data) if data else 0
        st.metric(label="Average Balance / Account", value=f"₹{avg_balance:,.2f}")
    
    st.markdown("---")
    st.subheader("📋 Registered Users Quick List")
    if data:
        summary_data = [
            {
                "Account No": u["accountNo"],
                "Name": u["name"],
                "Email": u["email"],
                "Balance (₹)": u["balance"]
            }
            for u in data
        ]
        st.dataframe(summary_data, use_container_width=True)
    else:
        st.info("No user accounts found in the database. Create one to get started!")


# -------------------- CREATE ACCOUNT --------------------
elif choice == "Create Account":
    st.subheader("🆕 Create New Bank Account")
    
    with st.form("create_acc_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=18)
        email = st.text_input("Email Address")
        pin = st.text_input("Set 4-Digit Secret PIN", type="password", max_chars=4)
        
        submitted = st.form_submit_button("Submit & Create Account")
        
        if submitted:
            if not name or not email or not pin:
                st.error("Please fill in all mandatory fields.")
            else:
                success, result = Bank.create_account(name, age, email, pin)
                if success:
                    st.success("🎉 Account created successfully!")
                    st.json(result)
                    st.warning("⚠️ Please note down your Account Number and PIN carefully!")
                else:
                    st.error(f"❌ Creation Failed: {result}")


# -------------------- DEPOSIT MONEY --------------------
elif choice == "Deposit Money":
    st.subheader("💵 Deposit Funds")
    
    col1, col2 = st.columns(2)
    with col1:
        acc_no = st.text_input("Account Number")
    with col2:
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        
    amount = st.number_input("Deposit Amount (Max ₹10,000 per transaction)", min_value=1, max_value=10000, value=500)
    
    if st.button("Deposit Amount"):
        if not acc_no or not pin:
            st.error("Please enter both Account Number and PIN.")
        else:
            success, msg = Bank.deposit_money(acc_no, pin, amount)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ Deposit Failed: {msg}")


# -------------------- WITHDRAW MONEY --------------------
elif choice == "Withdraw Money":
    st.subheader("💸 Withdraw Funds")
    
    col1, col2 = st.columns(2)
    with col1:
        acc_no = st.text_input("Account Number")
    with col2:
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        
    amount = st.number_input("Withdrawal Amount", min_value=1, value=500)
    
    if st.button("Withdraw Amount"):
        if not acc_no or not pin:
            st.error("Please enter both Account Number and PIN.")
        else:
            success, msg = Bank.withdraw_money(acc_no, pin, amount)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ Withdrawal Failed: {msg}")


# -------------------- VIEW DETAILS --------------------
elif choice == "View Details":
    st.subheader("👤 View Account Details")
    
    col1, col2 = st.columns(2)
    with col1:
        acc_no = st.text_input("Account Number")
    with col2:
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        
    if st.button("Fetch Details"):
        if not acc_no or not pin:
            st.error("Please provide both Account Number and PIN.")
        else:
            user, _ = Bank.get_account(acc_no, pin)
            if user:
                st.success("Details fetched successfully!")
                st.write(f"**Name:** {user['name']}")
                st.write(f"**Age:** {user['age']}")
                st.write(f"**Email:** {user['email']}")
                st.write(f"**Account Number:** {user['accountNo']}")
                st.write(f"**Current Balance:** ₹{user['balance']:.2f}")
            else:
                st.error("❌ Account not found or incorrect PIN.")


# -------------------- UPDATE DETAILS --------------------
elif choice == "Update Details":
    st.subheader("⚙️ Update Profile Information")
    st.caption("Note: You cannot modify Age, Account Number, or Balance.")
    
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Current 4-Digit PIN", type="password", max_chars=4)
    
    st.markdown("---")
    st.write("##### Fields to Update (Leave blank to keep existing value)")
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_pin = st.text_input("New 4-Digit PIN (optional)", type="password", max_chars=4)
    
    if st.button("Update Account Information"):
        if not acc_no or not pin:
            st.error("Account Number and current PIN are required for verification.")
        else:
            success, msg = Bank.update_details(acc_no, pin, new_name, new_email, new_pin)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ Update Failed: {msg}")


# -------------------- DELETE ACCOUNT --------------------
elif choice == "Delete Account":
    st.subheader("🗑️ Delete Account")
    st.warning("⚠️ Warning: Deleting an account is permanent and cannot be undone!")
    
    acc_no = st.text_input("Account Number to Delete")
    pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
    confirm = st.checkbox("I confirm that I want to delete this account permanently.")
    
    if st.button("Delete My Account"):
        if not confirm:
            st.warning("Please check the confirmation box to proceed.")
        elif not acc_no or not pin:
            st.error("Please provide Account Number and PIN.")
        else:
            success, msg = Bank.delete_account(acc_no, pin)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ Deletion Failed: {msg}")
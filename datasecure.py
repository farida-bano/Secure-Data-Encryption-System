import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import pbkdf2_hmac

# === Constants ===
DATA_FILE = "secure_data.json"
SALT = b"secure_salt_value"
LOCKOUT_DURATION = 60  # in seconds

# === Session State Initialization ===
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

# === Data Load/Save Functions ===
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# === Crypto Utilities ===
def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key)

def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()

def encrypt_text(text, key):
    cipher = Fernet(generate_key(key))
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    try:
        cipher = Fernet(generate_key(key))
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception:
        return None

stored_data = load_data()

# === Navigation Bar ===
st.title("🔐 Secure Data Encryption System")
menu = ["🏠 Home", "📝 Register", "🔐 Login", "💾 Store Data", "📂 Retrieve Data"]
choice = st.sidebar.selectbox("🔎 Navigation", menu)

# === Home Page ===
if choice == "🏠 Home":
    st.subheader("Welcome to the Secure Data Encryption System! 🛡️")
    st.markdown("""
    - 🔑 Users can **store** data using a unique **passkey**
    - 🔓 Users can **decrypt** the data using the correct passkey
    - 🔁 Multiple failed attempts result in **forced re-login**
    - ⚙️ All data is stored **locally** in memory (no external DB)
    """)

# === Register Page ===
elif choice == "📝 Register":
    st.subheader("Register New User 🧾")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    if st.button("Register 🟢"):
        if username in stored_data:
            st.warning("⚠️ User already exists.")
        elif not username or not password:
            st.error("❗ Both fields are required.")
        else:
            stored_data[username] = {
                "password": hash_password(password),
                "data": []
            }
            save_data(stored_data)
            st.success("✅ User registered successfully!")

# === Login Page ===
elif choice == "🔐 Login":
    st.subheader("User Login 🔐")

    if time.time() < st.session_state.lockout_time:
        remaining = int(st.session_state.lockout_time - time.time())
        st.error(f"⏳ Too many failed attempts. Please wait {remaining} seconds.")
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login 🔑"):
            if username in stored_data and stored_data[username]["password"] == hash_password(password):
                st.session_state.authenticated_user = username
                st.session_state.failed_attempts = 0
                st.success(f"👋 Welcome, {username}!")
            else:
                st.session_state.failed_attempts += 1
                st.error("❌ Invalid credentials.")
                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time() + LOCKOUT_DURATION
                    st.session_state.failed_attempts = 0

# === Store Data Page ===
elif choice == "💾 Store Data":
    if not st.session_state.authenticated_user:
        st.warning("⚠️ Please login first.")
    else:
        st.subheader("Store Encrypted Data 🔐")
        data = st.text_area("Enter your data here 📝")
        passkey = st.text_input("Passkey (for encryption) 🔑", type="password")

        if st.button("Encrypt and Save 💾"):
            if data and passkey:
                encrypted = encrypt_text(data, passkey)
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted)
                save_data(stored_data)
                st.success("✅ Data encrypted and saved!")
            else:
                st.error("❗ All fields are required.")

# === Retrieve Data Page ===
elif choice == "📂 Retrieve Data":
    if not st.session_state.authenticated_user:
        st.warning("⚠️ Please login first.")
    else:
        st.subheader("Retrieve Your Data 🔍")
        user_data = stored_data[st.session_state.authenticated_user]["data"]
        if not user_data:
            st.info("📭 No data stored.")
        else:
            passkey = st.text_input("Enter your passkey to decrypt 🔑", type="password")
            if st.button("Decrypt Data"):
                if passkey:
                    for i, item in enumerate(user_data, 1):
                        decrypted = decrypt_text(item, passkey)
                        if decrypted:
                            st.success(f"📄 Data {i}: {decrypted}")
                        else:
                            st.error(f"🔒 Data {i}: Incorrect passkey or corrupted data.")
                else:
                    st.error("❗ Passkey is required.")

# Secure-Data-Encryption-System
https://secure-data-encryption-system-8abppciiaebbfst6lj4iey.streamlit.app/
🔐 Key Features:
User Registration & Login

Naya user register kar sakta hai.

Existing user login kar sakta hai.

3 wrong login attempts ke baad lockout ho jata hai 60 seconds ke liye.

Data Encryption & Storage

Logged-in user koi bhi text encrypt karke store kar sakta hai using a passkey.

Data Decryption & Retrieval

User apni stored data ko decrypt kar sakta hai agar correct passkey de.

Local Storage

Saara data (passwords + encrypted data) locally secure_data.json file mein save hota hai.

🔧 Technical Breakdown:

Section	Explanation
hash_password()	Passwords ko hash karta hai for secure storage.
generate_key()	Passkey se encryption key banata hai using PBKDF2.
encrypt_text() / decrypt_text()	Text ko encrypt/decrypt karta hai using Fernet (AES-based encryption).
st.session_state	Login sessions, failed attempts, aur lockout time handle karta hai.
load_data() / save_data()	Data file se JSON data load/save karta hai.
📚 Pages:
🏠 Home
Welcome message + system ka overview.

📝 Register
New user create karta hai (username + password).

🔐 Login
User login karta hai. Wrong credentials = failed attempts count.

💾 Store Data
User text encrypt karke save karta hai using passkey.

📂 Retrieve Data
User encrypted data ko decrypt karta hai with correct passkey.


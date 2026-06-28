import os

content = """

add("Projects", "Walk me through the architecture and security features of your Password Manager project.", \"\"\"
* **Overview**: I built a secure Password Manager application that allows users to store, retrieve, and generate strong passwords.
* **Architecture**: 
  - **Frontend**: A React or vanilla JS interface for users to log in, view their vault, and add new credentials.
  - **Backend**: A Node.js/Express or Python/FastAPI backend to handle authentication and encrypted data storage.
  - **Database**: PostgreSQL or MongoDB to store user accounts and their encrypted password vaults.
* **Core Security Features**:
  1. **Master Password**: Users authenticate with a Master Password that is never stored in plaintext.
  2. **Zero-Knowledge Architecture (Client-Side Encryption)**: The actual passwords in the vault are encrypted on the client side before being sent to the server. The server only stores the encrypted ciphertext and never sees the decryption key.
  3. **Data in Transit**: Enforced HTTPS/TLS for all communications to prevent Man-In-The-Middle (MITM) attacks.
\"\"\")

add("Projects", "How did you ensure that user passwords were safe from both database leaks and internal server compromises?", \"\"\"
* **Authentication (Protecting the Master Password)**: 
  - When a user signs up, their Master Password is hashed using a strong key derivation function like **bcrypt** or **PBKDF2** with a unique random **salt**. 
  - If the database is leaked, attackers only get the hashes and salts, making brute-forcing computationally expensive.
* **Vault Encryption (Protecting Stored Passwords)**:
  - I used **AES-256-GCM** (Advanced Encryption Standard with Galois/Counter Mode), which provides both confidentiality and data integrity (authenticated encryption).
  - The encryption key is derived from the user's Master Password (using PBKDF2). 
  - Crucially, encryption and decryption happen **on the client side** (in the browser). The backend only receives and stores the AES-encrypted strings. Therefore, even if the server is compromised or an admin looks at the database, they cannot read the user's saved passwords (Zero-Knowledge).
\"\"\")

add("Projects", "How did you manage user sessions and authentication in your Password Manager?", \"\"\"
* **JWT (JSON Web Tokens)**: Upon successful login (verifying the bcrypt hash of the Master Password), the server issues a JWT.
* **Security Measures for JWT**:
  1. **Short Expiration**: Tokens expire quickly (e.g., 15 minutes) to limit the window of opportunity if a token is stolen.
  2. **Refresh Tokens**: Used an HttpOnly, Secure cookie to store a longer-lived refresh token, which is used to obtain new access tokens without re-entering the Master Password.
  3. **HttpOnly Cookies**: By storing the JWT or refresh token in HttpOnly cookies, I protected the session against Cross-Site Scripting (XSS) attacks, as JavaScript cannot access the token.
  4. **CSRF Protection**: Implemented Anti-CSRF tokens to ensure that requests to modify the vault originated from the legitimate frontend.
\"\"\")
"""

with open('data/db_projects.py', 'a', encoding='utf-8') as f:
    f.write(content)

import os

content = """

add("Projects", "How did you handle the deployment and serving of the heavy CNN model in your Fashion Recommender system?", \"\"\"
* **Model Serving**: Serving a large deep learning model (like VGG16/ResNet) directly within a synchronous web framework can cause massive bottlenecks. Instead, I decoupled the model inference using **FastAPI** (or TensorFlow Serving/ONNX Runtime).
* **Optimization**:
  1. **ONNX Conversion**: Converted the PyTorch/Keras model to ONNX format to optimize the computation graph and reduce inference latency by ~30%.
  2. **Batching**: Configured dynamic batching on the inference server to group multiple concurrent image requests together, maximizing GPU/CPU utilization.
  3. **Caching**: Stored the extracted feature vectors in the Vector Database. Inference is only required for *new* images uploaded by users. Pre-existing database images do not need to be re-run through the CNN.
\"\"\")

add("Projects", "How would you handle a scenario where a user forgets their Master Password in your Zero-Knowledge Password Manager?", \"\"\"
* **The Zero-Knowledge Dilemma**: Because the encryption key is derived entirely from the Master Password on the client side, if the user forgets the Master Password, the server cannot restore access to the encrypted vault. The data is mathematically unrecoverable.
* **Mitigation Strategies**:
  1. **Emergency Kit**: During onboarding, users are prompted to download or print an 'Emergency Kit' PDF. This document contains a hint for their Master Password and a secondary randomly generated 'Secret Key' used to salt their login on new devices.
  2. **Vault Reset**: If all access is lost, I implemented an account recovery flow verified via Email/2FA. This allows the user to regain access to their *account*, but their previous vault is wiped clean and re-initialized with a new Master Password.
  3. **Biometric Fallback**: On mobile/desktop apps, users can unlock the vault using FaceID/TouchID (where the derived encryption key is securely stored in the device's Secure Enclave) if they temporarily forget the password.
\"\"\")

add("BloodBridge AI", "Can you elaborate on the Machine Learning models used in BloodBridge AI for donor churn and patient urgency?", \"\"\"
* **Donor Churn Prediction (XGBoost Classifier)**: 
  - We trained an XGBoost model to predict if a donor is at high risk of becoming inactive.
  - **Features**: Days since last donation, total donation count, response rate to previous alerts, age, and geographic distance to the nearest clinic.
  - **Action**: If the probability of churn exceeds 75%, the Gamification/Planner agent is triggered to send personalized appreciation messages or voice calls to re-engage the donor.
* **Patient Urgency Scoring (XGBoost Regressor)**:
  - We needed a dynamic way to rank patients during a shortage.
  - **Features**: Current Hemoglobin (Hb) levels, days elapsed since their last transfusion cycle, age, and boolean flags for cardiac/liver complications.
  - **Output**: The model outputs a continuous urgency score (1.0 to 10.0). The LangGraph workflow uses this score to prioritize matching and allocate the rarest blood types (e.g., O-negative, Kell-negative) to the most critical patients first.
\"\"\")
"""

with open('data/db_projects.py', 'a', encoding='utf-8') as f:
    f.write(content)

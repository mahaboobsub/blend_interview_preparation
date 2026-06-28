import os

content = """

# ═══════════════════════════════════════════════════════════════
# BLOODBRIDGE AI (10)
# ═══════════════════════════════════════════════════════════════

add("BloodBridge AI", "Why did you choose FastAPI over Node.js for the backend in this project?", \"\"\"
FastAPI was chosen because the core capabilities of our system are Python-heavy:
* **Machine Learning & Analytics**: We are running XGBoost classifiers for donor churn risk, regression for patient urgency scoring, and Scipy's Hungarian algorithm for matching optimization. Running this in Node.js would require spawning a subprocess or communicating with a Python sidecar.
* **LangGraph Agentic Workflow**: The state-driven orchestration framework is Python-native.
* **Low Latency & Async**: FastAPI handles highly concurrent, asynchronous requests natively using uvicorn, which is critical for real-time WebSocket broadcasting and webhook ingestion. Adding Node.js would introduce structural overhead without any performance benefit.
\"\"\")

add("BloodBridge AI", "How did you implement real-time updates for the frontend dashboard?", \"\"\"
We built a centralized ConnectionManager class to manage active WebSocket connections.
* **Node-Level Broadcasting**: To make the agent actions visual, we created a Python decorator named `@broadcast_agent_node`.
* Every time a LangGraph node executes, the decorator broadcasts `agent_node_started` and `agent_node_completed` payloads containing the duration in milliseconds, node label, and status.
* The React dashboard receives these events over the `/ws/emergency` channel and updates the visual overlay in real-time.
\"\"\")

add("BloodBridge AI", "Why did you use a dual-database model (PostgreSQL + Neo4j)?", \"\"\"
Each database handles what it does best:
* **Supabase PostgreSQL**: Excellent for relational tables, transactions, strict schemas (like donor demographics, calendars, consent logs), and JWT authentication.
* **Neo4j Aura (Graph DB)**: Relational databases struggle with many-to-many relationships across multiple attributes. Matching 500 donors with 50 patients across 8 antigen attributes results in a 25,000 combination join operation. In Neo4j, we pre-calculate compatibility edges (`COMPATIBLE_WITH`) at onboarding. Finding the top 8 compatible donors within a geographic radius is simplified into a Cypher traversal that runs in under 100ms.
\"\"\")

add("BloodBridge AI", "How is database synchronization handled between PostgreSQL and Neo4j?", \"\"\"
To prevent data drift, we mirror primary keys (`donor_id`, `patient_id`) across both databases.
* When a donor registers, the profile is written to Supabase and a corresponding `(:Donor)` node is merged in Neo4j.
* We run a background task to compute the 8-antigen compatibility score against all active patients. For each match exceeding a score of 0.60, we create a `[:COMPATIBLE_WITH]` edge in Neo4j.
* During active emergencies, when a donor is selected, we create an `[:IN_CHAIN]` edge in Neo4j and a mirror record in the `blood_chains` table in Supabase. Supabase acts as the transactional ledger while Neo4j maintains the spatial-structural representation.
\"\"\")

add("BloodBridge AI", "How does the 14-Agent system manage state and recover from failures?", \"\"\"
We define a shared `AgentState` struct utilizing LangGraph's typing. State is passed sequentially through nodes:
* **Parallel Execution**: The AntigenScoringAgent and UrgencyScoringAgent run in parallel to minimize pipeline latency.
* **Conditional Routing**: The graph routes to the ConflictResolverAgent only if a rare donor is selected in the top-3 chains of two separate critical patients.
* **State Checkpointing**: The graph is compiled with a memory checkpointer. If the ChainMonitorAgent detects a donor node failure (time-out after 7 minutes or explicit decline), it updates the state and routes to the ChainRepairAgent which swaps in the next best donor and triggers outreach automatically.
\"\"\")

add("BloodBridge AI", "How does the hybrid Telegram webhook routing work?", \"\"\"
To prevent LLM hallucinations from corrupting the state of active coordination chains, we built a hybrid handler in the webhook route:
* **Deterministic Branch**: If a user is registered in the database as currently `ALERTED` in a blood chain and their text input is a simple confirmation keyword (yes, no, haan, kadu), we bypass the LLM entirely and run a deterministic state update.
* **Agentic Branch**: For conversational replies, questions, or profile registrations, the message is sent to a LangGraph ReAct agent that evaluates the text and calls registered tools (such as checking matching status or updating consent).
\"\"\")

add("BloodBridge AI", "Explain the clinical logic behind the 8-Antigen Matching Engine.", \"\"\"
Thalassemia Major patients receive blood transfusions for life. Over time, their immune systems develop allo-antibodies against minor blood antigens. If they receive blood with these antigens, they can suffer Delayed Hemolytic Transfusion Reactions. We implement an ISBT-weighted compatibility scorer:
* ABO mismatch = 0.0 score (immediate block).
* Kell mismatch = -0.35 penalty (highly immunogenic).
* Duffy mismatch = -0.25 penalty.
* Kidd mismatch = -0.20 penalty.
* The scorer checks the patient's existing `antibody_flags` and deducts penalties if the donor possesses corresponding antigens.
\"\"\")

add("BloodBridge AI", "Why did you choose Bolna.ai over standard Twilio Voice + gTTS?", \"\"\"
Bolna.ai provides an India-first voice infrastructure:
* **Native SIP Trunking**: Twilio requires purchase and validation of US numbers which can trigger spam filters on Indian mobile networks. Bolna integrates natively with Indian telecom providers for clean outbound caller ID.
* **Built-in Sarvam AI**: We get native Indian regional text-to-speech voices (Meera for Hindi, Padmaja for Telugu, Lakshmi for Tamil) with natural accents, bypassing the robotic tone of Google TTS.
* **Latency & NLU**: Speech-to-Text and intent mapping (YES/NO responses) are handled in-session with under 500ms latency.
\"\"\")

add("BloodBridge AI", "How did you implement DPDP Act 2023 compliance?", \"\"\"
India's DPDP Act 2023 mandates strict data protection, consent, and user access:
* **Consent Registry**: The `consent_records` table logs consent status. We store a cryptographic SHA256 hash of the exact consent text shown to the donor in their regional language to maintain a verifiable audit trail.
* **Right to Erasure (DPDP Sec 12)**: Triggered via the `/deletedata` Telegram command or API. We check if the donor is in any active emergency chain. If not, we run a cascade delete on their memory, gamification, and consent records. The donor profile is fully anonymized while retaining their donation count and blood type for historical statistics.
* **Audit Hash Log**: Client IP addresses are hashed using SHA256 before writing to server access logs to protect PII.
\"\"\")

add("BloodBridge AI", "How does the LoRa Offline Bridge function?", \"\"\"
To support remote tribal clinics lacking cellular data, we designed a custom 8-byte packet protocol:
* Byte 0: Blood type code.
* Bytes 1-3: First 3 bytes of MD5(patient_id) to verify identity.
* Byte 4: Urgency and phenotype flags.
* Byte 5: Region / City code.
* Bytes 6-7: CRC16/CCITT-FALSE checksum.
* The LoRa simulator serializes this packet and POSTs it to the `/api/lora/ingest` endpoint. The backend decodes it, resolves the patient from the hash, creates the emergency request, and kicks off the LangGraph matching workflow without requiring internet at the patient's location.
\"\"\")
"""

with open('data/db_projects.py', 'a', encoding='utf-8') as f:
    f.write(content)

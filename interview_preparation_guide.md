# 🎓 ExamReady & Vidvantu Ecosystem: Complete Interview Preparation Guide

This guide details the complete features of the **Vidvantu** educational project, the architecture and secondary services of the **FastAPI AI Core**, and includes 50 technical interview questions and answers.

---

## 👥 1. Team & Separation of Concerns

The project was built by a collaborative team of 4 members:
*   **Saniya (React Frontend)**: Developed the client-side user experience ([examready-frontend](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/examready-frontend)) including practice panels, student analytics history, and the teacher-facing review interface.
*   **Dinesh (Express Backend & Shared Database)**: Created the Node.js Express server ([examready-backend](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/examready-backend)) handling student authentication (JWTs), activity timelines, proxy endpoints, and mapped database tables via **Prisma ORM**.
*   **Uday (AI Tutor Service)**: Built the standalone AI tutoring microservice ([examreadyaitutor](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/examreadyaitutor)) on port 8001 for real-time streaming chapter instruction.
*   **You (FastAPI AI Core)**: Designed, engineered, and tested the high-performance **RAG & 4-Agent Exam Generation Engine** ([ExamReadyFastAPI](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI)) on port 8000.

---

## 💬 1.5. Resume Experience Section (Copy & Paste)

Here are the impact-driven bullet points for your **Ruvinsys Backend AI Engineer Internship** experience section in your resume:
*   Designed and implemented the core **asynchronous 4-agent generation pipeline** in FastAPI, orchestrating hybrid Qdrant search, Google Gemini model key rotation, and a SymPy-driven math verification engine to produce CBSE-compliant exams in under 10 seconds.
*   Built a custom framework-free RAG ingestion pipeline integrating PyMuPDF and Gemini Vision VLM OCR to convert textbooks containing complex formulas and diagrams into searchable vector embeddings.
*   Collaborated with a 4-person team to align schemas with a Node.js Express/Prisma database layer, implementing human-in-the-loop review queues, database auditing, and 400+ automated test suites.

---

## 🌐 2. Inter-Service Communication Architecture

```
 ┌───────────────────┐               REST API Calls               ┌──────────────────────┐
 │  React Frontend   │ ─────────────────────────────────────────► │  Express Backend     │
 │  (Saniya)         │ ◄───────────────────────────────────────── │  (Dinesh)            │
 └───────────────────┘             SSE Status Streaming           └──────────────────────┘
           ▲                                                                 │
           │                                                                 │ Proxy HTTP Calls
           │                                                                 │ X-Internal-Key
           │ Direct HTTP / SSE (Optional)                                    ▼
           └────────────────────────────────────────────────────── ┌──────────────────────┐
                                                                   │  FastAPI AI Core     │
                                                                   │  (You)               │
                                                                   └──────────────────────┘
                                                                             │
                                   ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
                                   ▼                                         ▼                                         ▼
                      ┌────────────────────────┐                ┌────────────────────────┐                ┌────────────────────────┐
                      │  PostgreSQL Database   │                │   Qdrant Cloud DB      │                │   Google Gemini API    │
                      │  (Shared SQLAlchemy)   │                │   (Vector Retrieval)   │                │   (LLM & Embeddings)   │
                      └────────────────────────┘                └────────────────────────┘                └────────────────────────┘
```

The services communicate using structured interfaces:
*   **Authentication & Security**: The React Frontend communicates with the Node.js Express server using JWTs. The Express server proxies requests to the FastAPI AI Core on port 8000 using HTTP requests. These requests include a shared `X-Internal-Key` header secret.
*   **Stateful Storage**: Both backends connect directly to the same **PostgreSQL** database. Express uses Prisma, while FastAPI uses SQLAlchemy Core with the async `databases` library. This allows FastAPI to read, write, and audit questions, reviews, and logs in the same tables accessed by the frontend.
*   **Asynchronous Progress Updates**: To prevent browser timeouts during generation, FastAPI uses `StreamingResponse` to stream Server-Sent Events (SSE) directly back to the client. This provides real-time updates as the orchestrator moves through each stage.

---

## 🤖 3. The 4-Agent Pipeline: Individual Component Breakdown

The pipeline runs inside [exam_orchestrator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/exam_orchestrator.py) and coordinates 4 decoupled agents:

```
                  [Exam Request]
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ 1. Blueprint Agent (Deterministic Planning)  │ ──► Creates 38/39 Empty Slots
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ 2. Retrieval Agent (Semantic & BM25 Search)  │ ──► Phase 1: Approved Question Bank
└──────────────────────────────────────────────┘     Phase 2: Raw NCERT/Exemplar Chunks
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ 3. Generation Agent (Structured LLM Drafting) │ ──► Gemini 2.0 API calls with context
└──────────────────────────────────────────────┘     Enforces diagram safety rules
                        │
                        ▼
┌──────────────────────────────────────────────┐
│ 4. Verification Agent (Automatic Validation) │ ──► SymPy Math Verification
└──────────────────────────────────────────────┘     LaTeX Sanitization & Quality Scoring
```

### A. Blueprint Agent ([blueprint_agent.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/blueprint_agent.py))
*   **Responsibility**: Decouples structural exam planning from question content.
*   **Mechanics**: Reads subject JSON configs to create 38 empty question slots (for Mathematics) or 39 slots (for Science). It sets parameters like section groups (A to E), question typologies (MCQ, VSA, SA, LA, Case-based), target marks, and locks chapter boundaries for Section E slots.

### B. Retrieval Agent ([retrieval_agent.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/retrieval_agent.py))
*   **Responsibility**: Queries vector stores to find existing questions, reducing LLM API consumption.
*   **Two-Phase Retrieval**:
    1.  *Phase 1*: Queries the **Approved Question Bank** (`cbse_class_10_maths_questionbank`) to fetch human-verified questions.
    2.  *Phase 2*: If the approved bank does not contain matching questions, it queries raw textbook and exam collections (`cbse_class_10_maths`).
*   **Variety Controls**: Restricts approved questions to a maximum of 70% per paper, applies a usage frequency penalty, and excludes items used in the last 7 days.

### C. Generation Agent ([generation_agent.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/generation_agent.py))
*   **Responsibility**: Generates new questions for slots that retrieval could not fill.
*   **Safety Guards**: Enforces diagram safety rules. It blocks LLM generation for geometry or diagram-heavy chapters, routing those slots back to verified question banks instead.
*   **Key Rotation**: Rotates through API keys to handle rate limits and retries failed calls up to 3 times.

### D. Verification Agent ([verification_agent.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/verification_agent.py))
*   **Responsibility**: Verifies question correctness.
*   **Validation Steps**:
    1.  *Mathematical Checks*: Verifies algebra through a SymPy-based evaluator.
    2.  *LaTeX Fixer*: Cleans up LaTeX syntax to ensure equations render properly on the frontend.
    3.  *Quality Scorer*: Rates readability, difficulty, and checks alignment with Bloom's Taxonomy.

---

## 🔍 4. The RAG Ingestion Pipeline: Component Breakdown

You built a custom, framework-free ingestion pipeline to parse NCERT materials and index them to Qdrant:

### A. Document Text Extractor ([ncert_content_extractor.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/ncert_content_extractor.py))
*   Uses `PyMuPDF` to read raw PDF streams, extracting raw text and positioning information page-by-page.

### B. Multimodal Diagram Router ([visionservice.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/visionservice.py) & [diagram_detector.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/diagram_detector.py))
*   Monitors layout bounding boxes. If a page contains complex diagrams or tables, it routes those coordinates to `pix2text` (to extract mathematical formulas) and Gemini Vision (to generate descriptions of diagrams).

### C. Semantic Section Chunker ([semantic_chunker.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/semantic_chunker.py))
*   Chunks documents along chapter divisions, heading titles, and exercise boundaries. This preserves context boundaries and prevents splitting math formulas in half.

### D. Sparse-Dense Vector Indexer ([sparse_vector_service.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/sparse_vector_service.py) & [qdrant_service.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/qdrant_service.py))
*   Generates 768-dimensional dense vector embeddings using `gemini-embedding-001`.
*   Computes BM25 sparse vectors for exact keyword matching.
*   Batch-upserts points to Qdrant Cloud using `PointStruct`.

---

## ⚙️ 5. Additional Backend Features (Excluding RAG & Agents)

*   **SymPy Math Verification Engine ([math_verifier.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/math_verifier.py))**: Converts math strings into SymPy expressions. Evaluates generated question keys to verify mathematical correctness before papers are built.
*   **Stateless Grading & AI Student Coach ([evaluation.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/routers/evaluation.py))**: Evaluates student open-ended answers against textbook guidelines using CBSE step-marking rubrics. Examines pre-computed student progress logs to generate study-priority tables and recommendations.
*   **Data Sanitization & LaTeX Cleanup ([latex_fixer.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/latex_fixer.py))**: Standardizes mixed math symbols (e.g., converting `\( \)` to `$`). Removes rendering headers (such as `\centering` or `\begin{table}`) to prevent layout breakage on the frontend.
*   **Audit Logging & Override Trackers ([override_audit.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/override_audit.py))**: Saves before/after JSON structures, reviewer metadata, and reasons when administrators override questions.
*   **Centralized Prompt Manager ([versioned_prompt_manager.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/versioned_prompt_manager.py))**: Manages prompts via a unified YAML configuration. It offers hot-reloading in development and measures prompt drift metrics.
*   **Quota & Budget Enforcement ([quota_enforcer.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/quota_enforcer.py))**: Monitors chapter distributions across exam files, enforcing budget rules to prevent question selection bias.
*   **Exam Exporter & HTML-to-PDF compiler ([pdfgenerator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/pdfgenerator.py))**: Compiles exam questions into print-ready PDF files using Jinja2 HTML templates and WeasyPrint.
*   **Observability & Performance Metrics ([metrics_service.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/metrics_service.py))**: Exposes Prometheus-compatible endpoints tracking latency profiles per agent slot and token counts.
*   **Cross-Paper Duplicate Checking ([cross_paper_checker.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/cross_paper_checker.py))**: Evaluates similarity between exam sheets to ensure there is zero question overlap across different versions.
*   **Character-Level Text Diff Utility ([diff_util.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/diff_util.py))**: Generates character-level inline differences, highlighting changes for teachers inside the approval board dashboard.

---

## 📈 6. Evolution & Optimization Journey

During development, the AI pipeline evolved through five phases based on performance metrics and failure modes:

```
┌───────────────────────────┐      High Latency (>60s)
│ Phase 1: Single Prompt    │ ──►  Math Hallucinations
│ Prototype                 │      No CBSE Layout Control
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐      Added SymPy Evaluator
│ Phase 2: Decoupled Slots  │ ──►  Reduced Hallucinations
│ & Math Checks             │      Hit API Rate Limits
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐      Lookup Approved Questions
│ Phase 3: Hybrid Qdrant    │ ──►  Reduced LLM Calls by 70%
│ Retrieval Layer           │      Slow Sequential Processing
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐      Parallel asyncio.gather()
│ Phase 4: Async Parallel   │ ──►  Reduced Latency to <10s
│ Execution                 │      Rate Limit issues remain
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐      Added Round-Robin Keys
│ Phase 5: Key Rotation     │ ──►  Stable Production Release
│ & Dynamic Routing         │      Multi-Subject Configs
└───────────────────────────┘
```

1.  **Phase 1: Single Prompt Prototype**: Originally, a single prompt generated the entire exam. This resulted in math inaccuracies (hallucinations), structural errors (wrong question counts, marks mismatch), and high latency (over 60 seconds).
2.  **Phase 2: Decoupled Slots & Math Verification**: Split the process into individual slot calls and added SymPy math checking. Hallucinations decreased, but API rate limits were quickly hit.
3.  **Phase 3: Hybrid Qdrant Retrieval Layer**: Added a retrieval layer to lookup existing human-verified questions, reducing LLM calls by 70%.
4.  **Phase 4: Async Parallel Orchestrator**: Concurrently triggered retrieval and generation for all 38 slots, decreasing generation times to under 10 seconds.
5.  **Phase 5: Key Rotation & Dynamic Subject Routing**: Added rotation config to survive rate limits, and sub-discipline filtering to support multiple subjects.

---

## 🧪 7. Testing Strategy for the RAG & Agent Pipeline

You built a testing framework in Python to validate the AI generation engine:
*   **Testing Architecture**: Uses `pytest` with `pytest-asyncio` to test async database sessions, API endpoints, and orchestrator pipelines.
*   **Mocking Integrations**: Uses `unittest.mock` to mock external API calls. This allows testing agent orchestration without triggering live Gemini or Qdrant billing charges.
*   **E2E Integration Testing ([test_full_exam_pipeline.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/tests/integration/test_full_exam_pipeline.py))**: Validates the entire workflow (from blueprinting through validation and PDF export) using mock data.
*   **Pre-Flight Verification Scripts ([validate_qdrant_data.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/scripts/validate_qdrant_data.py))**: Verifies Qdrant collection connections and collection schema counts before deployment.

---

## 🪙 8. Token Optimizations

We applied token reduction strategies to control API usage costs:
*   **Selective Context Pruning**: Restricts the retrieved context to the top $k$ relevant chunks (e.g. $k=3$), filtering chunks using indexed payload properties.
*   **Dynamic Truncation**: Normalizes whitespaces and strips redundant HTML formatting before sending text to the LLM.
*   **JSON Schema Constraints**: Restricts LLM responses to a minimal JSON schema, reducing output token overhead.

---

## ❓ 9. 50 Technical Interview Questions & Answers

### Core FastAPI & Architecture (1-10)

#### 1. How does FastAPI handle asynchronous requests, and why was it chosen for this project?
*   **Answer**: FastAPI is built on ASGI (Asynchronous Server Gateway Interface) and uses Starlette under the hood. It leverages Python's `async/await` syntax to run asynchronous I/O operations non-blockingly. In this project, creating a CBSE exam requires calling multiple LLM instances and vector stores. Running these requests concurrently via `asyncio.gather` prevents blocking, allowing the server to generate complex exams in under 10 seconds.

#### 2. Explain the purpose of `lifespan` handlers in `app/main.py`.
*   **Answer**: The `lifespan` handler manages resources during application startup and shutdown. It initializes the database connections, establishes connections to Qdrant Cloud, and loads the active subject config registries. When the application stops, it safely closes these open client connections, preventing database connection leaks.

#### 3. How is database concurrency handled in FastAPI without using Prisma?
*   **Answer**: In FastAPI, we use **SQLAlchemy Core** to construct schemas and table metadata, but execute the database operations using the asynchronous `databases` library. This library provides a clean wrapper around `asyncpg` (for PostgreSQL) to execute queries asynchronously, ensuring the database thread pool isn't blocked during heavy API loads.

#### 4. How does the API layer authorize requests from the Node.js Express server?
*   **Answer**: We implemented a token-based verification middleware inside [main.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/main.py). All incoming requests targeting non-public API endpoints must supply a valid `X-Internal-Key` header matching the shared application secret. If the key is missing or incorrect, it returns an HTTP 403 Forbidden response.

#### 5. How is subject-specific routing managed for Mathematics vs. Science?
*   **Answer**: We implemented the [SubjectConfigService](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/config/subject_config.py), which reads configuration maps from JSON files (e.g., `mathematics.json` and `science.json`). This registry dynamically determines the number of questions, target marks, chapter limits, Qdrant collection targets, and sub-discipline filters (like routing Science to Physics/Chemistry sub-chunks).

#### 6. What is the difference between `Pydantic` v1 and v2, and how did it affect data validation in your codebase?
*   **Answer**: Pydantic v2 is written in Rust, making it up to 5-10 times faster than v1. It provides stricter data validation and updated serialization APIs (e.g., `model_validate`). We leverage Pydantic v2 to validate incoming generation requests and output schemas, ensuring payload structural integrity before triggering LLM calls.

#### 7. How did you implement real-time generation status streaming?
*   **Answer**: We utilized FastAPI's `StreamingResponse` returning a server-sent events (SSE) stream. As the orchestrator transitions through each step (Blueprint creation, Retrieval, Generation, and Verification), it yields a structured JSON event payload, allowing the React frontend to display live step-by-step progress to the user.

#### 8. Explain how CORS middleware is configured in the FastAPI backend.
*   **Answer**: We imported and initialized `CORSMiddleware` in [main.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/main.py), explicitly whitelisting the local frontend development ports (`3000`, `5173`) and production domains (`examready.app`). We allowed standard methods (`GET`, `POST`, `OPTIONS`) and enabled `allow_credentials=True` to support credentialed cookies and tokens.

#### 9. How do you manage API rate-limiting directly inside the FastAPI backend?
*   **Answer**: We created a custom `RateLimitMiddleware` using an in-memory sliding window or Redis counter. It extracts the client's IP address or authorization token and checks it against a configured rate limit (e.g., 60 requests per minute). If a client exceeds this limit, the middleware returns an HTTP 429 Too Many Requests response.

#### 10. How do you run background tasks in FastAPI, and when did you use them?
*   **Answer**: FastAPI provides a `BackgroundTasks` parameter that runs callables after returning a response. We used background tasks to generate exam PDFs via WeasyPrint and sync approved questions back to the Qdrant vector database, keeping the primary HTTP response fast.

---

### 4-Agent Pipeline & Orchestration (11-20)

#### 11. How did you implement and orchestrate the asynchronous 4-agent generation pipeline without LangChain or LangGraph? How do you defend this framework-free architecture?
*   **Answer**: 
    - **Implementation**: I designed a native asynchronous state machine using pure Python `asyncio`. The orchestration loop runs in [exam_orchestrator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/exam_orchestrator.py) and coordinates 4 distinct classes: `BlueprintAgent`, `RetrievalAgent`, `GenerationAgent`, and `VerificationAgent`. I used `asyncio.gather()` to concurrently trigger vector database and LLM requests per blueprint slot, keeping the total paper generation time under 10 seconds.
    - **Interview Defense**:
        1. *Zero Abstraction Overhead*: Frameworks like LangChain or LangGraph introduce massive class hierarchies that serialize and structure payloads behind the scenes, adding latency. Writing a raw async loop allowed us to achieve sub-10 second latency targets.
        2. *Absolute State Determinism*: CBSE exam papers require strict, non-negotiable structural constraint locks (such as locking Math Section E to specific chapters). Native state machines prevent state-transition drift that often occurs in LLM-driven graph agents.
        3. *Granular Verification Loops*: I could insert validation checkups (such as SymPy math equations and LaTeX sanitizers) directly into the agent retry loop without fighting against complex framework pipelines.

#### 12. Walk through the step-by-step execution flow of the 4-Agent Pipeline.
*   **Answer**: First, the **Blueprint Agent** initializes a list of 38 empty question slots. Second, the **Retrieval Agent** attempts to fill these slots by performing hybrid vector searches. Third, the **Generation Agent** calls the LLM to write fresh questions for any unfilled slots. Finally, the **Verification Agent** checks mathematical statements, sanitizes LaTeX equations, and calculates a final Quality Score.

#### 13. What is the Section E Chapter Lock constraint, and how is it implemented?
*   **Answer**: In CBSE Class 10 Mathematics, Section E consists of 3 case-based questions worth 4 marks each. The blueprint specifies that these questions must belong to *Arithmetic Progressions*, *Coordinate Geometry*, and *Applications of Trigonometry*. The Blueprint Agent enforces this by hardcoding these chapter associations for slots 36, 37, and 38, preventing other chapters from occupying them.

#### 14. How do you handle parallel processing of the 38 question slots?
*   **Answer**: We group the blueprint slots and process them in parallel using `asyncio.gather`. For the retrieval phase, the slots query Qdrant concurrently. The generation phase also triggers parallel asynchronous requests to the Gemini API, bringing the total generation time down to under 10 seconds.

#### 15. What are the constraints evaluated during the Assembly Validation step?
*   **Answer**: The [assembly_validator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/assembly_validator.py) checks that:
1. The exam contains the exact number of expected questions (e.g., 38 for Math, 39 for Science).
2. The total marks sum to exactly 80.
3. Every question contains the required properties (such as text, choices, correct answer, and explanation).
4. No duplicate questions exist (verified by comparing SHA-256 hashes).

#### 16. How does the system handle a failure where the generated exam fails structural validation?
*   **Answer**: If validation checks fail, the orchestrator logs the violations as metrics and falls back to replacing the invalid questions with verified items from the human-approved database bank, ensuring the API always returns a valid, structurally correct exam.

#### 17. What is the dynamic "Quality Score" calculated in the pipeline?
*   **Answer**: The `QualityScorer` rates each question from `0.0` to `1.0`. It scores questions based on readability length, LaTeX layout correctness, difficulty labels, and whether the cognitive classification matches Bloom's Taxonomy goals. Any question scoring below a threshold (like `0.65`) is rejected.

#### 18. How do you implement retry limits inside the Generation Agent?
*   **Answer**: When Gemini produces a question that fails LaTeX sanitization or math validation, the Generation Agent catches the exception and retries the request up to 3 times. We pass the validation error message back into the prompt context on retries, helping the LLM correct its output. If it still fails, the agent falls back to the human-approved question bank.

#### 19. How did you implement the "Advisory Board Review" flow in your orchestrator?
*   **Answer**: The orchestrator writes generated exams to the PostgreSQL database with a status of `PENDING`. This populates a review queue. Administrators or advisory members can accept, reject, or edit questions via the API. Once approved, the system updates the question's status to `APPROVED` and syncs it to the approved Qdrant question bank collection.

#### 20. What is "Variation Lineage", and why do you validate it?
*   **Answer**: To prevent questions from becoming repetitive, we track parent-child relationships for generated variations. If a question is generated as a variation of a base question, it receives a reference parent ID. The orchestrator checks this lineage metadata, blocking the generation of variations of variations to prevent quality degradation.

---

### RAG & Vector Database (Qdrant) (21-30)

#### 21. Describe the difference between dense and sparse vectors and how they are used together.
*   **Answer**: Dense vectors represent semantic meaning (using `gemini-embedding-001` at 768 dimensions), which helps match concepts (like matching "linear functions" to "straight lines"). Sparse vectors (representing word frequency, like BM25) match exact keywords (like finding "NCERT Exercise 3.2"). We combine their search scores to perform hybrid searches.

#### 22. How are the two vector databases partitioned for Mathematics and Science?
*   **Answer**: We use four collections in Qdrant:
1. `cbse_class_10_maths` (Textbook and exemplar raw data).
2. `cbse_class_10_science` (Science raw data).
3. `cbse_class_10_maths_questionbank` (Approved math questions).
4. `cbse_class_10_science_questionbank` (Approved science questions).
The [SubjectConfigService](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/config/subject_config.py) resolves these collections dynamically at query time.

#### 23. What payload filters are configured in Qdrant, and how do they speed up retrieval?
*   **Answer**: We index key payload fields in Qdrant: `chapter`, `difficulty`, `question_type`, and `bloom_level`. When querying, we pass a Qdrant `Filter` matching these keys. Indexing these fields allows Qdrant to skip scanning unrelated points, returning matches in under 50ms.

#### 24. How did you build the custom RAG ingestion and retrieval pipeline without LangChain or LlamaIndex? What tools were used instead?
*   **Answer**:
    - **Instead of LangChain Loaders**: I wrote a native python parser using **`PyMuPDF` (fitz)** to extract clean raw text streams page-by-page from NCERT textbook and exam PDFs, bypassing the slow, generic document loaders found in standard frameworks.
    - **Instead of Recursive Text Splitters**: I implemented a custom **`SemanticChunker` / heading-based parser** that splits texts at NCERT section headings and markdown dividers. This preserves semantic boundaries, keeping context clean and avoiding splitting mathematical equations in half.
    - **Instead of Framework Vector Wrappers**: I implemented direct asynchronous calls to the **`qdrant-client` SDK** to construct collection schemas, define HNSW indexes, build sparse-dense search configurations, and handle batch upserts using `PointStruct`.
    - **Instead of Framework LLM wrappers**: I integrated the raw **`google-generativeai` SDK** directly to generate 768-dimensional embeddings via `gemini-embedding-001` and call model chat completions, enabling key-rotation logic and custom retries.

#### 25. How do you handle diagrams and visual questions in the ingestion pipeline?
*   **Answer**: When the ingestion parser detects a diagram or image area, it calls a Gemini Vision VLM prompt. The VLM acts as an OCR engine, converting diagram layouts, coordinate systems, and text labels into descriptive markdown text. This text is embedded alongside the main text chunk, allowing visual content to be searched.

#### 26. How do you prevent duplicate chunks during vector ingestion?
*   **Answer**: We generate an MD5 hash of the raw text contents of each chunk before indexing. We use this hash as the Qdrant point's UUID. If we ingest the same textbook chapter again, Qdrant's upsert operation replaces the existing point rather than creating a duplicate, ensuring idempotency.

#### 27. What is the "reuse penalty factor" in the Retrieval Agent?
*   **Answer**: To prevent the generator from using the same questions in multiple papers, we check the question's `usage_count` in PostgreSQL. For every reuse, we reduce its search similarity score by 10%. This penalty pushes frequently used questions down the retrieval results, ensuring variety in generated papers.

#### 28. How is the cosine distance threshold managed in the Retrieval Agent?
*   **Answer**: We set a minimum similarity threshold of `0.65` for retrieved items. If the top search result falls below this score, the agent marks retrieval as low-confidence and routes the slot to the Generation Agent to create a new question instead.

#### 29. Explain how you normalize Qdrant similarity scores.
*   **Answer**: Vector similarity scores can vary depending on the query length. We normalize scores using a Sigmoid function:
$$\text{Normalized Score} = \frac{1}{1 + e^{-k(x - x_0)}}$$
This function maps raw similarity scores to a 0-1 range, making it easier to evaluate confidence thresholds.

#### 30. How do you sync approved question drafts back into Qdrant?
*   **Answer**: When an administrator approves a question in the review queue, a background task generates its vector embedding using Gemini and upserts the question text and metadata into the approved question bank collection (e.g., `cbse_class_10_maths_questionbank`).

---

### LLMs & Prompts (31-40)

#### 31. How is model key rotation configured for Google Gemini API?
*   **Answer**: We define a list of Gemini API keys in the `.env` configuration file. The [geminiservice.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/geminiservice.py) rotates through these keys in a round-robin fashion. If a key hits a rate limit or returns a quota error, the service switches to the next key, minimizing API downtime.

#### 32. What is "Diagram Safety", and how is it enforced?
*   **Answer**: LLMs can struggle to generate accurate questions for visual geometry chapters (like *Triangles* or *Circles*). To prevent errors, we define a list of these chapters in `DIAGRAM_CHAPTERS`. The Generation Agent is blocked from generating questions for these chapters; instead, it must retrieve them from the verified question bank.

#### 33. How do you prevent LLM hallucinations in questions?
*   **Answer**: We use retrieval-augmented generation. When generating a question, we inject relevant NCERT textbook chunks into the LLM system prompt. We also instruct the LLM to return the exact source context and run automated algebraic checks on the output.

#### 34. Explain the prompt template structure in `config/prompts.yaml`.
*   **Answer**: The configuration groups prompts by operation: `generation` (for creating questions), `blooms_tagger` (for classifying questions), and `validation` (for verifying math). Each entry defines a `system` instruction detailing the model's persona and rules, and a `user` template containing placeholders for runtime variables.

#### 35. What is "Hot Reloading" for prompts, and how did you implement it?
*   **Answer**: In development mode, we use a file watcher service that monitors `config/prompts.yaml`. When a prompt is updated, the service reloads the YAML file without restarting the Uvicorn server, speeding up prompt testing.

#### 36. How do you check for concept drift in LLM-generated questions?
*   **Answer**: We pass the generated question and its target chapter to a validation model. The model evaluates whether the question's core concepts align with the NCERT curriculum boundaries. If it detects off-topic concepts, it rejects the question.

#### 37. How do you generate case-study questions (Section E) using Gemini?
*   **Answer**: Section E questions require a background passage followed by three sub-questions (worth 1, 1, and 2 marks). We use a specialized system prompt that instructs Gemini to return a unified JSON payload containing a `passage` string and a `sub_questions` array, verifying that the sub-questions' marks sum to exactly 4.

#### 38. What is the fallback strategy if the Gemini API goes down?
*   **Answer**: If all Gemini API keys fail, the orchestrator catches the exception, logs a warning, and switches to the local question bank JSON file (`human_bank.json`), fetching a matching verified question to fill the slot.

#### 39. How do you prompt the model to classify questions by Bloom's Taxonomy?
*   **Answer**: We pass the question text to a classifier prompt that defines the six levels of Bloom's Taxonomy (*Remembering*, *Understanding*, *Applying*, *Analyzing*, *Evaluating*, *Creating*). The model returns the matching category along with a short explanation of its classification.

#### 40. Why do you use structured JSON responses over plain text for LLM outputs?
*   **Answer**: Plain text outputs are difficult to parse programmatically. By requesting structured JSON payloads matching Pydantic schemas, we can directly validate fields like options, answers, and explanations, raising validation errors if any fields are missing.

---

### Math Verifications & LaTeX (41-45)

#### 41. Walk through the math verification process using SymPy.
*   **Answer**: In [math_verifier.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/math_verifier.py), we extract math expressions from the question. We use SymPy to parse equations and calculate the correct solution. We then compare this calculated solution against the option keys provided in the question. If the answers do not match, the question is flagged as mathematically incorrect.

#### 42. How does the SymPy verifier handle algebra and symbol declarations?
*   **Answer**: We parse standard math variables (like `x`, `y`, `z`, `theta`) into SymPy symbols. We use `sympy.sympify` or `sympy.parsing.latex.parse_latex` to convert equations into algebraic expressions, evaluating if they simplify to equality (e.g., confirming $x^2 - 4 = 0$ resolves to $x = \pm 2$).

#### 43. What LaTeX formatting issues did you encounter, and how did you resolve them?
*   **Answer**: We often encountered problems with double-slashes (`\\`), unescaped percentage signs (`%`), and mismatched dollar signs (`$`). We wrote a regex-based helper in [latex_fixer.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/latex_fixer.py) to clean math tags, balance brackets, and replace legacy characters, ensuring equations render correctly in MathJax/KaTeX.

#### 44. How does the verification agent identify "proof-based" questions?
*   **Answer**: We use regex search patterns (looking for words like "Prove that", "Show that", "Derive"). When a question matches these terms, we set the `is_proof` flag to `True`. This bypasses numerical option validation checks, routing the question through text-based explanation verification instead.

#### 45. How do you prevent infinite loops during math validation retries?
*   **Answer**: We enforce a maximum retry count of 3. If a question fails math verification, the agent retries the generation. If it fails a third time, the orchestrator terminates the loop and falls back to a verified question from the database.

---

### Student Evaluation & Analytics (46-50)

#### 46. What is the role of the stateless evaluation router `evaluation.py`?
*   **Answer**: The [evaluation.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/routers/evaluation.py) router defines endpoints for scoring subjective answers and rendering student performance coaching summaries. It is designed to be completely stateless—meaning it receives pre-computed session stats from the Express backend and handles LLM evaluation workloads without direct database reads.

#### 47. How are subjective answers graded dynamically inside your service?
*   **Answer**: Subjective answers are routed to `AnswerEvaluator.evaluate_subjective_answers`. The service compiles a prompt detailing the CBSE step-marking guidelines, the textbook answer scheme, and the student's submission. Gemini processes the prompt and returns a JSON array detailing marks awarded, correctness flags, and step-by-step coaching feedback.

#### 48. How do you prevent performance analysis timeouts when evaluating large exam papers?
*   **Answer**: To keep response times low, the subjective evaluation endpoint enforces a limit of 25 questions per request. Larger papers must be split into batches and sent as concurrent async queries to prevent timeouts.

#### 49. How does the `/v1/evaluate/performance` endpoint generate study priorities?
*   **Answer**: It parses the `PerformanceStats` payload (containing topic accuracies, weakness arrays, and score trends) sent by Dinesh's Express server. The evaluator feeds these stats into Gemini to output structured study priority tables, classifying chapters into HIGH/MEDIUM/LOW priority alongside supporting reasoning.

#### 50. How are database migrations executed concurrently with Express?
*   **Answer**: Dinesh handles migrations using Prisma schemas. To prevent database locks, you run raw validation scripts (like `validate_migration.py`) that verify PostgreSQL tables and column alignments before starting up the FastAPI server.

---
*Created for your Ruvinsys Backend AI interview preparation. Good luck!*

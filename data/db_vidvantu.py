# db_vidvantu.py - Vidvantu Project Specific Questions

VIDVANTU_QUESTIONS = [
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does FastAPI handle asynchronous requests, and why was it chosen for this project?",
    "answer": "*   **Answer**: FastAPI is built on ASGI (Asynchronous Server Gateway Interface) and uses Starlette under the hood. It leverages Python's `async/await` syntax to run asynchronous I/O operations non-blockingly. In this project, creating a CBSE exam requires calling multiple LLM instances and vector stores. Running these requests concurrently via `asyncio.gather` prevents blocking, allowing the server to generate complex exams in under 10 seconds.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Explain the purpose of `lifespan` handlers in `app/main.py`.",
    "answer": "*   **Answer**: The `lifespan` handler manages resources during application startup and shutdown. It initializes the database connections, establishes connections to Qdrant Cloud, and loads the active subject config registries. When the application stops, it safely closes these open client connections, preventing database connection leaks.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How is database concurrency handled in FastAPI without using Prisma?",
    "answer": "*   **Answer**: In FastAPI, we use **SQLAlchemy Core** to construct schemas and table metadata, but execute the database operations using the asynchronous `databases` library. This library provides a clean wrapper around `asyncpg` (for PostgreSQL) to execute queries asynchronously, ensuring the database thread pool isn't blocked during heavy API loads.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does the API layer authorize requests from the Node.js Express server?",
    "answer": "*   **Answer**: We implemented a token-based verification middleware inside [main.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/main.py). All incoming requests targeting non-public API endpoints must supply a valid `X-Internal-Key` header matching the shared application secret. If the key is missing or incorrect, it returns an HTTP 403 Forbidden response.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How is subject-specific routing managed for Mathematics vs. Science?",
    "answer": "*   **Answer**: We implemented the [SubjectConfigService](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/config/subject_config.py), which reads configuration maps from JSON files (e.g., `mathematics.json` and `science.json`). This registry dynamically determines the number of questions, target marks, chapter limits, Qdrant collection targets, and sub-discipline filters (like routing Science to Physics/Chemistry sub-chunks).",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the difference between `Pydantic` v1 and v2, and how did it affect data validation in your codebase?",
    "answer": "*   **Answer**: Pydantic v2 is written in Rust, making it up to 5-10 times faster than v1. It provides stricter data validation and updated serialization APIs (e.g., `model_validate`). We leverage Pydantic v2 to validate incoming generation requests and output schemas, ensuring payload structural integrity before triggering LLM calls.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How did you implement real-time generation status streaming?",
    "answer": "*   **Answer**: We utilized FastAPI's `StreamingResponse` returning a server-sent events (SSE) stream. As the orchestrator transitions through each step (Blueprint creation, Retrieval, Generation, and Verification), it yields a structured JSON event payload, allowing the React frontend to display live step-by-step progress to the user.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Explain how CORS middleware is configured in the FastAPI backend.",
    "answer": "*   **Answer**: We imported and initialized `CORSMiddleware` in [main.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/main.py), explicitly whitelisting the local frontend development ports (`3000`, `5173`) and production domains (`examready.app`). We allowed standard methods (`GET`, `POST`, `OPTIONS`) and enabled `allow_credentials=True` to support credentialed cookies and tokens.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you manage API rate-limiting directly inside the FastAPI backend?",
    "answer": "*   **Answer**: We created a custom `RateLimitMiddleware` using an in-memory sliding window or Redis counter. It extracts the client's IP address or authorization token and checks it against a configured rate limit (e.g., 60 requests per minute). If a client exceeds this limit, the middleware returns an HTTP 429 Too Many Requests response.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you run background tasks in FastAPI, and when did you use them?",
    "answer": "*   **Answer**: FastAPI provides a `BackgroundTasks` parameter that runs callables after returning a response. We used background tasks to generate exam PDFs via WeasyPrint and sync approved questions back to the Qdrant vector database, keeping the primary HTTP response fast.\n\n---",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How did you implement and orchestrate the asynchronous 4-agent generation pipeline without LangChain or LangGraph? How do you defend this framework-free architecture?",
    "answer": "*   **Answer**: \n    - **Implementation**: I designed a native asynchronous state machine using pure Python `asyncio`. The orchestration loop runs in [exam_orchestrator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/agents/exam_orchestrator.py) and coordinates 4 distinct classes: `BlueprintAgent`, `RetrievalAgent`, `GenerationAgent`, and `VerificationAgent`. I used `asyncio.gather()` to concurrently trigger vector database and LLM requests per blueprint slot, keeping the total paper generation time under 10 seconds.\n    - **Interview Defense**:\n        1. *Zero Abstraction Overhead*: Frameworks like LangChain or LangGraph introduce massive class hierarchies that serialize and structure payloads behind the scenes, adding latency. Writing a raw async loop allowed us to achieve sub-10 second latency targets.\n        2. *Absolute State Determinism*: CBSE exam papers require strict, non-negotiable structural constraint locks (such as locking Math Section E to specific chapters). Native state machines prevent state-transition drift that often occurs in LLM-driven graph agents.\n        3. *Granular Verification Loops*: I could insert validation checkups (such as SymPy math equations and LaTeX sanitizers) directly into the agent retry loop without fighting against complex framework pipelines.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Walk through the step-by-step execution flow of the 4-Agent Pipeline.",
    "answer": "*   **Answer**: First, the **Blueprint Agent** initializes a list of 38 empty question slots. Second, the **Retrieval Agent** attempts to fill these slots by performing hybrid vector searches. Third, the **Generation Agent** calls the LLM to write fresh questions for any unfilled slots. Finally, the **Verification Agent** checks mathematical statements, sanitizes LaTeX equations, and calculates a final Quality Score.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the Section E Chapter Lock constraint, and how is it implemented?",
    "answer": "*   **Answer**: In CBSE Class 10 Mathematics, Section E consists of 3 case-based questions worth 4 marks each. The blueprint specifies that these questions must belong to *Arithmetic Progressions*, *Coordinate Geometry*, and *Applications of Trigonometry*. The Blueprint Agent enforces this by hardcoding these chapter associations for slots 36, 37, and 38, preventing other chapters from occupying them.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you handle parallel processing of the 38 question slots?",
    "answer": "*   **Answer**: We group the blueprint slots and process them in parallel using `asyncio.gather`. For the retrieval phase, the slots query Qdrant concurrently. The generation phase also triggers parallel asynchronous requests to the Gemini API, bringing the total generation time down to under 10 seconds.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What are the constraints evaluated during the Assembly Validation step?",
    "answer": "*   **Answer**: The [assembly_validator.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/assembly_validator.py) checks that:\n1. The exam contains the exact number of expected questions (e.g., 38 for Math, 39 for Science).\n2. The total marks sum to exactly 80.\n3. Every question contains the required properties (such as text, choices, correct answer, and explanation).\n4. No duplicate questions exist (verified by comparing SHA-256 hashes).",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does the system handle a failure where the generated exam fails structural validation?",
    "answer": "*   **Answer**: If validation checks fail, the orchestrator logs the violations as metrics and falls back to replacing the invalid questions with verified items from the human-approved database bank, ensuring the API always returns a valid, structurally correct exam.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the dynamic \"Quality Score\" calculated in the pipeline?",
    "answer": "*   **Answer**: The `QualityScorer` rates each question from `0.0` to `1.0`. It scores questions based on readability length, LaTeX layout correctness, difficulty labels, and whether the cognitive classification matches Bloom's Taxonomy goals. Any question scoring below a threshold (like `0.65`) is rejected.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you implement retry limits inside the Generation Agent?",
    "answer": "*   **Answer**: When Gemini produces a question that fails LaTeX sanitization or math validation, the Generation Agent catches the exception and retries the request up to 3 times. We pass the validation error message back into the prompt context on retries, helping the LLM correct its output. If it still fails, the agent falls back to the human-approved question bank.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How did you implement the \"Advisory Board Review\" flow in your orchestrator?",
    "answer": "*   **Answer**: The orchestrator writes generated exams to the PostgreSQL database with a status of `PENDING`. This populates a review queue. Administrators or advisory members can accept, reject, or edit questions via the API. Once approved, the system updates the question's status to `APPROVED` and syncs it to the approved Qdrant question bank collection.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is \"Variation Lineage\", and why do you validate it?",
    "answer": "*   **Answer**: To prevent questions from becoming repetitive, we track parent-child relationships for generated variations. If a question is generated as a variation of a base question, it receives a reference parent ID. The orchestrator checks this lineage metadata, blocking the generation of variations of variations to prevent quality degradation.\n\n---",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Describe the difference between dense and sparse vectors and how they are used together.",
    "answer": "*   **Answer**: Dense vectors represent semantic meaning (using `gemini-embedding-001` at 768 dimensions), which helps match concepts (like matching \"linear functions\" to \"straight lines\"). Sparse vectors (representing word frequency, like BM25) match exact keywords (like finding \"NCERT Exercise 3.2\"). We combine their search scores to perform hybrid searches.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How are the two vector databases partitioned for Mathematics and Science?",
    "answer": "*   **Answer**: We use four collections in Qdrant:\n1. `cbse_class_10_maths` (Textbook and exemplar raw data).\n2. `cbse_class_10_science` (Science raw data).\n3. `cbse_class_10_maths_questionbank` (Approved math questions).\n4. `cbse_class_10_science_questionbank` (Approved science questions).\nThe [SubjectConfigService](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/config/subject_config.py) resolves these collections dynamically at query time.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What payload filters are configured in Qdrant, and how do they speed up retrieval?",
    "answer": "*   **Answer**: We index key payload fields in Qdrant: `chapter`, `difficulty`, `question_type`, and `bloom_level`. When querying, we pass a Qdrant `Filter` matching these keys. Indexing these fields allows Qdrant to skip scanning unrelated points, returning matches in under 50ms.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How did you build the custom RAG ingestion and retrieval pipeline without LangChain or LlamaIndex? What tools were used instead?",
    "answer": "*   **Answer**:\n    - **Instead of LangChain Loaders**: I wrote a native python parser using **`PyMuPDF` (fitz)** to extract clean raw text streams page-by-page from NCERT textbook and exam PDFs, bypassing the slow, generic document loaders found in standard frameworks.\n    - **Instead of Recursive Text Splitters**: I implemented a custom **`SemanticChunker` / heading-based parser** that splits texts at NCERT section headings and markdown dividers. This preserves semantic boundaries, keeping context clean and avoiding splitting mathematical equations in half.\n    - **Instead of Framework Vector Wrappers**: I implemented direct asynchronous calls to the **`qdrant-client` SDK** to construct collection schemas, define HNSW indexes, build sparse-dense search configurations, and handle batch upserts using `PointStruct`.\n    - **Instead of Framework LLM wrappers**: I integrated the raw **`google-generativeai` SDK** directly to generate 768-dimensional embeddings via `gemini-embedding-001` and call model chat completions, enabling key-rotation logic and custom retries.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you handle diagrams and visual questions in the ingestion pipeline?",
    "answer": "*   **Answer**: When the ingestion parser detects a diagram or image area, it calls a Gemini Vision VLM prompt. The VLM acts as an OCR engine, converting diagram layouts, coordinate systems, and text labels into descriptive markdown text. This text is embedded alongside the main text chunk, allowing visual content to be searched.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you prevent duplicate chunks during vector ingestion?",
    "answer": "*   **Answer**: We generate an MD5 hash of the raw text contents of each chunk before indexing. We use this hash as the Qdrant point's UUID. If we ingest the same textbook chapter again, Qdrant's upsert operation replaces the existing point rather than creating a duplicate, ensuring idempotency.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the \"reuse penalty factor\" in the Retrieval Agent?",
    "answer": "*   **Answer**: To prevent the generator from using the same questions in multiple papers, we check the question's `usage_count` in PostgreSQL. For every reuse, we reduce its search similarity score by 10%. This penalty pushes frequently used questions down the retrieval results, ensuring variety in generated papers.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How is the cosine distance threshold managed in the Retrieval Agent?",
    "answer": "*   **Answer**: We set a minimum similarity threshold of `0.65` for retrieved items. If the top search result falls below this score, the agent marks retrieval as low-confidence and routes the slot to the Generation Agent to create a new question instead.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Explain how you normalize Qdrant similarity scores.",
    "answer": "*   **Answer**: Vector similarity scores can vary depending on the query length. We normalize scores using a Sigmoid function:\n$$\\text{Normalized Score} = \\frac{1}{1 + e^{-k(x - x_0)}}$$\nThis function maps raw similarity scores to a 0-1 range, making it easier to evaluate confidence thresholds.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you sync approved question drafts back into Qdrant?",
    "answer": "*   **Answer**: When an administrator approves a question in the review queue, a background task generates its vector embedding using Gemini and upserts the question text and metadata into the approved question bank collection (e.g., `cbse_class_10_maths_questionbank`).\n\n---",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How is model key rotation configured for Google Gemini API?",
    "answer": "*   **Answer**: We define a list of Gemini API keys in the `.env` configuration file. The [geminiservice.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/geminiservice.py) rotates through these keys in a round-robin fashion. If a key hits a rate limit or returns a quota error, the service switches to the next key, minimizing API downtime.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is \"Diagram Safety\", and how is it enforced?",
    "answer": "*   **Answer**: LLMs can struggle to generate accurate questions for visual geometry chapters (like *Triangles* or *Circles*). To prevent errors, we define a list of these chapters in `DIAGRAM_CHAPTERS`. The Generation Agent is blocked from generating questions for these chapters; instead, it must retrieve them from the verified question bank.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you prevent LLM hallucinations in questions?",
    "answer": "*   **Answer**: We use retrieval-augmented generation. When generating a question, we inject relevant NCERT textbook chunks into the LLM system prompt. We also instruct the LLM to return the exact source context and run automated algebraic checks on the output.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Explain the prompt template structure in `config/prompts.yaml`.",
    "answer": "*   **Answer**: The configuration groups prompts by operation: `generation` (for creating questions), `blooms_tagger` (for classifying questions), and `validation` (for verifying math). Each entry defines a `system` instruction detailing the model's persona and rules, and a `user` template containing placeholders for runtime variables.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is \"Hot Reloading\" for prompts, and how did you implement it?",
    "answer": "*   **Answer**: In development mode, we use a file watcher service that monitors `config/prompts.yaml`. When a prompt is updated, the service reloads the YAML file without restarting the Uvicorn server, speeding up prompt testing.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you check for concept drift in LLM-generated questions?",
    "answer": "*   **Answer**: We pass the generated question and its target chapter to a validation model. The model evaluates whether the question's core concepts align with the NCERT curriculum boundaries. If it detects off-topic concepts, it rejects the question.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you generate case-study questions (Section E) using Gemini?",
    "answer": "*   **Answer**: Section E questions require a background passage followed by three sub-questions (worth 1, 1, and 2 marks). We use a specialized system prompt that instructs Gemini to return a unified JSON payload containing a `passage` string and a `sub_questions` array, verifying that the sub-questions' marks sum to exactly 4.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the fallback strategy if the Gemini API goes down?",
    "answer": "*   **Answer**: If all Gemini API keys fail, the orchestrator catches the exception, logs a warning, and switches to the local question bank JSON file (`human_bank.json`), fetching a matching verified question to fill the slot.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you prompt the model to classify questions by Bloom's Taxonomy?",
    "answer": "*   **Answer**: We pass the question text to a classifier prompt that defines the six levels of Bloom's Taxonomy (*Remembering*, *Understanding*, *Applying*, *Analyzing*, *Evaluating*, *Creating*). The model returns the matching category along with a short explanation of its classification.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Why do you use structured JSON responses over plain text for LLM outputs?",
    "answer": "*   **Answer**: Plain text outputs are difficult to parse programmatically. By requesting structured JSON payloads matching Pydantic schemas, we can directly validate fields like options, answers, and explanations, raising validation errors if any fields are missing.\n\n---",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "Walk through the math verification process using SymPy.",
    "answer": "*   **Answer**: In [math_verifier.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/math_verifier.py), we extract math expressions from the question. We use SymPy to parse equations and calculate the correct solution. We then compare this calculated solution against the option keys provided in the question. If the answers do not match, the question is flagged as mathematically incorrect.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does the SymPy verifier handle algebra and symbol declarations?",
    "answer": "*   **Answer**: We parse standard math variables (like `x`, `y`, `z`, `theta`) into SymPy symbols. We use `sympy.sympify` or `sympy.parsing.latex.parse_latex` to convert equations into algebraic expressions, evaluating if they simplify to equality (e.g., confirming $x^2 - 4 = 0$ resolves to $x = \\pm 2$).",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What LaTeX formatting issues did you encounter, and how did you resolve them?",
    "answer": "*   **Answer**: We often encountered problems with double-slashes (`\\\\`), unescaped percentage signs (`%`), and mismatched dollar signs (`$`). We wrote a regex-based helper in [latex_fixer.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/services/latex_fixer.py) to clean math tags, balance brackets, and replace legacy characters, ensuring equations render correctly in MathJax/KaTeX.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does the verification agent identify \"proof-based\" questions?",
    "answer": "*   **Answer**: We use regex search patterns (looking for words like \"Prove that\", \"Show that\", \"Derive\"). When a question matches these terms, we set the `is_proof` flag to `True`. This bypasses numerical option validation checks, routing the question through text-based explanation verification instead.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you prevent infinite loops during math validation retries?",
    "answer": "*   **Answer**: We enforce a maximum retry count of 3. If a question fails math verification, the agent retries the generation. If it fails a third time, the orchestrator terminates the loop and falls back to a verified question from the database.\n\n---",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "What is the role of the stateless evaluation router `evaluation.py`?",
    "answer": "*   **Answer**: The [evaluation.py](file:///c:/Users/Lenovo/Desktop/vidvantuv1/vidvantu/ExamReadyFastAPI/app/routers/evaluation.py) router defines endpoints for scoring subjective answers and rendering student performance coaching summaries. It is designed to be completely stateless—meaning it receives pre-computed session stats from the Express backend and handles LLM evaluation workloads without direct database reads.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How are subjective answers graded dynamically inside your service?",
    "answer": "*   **Answer**: Subjective answers are routed to `AnswerEvaluator.evaluate_subjective_answers`. The service compiles a prompt detailing the CBSE step-marking guidelines, the textbook answer scheme, and the student's submission. Gemini processes the prompt and returns a JSON array detailing marks awarded, correctness flags, and step-by-step coaching feedback.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How do you prevent performance analysis timeouts when evaluating large exam papers?",
    "answer": "*   **Answer**: To keep response times low, the subjective evaluation endpoint enforces a limit of 25 questions per request. Larger papers must be split into batches and sent as concurrent async queries to prevent timeouts.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How does the `/v1/evaluate/performance` endpoint generate study priorities?",
    "answer": "*   **Answer**: It parses the `PerformanceStats` payload (containing topic accuracies, weakness arrays, and score trends) sent by Dinesh's Express server. The evaluator feeds these stats into Gemini to output structured study priority tables, classifying chapters into HIGH/MEDIUM/LOW priority alongside supporting reasoning.",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  },
  {
    "category": "vidvantu",
    "subcategory": "Vidvantu Architecture & FastAPI",
    "question": "How are database migrations executed concurrently with Express?",
    "answer": "*   **Answer**: Dinesh handles migrations using Prisma schemas. To prevent database locks, you run raw validation scripts (like `validate_migration.py`) that verify PostgreSQL tables and column alignments before starting up the FastAPI server.\n\n---\n*Created for your Ruvinsys Backend AI interview preparation. Good luck!*",
    "is_coding": False,
    "code_sql": "",
    "code_java": "",
    "code_python": ""
  }
]

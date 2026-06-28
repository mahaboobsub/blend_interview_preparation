# db_projects.py - COMPREHENSIVE DevOps, System Design, Git, Postman, Projects
# Covers: Git, Postman, System Design, Project walkthroughs, Behavioral

PROJECT_QUESTIONS = []

def add(sub, q, a, is_coding=False, code_python="", code_sql=""):
    PROJECT_QUESTIONS.append({
        "category": "devops_projects",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": is_coding,
        "code_sql": code_sql.strip(),
        "code_java": "",
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# GIT & VERSION CONTROL (15)
# ═══════════════════════════════════════════════════════════════

add("Git", "What is Git? Explain the basic workflow.", """
Git is a distributed version control system that tracks changes in source code.
* **Basic workflow**:
  1. **git init**: Initialize a repository.
  2. **git add <file>**: Stage changes (working dir → staging area).
  3. **git commit -m 'message'**: Save staged changes to local repository.
  4. **git push**: Upload local commits to remote (GitHub, GitLab).
  5. **git pull**: Fetch and merge remote changes.
* **Three areas**: Working Directory → Staging Area (Index) → Repository.
""")

add("Git", "What is the difference between git merge and git rebase?", """
* **git merge**: Creates a merge commit combining two branches. Preserves complete history. Non-destructive.
  - git checkout main; git merge feature → creates merge commit.
* **git rebase**: Moves (replays) your branch's commits on top of another branch. Creates linear history. Rewrites commit history.
  - git checkout feature; git rebase main → replays feature commits after main's HEAD.
* **When to use**:
  - Merge: Public/shared branches. When preserving history is important.
  - Rebase: Local/feature branches before merging to main. Clean, linear history.
* **Golden rule**: Never rebase commits that have been pushed to a shared branch.
""")

add("Git", "What is git stash? When would you use it?", """
git stash temporarily saves uncommitted changes (both staged and unstaged) so you can switch branches cleanly.
* **Commands**:
  - git stash: Save current changes.
  - git stash pop: Apply most recent stash and remove it from stash list.
  - git stash apply: Apply stash but keep it in the list.
  - git stash list: Show all saved stashes.
  - git stash drop: Remove a specific stash.
* **Use cases**: Need to switch branches but have uncommitted work. Pull latest changes on a dirty working directory.
""")

add("Git", "What is a git conflict? How do you resolve it?", """
A merge conflict occurs when two branches modify the same lines in a file, and Git can't automatically merge.
* **How to resolve**:
  1. Git marks conflicts in the file with <<<<<<< HEAD, =======, and >>>>>>> branch-name markers.
  2. Manually edit the file to choose correct changes.
  3. Remove conflict markers.
  4. Stage the resolved file: git add <file>.
  5. Complete the merge: git commit.
* **Prevention**: Communicate with team, merge frequently, keep branches small and short-lived.
""")

add("Git", "Explain git cherry-pick, git bisect, and git reset.", """
* **git cherry-pick <commit>**: Apply a specific commit from one branch to another without merging the entire branch. Useful for hotfixes.
* **git bisect**: Binary search through commit history to find which commit introduced a bug. git bisect start → git bisect bad → git bisect good <commit> → Git checks out middle commit for testing.
* **git reset**: Move HEAD and potentially modify staging area and working directory.
  - --soft: Move HEAD only. Changes stay staged.
  - --mixed (default): Move HEAD, unstage changes. Changes stay in working directory.
  - --hard: Move HEAD, discard ALL changes. Dangerous!
""")

add("Git", "What is a .gitignore file? What should be in it?", """
.gitignore specifies files and directories that Git should NOT track.
* **Common entries**:
  - node_modules/ — npm packages (large, recreatable).
  - __pycache__/, *.pyc — Python compiled files.
  - .env — Environment variables (secrets!).
  - dist/, build/ — Build artifacts.
  - .DS_Store — macOS metadata.
  - *.log — Log files.
  - .idea/, .vscode/ — IDE configuration.
* **Pattern syntax**: * (wildcard), / (directory), ! (negation), ** (recursive match).
* **Best practice**: Add .gitignore BEFORE first commit. Use templates from github.com/github/gitignore.
""")

add("Git", "Explain Git branching strategies: GitFlow, GitHub Flow, Trunk-Based.", """
* **GitFlow**: Complex branching with main, develop, feature, release, and hotfix branches. Good for scheduled releases.
* **GitHub Flow**: Simple — main branch + feature branches. Feature branches are short-lived, merged via Pull Requests. Good for continuous deployment.
* **Trunk-Based Development**: All developers commit to a single branch (main/trunk). Feature flags hide incomplete work. Fastest CI/CD cycle.
* **Best practice for teams**: GitHub Flow for most web projects. GitFlow for versioned software releases. Trunk-based for high-velocity teams.
""")

# ═══════════════════════════════════════════════════════════════
# POSTMAN & API TESTING (10)
# ═══════════════════════════════════════════════════════════════

add("Postman", "What is Postman? How do you use it for API testing?", """
Postman is an API development and testing platform.
* **Key features**:
  1. **Request builder**: Send GET, POST, PUT, DELETE requests with headers, body, params.
  2. **Collections**: Organize related API requests into groups.
  3. **Environment variables**: Store base URLs, tokens, keys for different environments (dev, staging, prod).
  4. **Tests**: Write JavaScript test scripts to validate responses.
  5. **Pre-request scripts**: Set up data before each request (generate timestamps, compute signatures).
  6. **Mock servers**: Simulate API endpoints before backend is ready.
  7. **Newman**: CLI runner for running Postman collections in CI/CD pipelines.
""")

add("Postman", "How do you write test assertions in Postman?", """
Postman uses JavaScript in the 'Tests' tab to validate API responses:
* **Status code**: pm.test('Status 200', () => pm.response.to.have.status(200));
* **JSON body**: pm.test('Has name', () => { let json = pm.response.json(); pm.expect(json.name).to.eql('Alice'); });
* **Response time**: pm.test('Fast response', () => pm.expect(pm.response.responseTime).to.be.below(500));
* **Headers**: pm.test('Content-Type', () => pm.response.to.have.header('Content-Type', 'application/json'));
* **Chaining**: Set variable from response: pm.environment.set('token', pm.response.json().access_token); — used in next request's Authorization header.
""")

add("Postman", "How do you automate API tests with Postman and Newman?", """
Newman is Postman's CLI tool for running collections in CI/CD:
* **Export collection**: From Postman → Export → Collection v2.1 JSON.
* **Run**: newman run collection.json -e environment.json
* **CI/CD integration**: Add Newman step in GitHub Actions, Jenkins, or GitLab CI:
  - Install: npm install -g newman
  - Run: newman run tests/api_tests.json --reporters cli,html
* **Data-driven testing**: Use CSV/JSON data files: newman run collection.json -d test_data.csv
* **Reports**: Generate HTML reports with newman-reporter-htmlextra.
""")

# ═══════════════════════════════════════════════════════════════
# SYSTEM DESIGN (15)
# ═══════════════════════════════════════════════════════════════

add("System Design", "How would you design a URL shortener (like bit.ly)?", """
* **Requirements**: Generate short URL from long URL. Redirect short URL to original. Track click analytics.
* **Architecture**:
  1. **Encoding**: Use Base62 encoding (a-z, A-Z, 0-9). 7 chars = 62⁷ = 3.5 trillion unique URLs.
  2. **Database**: Key-value store (Redis) for fast lookups. PostgreSQL for persistence.
  3. **Hash collision**: Counter-based approach (auto-increment ID → Base62) or hash (MD5/SHA → take first 7 chars) with collision check.
  4. **Read-heavy**: Cache popular URLs in Redis. 80/20 rule — 20% of URLs get 80% of traffic.
  5. **Scaling**: Horizontal scaling with load balancer. Database sharding by hash prefix.
""")

add("System Design", "What is a load balancer? Common algorithms.", """
A load balancer distributes incoming network traffic across multiple servers.
* **Algorithms**:
  1. **Round Robin**: Requests distributed sequentially. Simple but ignores server capacity.
  2. **Weighted Round Robin**: Servers with more capacity get more requests.
  3. **Least Connections**: Routes to server with fewest active connections.
  4. **IP Hash**: Consistent mapping of client IP to server. Good for session persistence.
  5. **Random**: Randomly selects a server. Simple, works well at scale.
* **Types**: Layer 4 (TCP/UDP — faster) vs Layer 7 (HTTP — content-aware routing).
* **Tools**: Nginx, HAProxy, AWS ALB/NLB.
""")

add("System Design", "What is caching? Explain caching strategies.", """
Caching stores frequently accessed data in fast storage (memory) to reduce latency and database load.
* **Strategies**:
  1. **Cache-Aside (Lazy Loading)**: App checks cache first. On miss, fetches from DB, stores in cache. Most common.
  2. **Write-Through**: Every write goes to cache AND database simultaneously. Consistent but slower writes.
  3. **Write-Behind**: Write to cache only. Asynchronously batch-write to database. Fast writes but risk of data loss.
  4. **Read-Through**: Cache automatically fetches from DB on miss. App only interacts with cache.
* **Eviction policies**: LRU (Least Recently Used), LFU (Least Frequently Used), TTL (Time-To-Live).
* **Tools**: Redis, Memcached.
""")

add("System Design", "What is a message queue? When to use Kafka vs RabbitMQ?", """
Message queues decouple producers from consumers, enabling asynchronous communication.
* **RabbitMQ**: Traditional message broker. Push-based. Messages deleted after consumption. Best for: task queues, RPC, complex routing.
* **Apache Kafka**: Distributed event streaming platform. Pull-based. Messages retained (configurable duration). Best for: event sourcing, log aggregation, real-time analytics, high-throughput data pipelines.
* **Key differences**:
  | Feature | RabbitMQ | Kafka |
  |---------|----------|-------|
  | Model | Message queue | Event log |
  | Throughput | Medium | Very high |
  | Retention | Deleted after ack | Retained |
  | Ordering | Per queue | Per partition |
""")

add("System Design", "What is a microservices architecture? Pros and cons vs monolith.", """
* **Monolith**: Single deployable unit containing all functionality. Simple to develop initially but hard to scale and modify independently.
* **Microservices**: Application split into small, independent services, each owning its own data and deployed separately.
* **Pros of microservices**:
  1. Independent deployment and scaling.
  2. Technology diversity (each service can use different language/DB).
  3. Fault isolation (one service failing doesn't crash everything).
  4. Team autonomy.
* **Cons**: Distributed system complexity, network latency, data consistency challenges, operational overhead (monitoring, debugging).
* **When to use monolith**: Small teams, early-stage products, low complexity.
""")

add("System Design", "Explain horizontal vs vertical scaling.", """
* **Vertical Scaling (Scale Up)**: Add more resources (CPU, RAM, disk) to existing server. Simpler. Has hardware limits.
* **Horizontal Scaling (Scale Out)**: Add more servers/instances. Distribute load. Theoretically unlimited.
* **Comparison**:
  | Feature | Vertical | Horizontal |
  |---------|----------|------------|
  | Simplicity | Simpler | Complex (load balancing, state management) |
  | Limit | Hardware ceiling | Theoretically unlimited |
  | Downtime | Usually required | Zero downtime possible |
  | Cost | Expensive at high end | Commodity hardware |
* **Modern approach**: Start vertical, then go horizontal when needed. Use auto-scaling groups.
""")

add("System Design", "What is a CDN? How does it improve performance?", """
A CDN (Content Delivery Network) is a globally distributed network of edge servers that cache content closer to users.
* **How it works**: Static assets (images, CSS, JS, videos) are cached on edge servers worldwide. User requests are routed to the nearest edge server instead of the origin.
* **Benefits**:
  1. **Reduced latency**: Content served from nearby edge, not distant origin.
  2. **Reduced origin load**: Edge servers handle most requests.
  3. **DDoS protection**: Distributed infrastructure absorbs attacks.
  4. **High availability**: If one edge fails, traffic reroutes to next nearest.
* **Examples**: Cloudflare, AWS CloudFront, Akamai, Vercel Edge Network.
""")

# ═══════════════════════════════════════════════════════════════
# PROJECT WALKTHROUGHS (15)
# ═══════════════════════════════════════════════════════════════

add("Projects", "Walk me through your VGG16 Fashion Recommender project.", """
* **Problem**: Build a visual similarity-based fashion recommendation system.
* **Architecture**:
  1. **Feature Extraction**: Used pre-trained VGG16 (trained on ImageNet) as a feature extractor. Removed the final classification layers, using the FC layers' 4096-dimensional output as a feature vector.
  2. **Dataset**: Fashion product images. Each image processed through VGG16 to generate a feature vector.
  3. **Similarity**: Computed cosine similarity between the query image's feature vector and all stored feature vectors.
  4. **Top-K**: Retrieved the K most similar products based on highest cosine similarity scores.
* **Why VGG16**: Strong feature extraction despite being older. Transfer learning reduces training time. 3×3 convolution filters capture fine-grained visual patterns.
""")

add("Projects", "How would you handle cold-start in a recommendation system?", """
Cold-start: New users (no history) or new items (no interactions) → recommender has no data.
* **New user strategies**:
  1. **Content-based**: Recommend popular or trending items.
  2. **Onboarding questionnaire**: Ask preferences during signup.
  3. **Demographic-based**: Use age, location, gender for initial recommendations.
  4. **Hybrid**: Combine content-based with collaborative filtering as data accumulates.
* **New item strategies**:
  1. **Content-based features**: Use item metadata (description, category, image features from VGG16).
  2. **Exploration**: Randomly show new items to collect feedback.
  3. **Similar items**: Use item attributes to find similar existing items with known preferences.
""")

add("Projects", "Explain your RAG-based chatbot project architecture.", """
* **Architecture**:
  1. **Document Ingestion**: PDF/text documents loaded → chunked (500 tokens, 50 overlap) → embedded using sentence-transformers → stored in vector database (FAISS/ChromaDB).
  2. **Query Processing**: User question → embedded → similarity search retrieves top-5 relevant chunks.
  3. **Augmented Prompt**: System prompt + retrieved chunks + user question → sent to LLM (GPT-4/Claude).
  4. **Response**: LLM generates grounded answer based on retrieved context.
* **Key decisions**:
  - Chunk size: 500 tokens balances context vs specificity.
  - Overlap: 50 tokens prevents information loss at chunk boundaries.
  - Reranking: Added cross-encoder reranker to improve retrieval quality.
  - Memory: ConversationBufferWindowMemory (last 5 exchanges) for multi-turn conversations.
""")

add("Projects", "How did you deploy your project? Explain the CI/CD pipeline.", """
* **Deployment stack**:
  1. **Containerization**: Docker for consistent environments across dev/staging/prod.
  2. **Cloud**: AWS ECS or Vercel (for static) / Railway (for backend).
  3. **CI/CD**: GitHub Actions pipeline:
     - On push to main: Run linting (flake8/eslint) → Run tests (pytest) → Build Docker image → Push to container registry → Deploy to production.
  4. **Environment management**: .env files with secrets in GitHub Secrets (not in code).
* **Monitoring**: Application logs, error tracking, response time monitoring.
* **Rollback**: If health checks fail, auto-rollback to previous deployment.
""")

add("Projects", "Tell me about a challenging bug you debugged. How did you approach it?", """
* **Structured debugging approach (IDEAL for interviews)**:
  1. **Reproduce**: Identify exact steps to reproduce consistently.
  2. **Isolate**: Narrow down — which component? Which line? Use binary search (comment out half the code).
  3. **Hypothesize**: Form theories about root cause based on symptoms.
  4. **Test**: Verify hypothesis with targeted debugging (print statements, breakpoints, logs).
  5. **Fix & Verify**: Apply fix, run regression tests, verify in staging.
* **Example response structure**: 'In my [project], I encountered [symptom]. I isolated it to [component] by [method]. The root cause was [issue]. I fixed it by [solution] and added [tests] to prevent regression.'
""")

add("Projects", "How do you handle API rate limiting in production?", """
Rate limiting controls how many requests a client can make in a time window.
* **Implementation approaches**:
  1. **Token Bucket**: Tokens added at fixed rate. Each request costs a token. Burst-friendly.
  2. **Sliding Window**: Count requests in a rolling time window. Smoother than fixed window.
  3. **Fixed Window**: Count requests in discrete time intervals (e.g., 100 req/min). Simple but allows burst at window boundaries.
* **Server-side**: Use middleware (express-rate-limit, slowapi for FastAPI). Store counts in Redis for distributed systems.
* **Client-side (calling external APIs)**: Implement exponential backoff with jitter. Respect Retry-After headers. Queue requests.
""")

add("Projects", "What is Docker? Explain Dockerfile, images, and containers.", """
Docker packages applications and dependencies into portable, isolated containers.
* **Key concepts**:
  1. **Dockerfile**: Blueprint/recipe for building an image. Contains: FROM (base image), COPY, RUN, CMD instructions.
  2. **Image**: Read-only template built from Dockerfile. Layered filesystem.
  3. **Container**: Running instance of an image. Isolated process with its own filesystem, network.
  4. **docker-compose**: Define and run multi-container applications (app + database + redis) from a single YAML file.
* **Benefits**: Consistent environments, fast deployment, isolation, scalability.
* **Common commands**: docker build, docker run, docker ps, docker stop, docker logs.
""")


add("Projects", "In your Fashion Recommendation System, how exactly did you extract features from images, and why did you use a pre-trained CNN?", """
* **Feature Extraction Process**:
  1. **Preprocessing**: Images were loaded and resized to the required input size of the model (e.g., 224x224 for VGG16/ResNet). They were then converted to arrays and preprocessed (e.g., zero-centering color channels) using the model's specific preprocessing function (`preprocess_input`).
  2. **Model Architecture**: I loaded a pre-trained CNN (like VGG16 or ResNet50) excluding the top classification layers (`include_top=False`). 
  3. **Pooling**: I applied Global Average Pooling (or Global Max Pooling) to the final convolutional feature map to flatten it into a 1D vector (e.g., a 2048-d or 4096-d vector).
  4. **Normalization**: The extracted feature vector was normalized (e.g., L2 normalization) so that the scale of the features wouldn't affect the similarity calculations.
* **Why Pre-trained (Transfer Learning)**: 
  - Training a deep CNN from scratch requires a massive dataset (millions of images) and significant compute power. 
  - Pre-trained models (trained on ImageNet) have already learned excellent hierarchical visual features (edges, textures, shapes, object parts) that generalize perfectly to clothing and fashion items.
""")

add("Projects", "How did you measure the similarity between the input image and the dataset images in your fashion recommender?", """
* **Cosine Similarity**: I used Cosine Similarity to compare the feature vector of the input image against the feature vectors of all images in the database.
* **Why Cosine?**: Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It is highly effective for high-dimensional feature vectors because it cares about the *direction* (the pattern of features) rather than the *magnitude* (overall intensity). 
* **Process**: 
  1. The input image is converted into a normalized feature vector.
  2. The dot product is calculated between the input vector and all database vectors.
  3. The database images are sorted in descending order of their similarity scores (where 1 is identical and 0 is completely orthogonal).
  4. The top N images are returned as recommendations.
* **Alternatives**: Euclidean distance (L2 distance) could also be used, but Cosine is generally preferred for normalized deep learning embeddings as it handles the high-dimensional space more robustly.
""")

add("Projects", "If you wanted to scale or improve the accuracy of your fashion recommendation system, what techniques would you apply?", """
* **Accuracy Improvements**:
  1. **Fine-tuning**: Unfreeze the last few convolutional blocks of the pre-trained model and train it on the fashion dataset using a Triplet Loss or Contrastive Loss function to explicitly teach the model what 'similar' clothing looks like.
  2. **Object Detection / Segmentation**: Use YOLO or Mask R-CNN to detect and crop just the clothing item (ignoring the background, model's face, or text), passing only the cropped clothing to the feature extractor.
  3. **Multi-modal embeddings**: Combine the image features with text features (clothing description, brand, color text) using a model like CLIP.
* **Scaling Improvements**:
  1. **Vector Database**: Instead of doing a linear scan using basic Cosine Similarity, I would use a Vector Database like Qdrant, Pinecone, or FAISS (Facebook AI Similarity Search) which uses Approximate Nearest Neighbor (ANN) algorithms (like HNSW) to reduce search time.
  2. **Caching**: Cache frequent search queries using Redis.
""")


add("Projects", "Walk me through the architecture and security features of your Password Manager project.", """
* **Overview**: I built a secure Password Manager application that allows users to store, retrieve, and generate strong passwords.
* **Architecture**: 
  - **Frontend**: A React or vanilla JS interface for users to log in, view their vault, and add new credentials.
  - **Backend**: A Node.js/Express or Python/FastAPI backend to handle authentication and encrypted data storage.
  - **Database**: PostgreSQL or MongoDB to store user accounts and their encrypted password vaults.
* **Core Security Features**:
  1. **Master Password**: Users authenticate with a Master Password that is never stored in plaintext.
  2. **Zero-Knowledge Architecture (Client-Side Encryption)**: The actual passwords in the vault are encrypted on the client side before being sent to the server. The server only stores the encrypted ciphertext and never sees the decryption key.
  3. **Data in Transit**: Enforced HTTPS/TLS for all communications to prevent Man-In-The-Middle (MITM) attacks.
""")

add("Projects", "How did you ensure that user passwords were safe from both database leaks and internal server compromises?", """
* **Authentication (Protecting the Master Password)**: 
  - When a user signs up, their Master Password is hashed using a strong key derivation function like **bcrypt** or **PBKDF2** with a unique random **salt**. 
  - If the database is leaked, attackers only get the hashes and salts, making brute-forcing computationally expensive.
* **Vault Encryption (Protecting Stored Passwords)**:
  - I used **AES-256-GCM** (Advanced Encryption Standard with Galois/Counter Mode), which provides both confidentiality and data integrity (authenticated encryption).
  - The encryption key is derived from the user's Master Password (using PBKDF2). 
  - Crucially, encryption and decryption happen **on the client side** (in the browser). The backend only receives and stores the AES-encrypted strings. Therefore, even if the server is compromised or an admin looks at the database, they cannot read the user's saved passwords (Zero-Knowledge).
""")

add("Projects", "How did you manage user sessions and authentication in your Password Manager?", """
* **JWT (JSON Web Tokens)**: Upon successful login (verifying the bcrypt hash of the Master Password), the server issues a JWT.
* **Security Measures for JWT**:
  1. **Short Expiration**: Tokens expire quickly (e.g., 15 minutes) to limit the window of opportunity if a token is stolen.
  2. **Refresh Tokens**: Used an HttpOnly, Secure cookie to store a longer-lived refresh token, which is used to obtain new access tokens without re-entering the Master Password.
  3. **HttpOnly Cookies**: By storing the JWT or refresh token in HttpOnly cookies, I protected the session against Cross-Site Scripting (XSS) attacks, as JavaScript cannot access the token.
  4. **CSRF Protection**: Implemented Anti-CSRF tokens to ensure that requests to modify the vault originated from the legitimate frontend.
""")

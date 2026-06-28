# db_fullstack.py - COMPREHENSIVE Fullstack Development
# Covers: Python, JavaScript, OOP, REST APIs, FastAPI, Node.js, JWT/Security, WebSockets

FULLSTACK_QUESTIONS = []

def add(sub, q, a, is_coding=False, code_python="", code_java=""):
    FULLSTACK_QUESTIONS.append({
        "category": "fullstack",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": is_coding,
        "code_sql": "",
        "code_java": code_java.strip(),
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# PYTHON FUNDAMENTALS (20)
# ═══════════════════════════════════════════════════════════════

add("Python", "What is the difference between a list and a tuple in Python?", """
* **List**: Mutable, can add/remove/change elements. Uses square brackets []. Slower due to dynamic resizing.
* **Tuple**: Immutable, cannot be modified after creation. Uses parentheses (). Faster, hashable (can be dict keys).
* **When to use**: Tuples for fixed collections (coordinates, RGB values, function return values). Lists for collections that change.
""")

add("Python", "Explain *args and **kwargs in Python.", """
* ***args**: Collects positional arguments into a tuple. Allows a function to accept any number of positional arguments.
* ****kwargs**: Collects keyword arguments into a dictionary. Allows any number of named arguments.
* **Order**: def func(regular, *args, **kwargs)
* **Example**: def greet(*names, **options): — names is tuple, options is dict.
* **Unpacking**: Can also use * and ** to unpack iterables/dicts when calling functions.
""")

add("Python", "What are decorators in Python? Give an example.", """
A decorator is a function that wraps another function to extend its behavior without modifying it.
* **Syntax**: @decorator above function definition.
* **How it works**: Takes a function as input, returns a new function with added behavior.
""", is_coding=True, code_python="""
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time; time.sleep(1)
    return "done"
""")

add("Python", "What are generators in Python? How do they differ from lists?", """
Generators produce values lazily, one at a time, using yield instead of return.
* **Memory efficient**: Don't store all values in memory. Generate on-the-fly.
* **Syntax**: def gen(): yield 1; yield 2; yield 3 OR (x**2 for x in range(10))
* **vs List**: List stores all values in memory at once. Generator produces values on demand.
* **Use cases**: Processing large files line-by-line, infinite sequences, pipeline processing.
* **Key methods**: next(gen), send(value), close(), throw(exception).
""")

add("Python", "Explain list comprehensions vs generator expressions.", """
* **List comprehension**: [x**2 for x in range(10)] — Creates entire list in memory. Fast for small datasets.
* **Generator expression**: (x**2 for x in range(10)) — Creates generator object. Memory efficient for large datasets.
* **When to use generators**: When you only need to iterate once, or data is too large for memory.
* **Dict comprehension**: {k: v for k, v in pairs}
* **Set comprehension**: {x**2 for x in range(10)}
""")

add("Python", "What is the GIL (Global Interpreter Lock) in Python?", """
The GIL is a mutex that allows only one thread to execute Python bytecode at a time (in CPython).
* **Impact**: CPU-bound tasks don't benefit from multi-threading in Python. Only one thread runs at a time.
* **Workarounds**:
  1. **multiprocessing**: Use separate processes (each has its own GIL).
  2. **C extensions**: NumPy releases GIL during computation.
  3. **asyncio**: For I/O-bound tasks (network, file I/O), async is effective because GIL is released during I/O waits.
  4. **Alternative interpreters**: PyPy, Jython (no GIL).
* **Note**: GIL is only in CPython. I/O-bound multi-threading still works because GIL is released during I/O.
""")

add("Python", "Explain Python's memory management and garbage collection.", """
* **Reference counting**: Primary mechanism. Each object has a count of references. When count reaches 0, memory is freed immediately.
* **Cyclic garbage collector**: Handles circular references (A→B→A) that reference counting can't catch. Runs periodically on 'generations' (gen0, gen1, gen2).
* **Memory pool (pymalloc)**: Python pre-allocates small blocks of memory for objects < 512 bytes.
* **Interning**: Python caches small integers (-5 to 256) and some strings for reuse.
* **del**: Decreases reference count, doesn't guarantee immediate deallocation.
""")

add("Python", "What is the difference between shallow copy and deep copy?", """
* **Shallow copy**: Creates new object but references same nested objects. Changes to nested objects affect both. copy.copy() or list.copy().
* **Deep copy**: Creates new object AND recursively copies all nested objects. Fully independent. copy.deepcopy().
* **Assignment (=)**: No copy at all. Both variables point to same object.
* **Example**: a = [[1,2],[3,4]]; b = copy.copy(a); b[0].append(5) — a is also modified!
""")

add("Python", "Explain exception handling in Python. Try/except/else/finally.", """
* **try**: Code that might raise an exception.
* **except**: Handles specific exceptions. except ValueError as e: handles ValueError.
* **else**: Runs only if no exception was raised in try block.
* **finally**: Always runs, regardless of exceptions. Used for cleanup (closing files, connections).
* **Custom exceptions**: class MyError(Exception): pass
* **Best practices**: Catch specific exceptions (not bare except:). Use context managers (with statement) for resources.
""")

add("Python", "What are context managers? Explain the 'with' statement.", """
Context managers handle setup and teardown automatically, ensuring resources are properly managed.
* **with statement**: Guarantees cleanup (close, release) even if exceptions occur.
* **Built-in examples**: open(), threading.Lock(), database connections.
* **Custom context manager**: Implement __enter__ and __exit__ methods, OR use @contextmanager decorator.
""", is_coding=True, code_python="""
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Opening {name}")
    try:
        yield name  # Resource available in 'with' block
    finally:
        print(f"Closing {name}")  # Always runs

with managed_resource("file.txt") as f:
    print(f"Using {f}")
""")

# ═══════════════════════════════════════════════════════════════
# OOP CONCEPTS (20)
# ═══════════════════════════════════════════════════════════════

add("OOP", "Explain the four pillars of OOP: Encapsulation, Abstraction, Inheritance, Polymorphism.", """
1. **Encapsulation**: Bundling data and methods into a class. Restricting direct access to internals using access modifiers (private, protected, public).
2. **Abstraction**: Hiding complex implementation details, exposing only necessary interfaces. Abstract classes and interfaces.
3. **Inheritance**: Creating new classes from existing ones. Child class inherits parent's attributes and methods. Promotes code reuse.
4. **Polymorphism**: Same interface, different implementations. Method overriding (runtime) and method overloading (compile-time in Java).
""")

add("OOP", "What is the difference between an abstract class and an interface?", """
* **Abstract class**: Can have both abstract (unimplemented) and concrete (implemented) methods. Can have state (instance variables). Single inheritance in Java.
* **Interface**: Only abstract methods (Java 7), can have default methods (Java 8+). No state (only constants). Multiple interfaces can be implemented.
* **When to use**:
  - Abstract class: Shared base implementation + some methods that subclasses must implement.
  - Interface: Define a contract that multiple unrelated classes can implement.
* **Python**: Uses abc.ABC and @abstractmethod. No strict interfaces but uses duck typing.
""")

add("OOP", "Explain SOLID principles in object-oriented design.", """
1. **S - Single Responsibility**: A class should have only one reason to change.
2. **O - Open/Closed**: Classes should be open for extension, closed for modification.
3. **L - Liskov Substitution**: Subclasses should be substitutable for their parent class without breaking behavior.
4. **I - Interface Segregation**: Many specific interfaces are better than one general-purpose interface. Don't force classes to implement methods they don't use.
5. **D - Dependency Inversion**: High-level modules should not depend on low-level modules. Both should depend on abstractions.
""")

add("OOP", "What is method overloading vs method overriding?", """
* **Overloading** (Compile-time polymorphism): Same method name, different parameter types/counts in the SAME class. Java supports it natively. Python doesn't (uses *args/**kwargs instead).
* **Overriding** (Runtime polymorphism): Subclass provides its own implementation of a parent's method. Same name, same parameters. Uses @Override annotation in Java.
* **Key difference**: Overloading is resolved at compile time. Overriding is resolved at runtime based on actual object type.
""")

add("OOP", "What are design patterns? Explain Singleton, Factory, and Observer.", """
Design patterns are reusable solutions to common software design problems:
* **Singleton**: Ensures only one instance of a class exists. Private constructor + static instance method. Use: database connections, logging, configuration.
* **Factory**: Creates objects without specifying the exact class. Delegates instantiation to subclasses. Use: when object creation logic is complex.
* **Observer**: One-to-many dependency. When one object changes state, all dependents are notified. Use: event systems, pub/sub, reactive programming.
""")

# ═══════════════════════════════════════════════════════════════
# JAVASCRIPT (20)
# ═══════════════════════════════════════════════════════════════

add("JavaScript", "Explain var, let, and const in JavaScript.", """
* **var**: Function-scoped. Hoisted (declaration moved to top, value is undefined). Can be redeclared. AVOID in modern JS.
* **let**: Block-scoped. Not hoisted (temporal dead zone). Cannot be redeclared in same scope. Use for variables that change.
* **const**: Block-scoped. Must be initialized at declaration. Cannot be reassigned. Use for constants and object references (note: object properties CAN be mutated).
""")

add("JavaScript", "What are Promises? Explain async/await.", """
* **Promise**: Object representing eventual completion or failure of an async operation. States: pending, fulfilled, rejected.
  - .then(onFulfilled), .catch(onRejected), .finally().
* **async/await**: Syntactic sugar over Promises. Makes async code look synchronous.
  - async function: Returns a Promise implicitly.
  - await: Pauses execution until Promise resolves. Only inside async functions.
* **Promise.all()**: Runs multiple promises in parallel, resolves when ALL complete.
* **Promise.race()**: Resolves when FIRST promise completes.
""")

add("JavaScript", "What is the event loop in JavaScript?", """
JavaScript is single-threaded but handles async operations via the event loop:
* **Call Stack**: Executes synchronous code (LIFO).
* **Web APIs**: Handle async operations (setTimeout, fetch, DOM events) in separate threads.
* **Callback Queue (Task Queue)**: Completed callbacks wait here.
* **Microtask Queue**: Promises (.then), MutationObserver. Higher priority than callback queue.
* **Event Loop**: Continuously checks if call stack is empty. If empty, moves microtasks first, then callbacks from queue to stack.
* **Order**: Synchronous code → Microtasks (Promises) → Macrotasks (setTimeout, setInterval).
""")

add("JavaScript", "What are closures in JavaScript?", """
A closure is a function that remembers the variables from its outer scope even after the outer function has returned.
* **How it works**: Inner function 'closes over' the variables of its containing function.
* **Use cases**: Data privacy, function factories, maintaining state in callbacks.
* **Example**:
  function counter() {
    let count = 0;
    return function() { return ++count; }
  }
  const increment = counter();
  increment() → 1, increment() → 2 (count persists!)
""")

add("JavaScript", "Explain prototypal inheritance in JavaScript.", """
JavaScript uses prototypal inheritance — objects inherit directly from other objects.
* **Prototype chain**: Every object has a hidden [[Prototype]] property pointing to its parent object. Property lookups traverse the chain until found or reaching null.
* **Object.create()**: Creates new object with specified prototype.
* **Classes (ES6)**: Syntactic sugar over prototypal inheritance. class Dog extends Animal {} — uses prototype chain internally.
* **vs Classical inheritance**: No classes under the hood (unlike Java/C++). Objects delegate to other objects.
""")

add("JavaScript", "What is 'this' keyword in JavaScript? How does it behave?", """
'this' refers to the object that is executing the current function:
* **Global context**: this = window (browser) or global (Node.js).
* **Object method**: this = the object that owns the method.
* **Regular function**: this = undefined (strict mode) or window (non-strict).
* **Arrow function**: this = lexically inherited from enclosing scope (no own 'this').
* **Event handler**: this = the element that received the event.
* **bind/call/apply**: Explicitly set 'this' to a specific object.
""")

# ═══════════════════════════════════════════════════════════════
# REST API, FASTAPI, NODE.JS (25)
# ═══════════════════════════════════════════════════════════════

add("REST APIs", "What is REST? Explain its core principles.", """
REST (Representational State Transfer) is an architectural style for web APIs:
* **Core principles**:
  1. **Stateless**: Each request contains all info needed. Server doesn't store client state between requests.
  2. **Client-Server**: Separation of concerns. Client handles UI, server handles data/logic.
  3. **Uniform Interface**: Consistent resource-based URLs. HTTP methods map to CRUD operations.
  4. **Cacheable**: Responses should indicate if they can be cached.
  5. **Layered System**: Client can't tell if connected directly to server or intermediary.
* **HTTP methods**: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
""")

add("REST APIs", "What are HTTP status codes? Explain the major categories.", """
* **1xx (Informational)**: 100 Continue.
* **2xx (Success)**: 200 OK, 201 Created, 204 No Content.
* **3xx (Redirection)**: 301 Moved Permanently, 302 Found, 304 Not Modified.
* **4xx (Client Error)**: 400 Bad Request, 401 Unauthorized (not authenticated), 403 Forbidden (no permission), 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests.
* **5xx (Server Error)**: 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable.
""")

add("FastAPI", "What is FastAPI? Key features and advantages.", """
FastAPI is a modern Python web framework for building APIs with automatic OpenAPI documentation.
* **Key features**:
  1. **Type hints**: Uses Pydantic models for request/response validation with Python type hints.
  2. **Async support**: Native async/await for high-performance concurrent handling.
  3. **Auto-documentation**: Generates Swagger UI and ReDoc automatically from code.
  4. **Dependency injection**: Built-in DI system for shared resources, auth, DB connections.
  5. **Performance**: Built on Starlette (ASGI) and Uvicorn. One of the fastest Python frameworks.
* **vs Flask**: Flask is synchronous, no built-in validation, no auto-docs. FastAPI is async-first with type safety.
""")

add("FastAPI", "Explain Pydantic models in FastAPI. How do they validate data?", """
Pydantic models define data schemas using Python type hints:
* **Automatic validation**: Incoming request data is validated against the model. Invalid data returns 422 error with details.
* **Serialization**: Converts between Python objects and JSON automatically.
* **Features**: Default values, optional fields, nested models, custom validators (@validator), computed fields.
""", is_coding=True, code_python="""
from pydantic import BaseModel, validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    bio: Optional[str] = None

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

# FastAPI uses this model:
# @app.post("/users")
# async def create_user(user: UserCreate):
#     return {"id": 1, **user.dict()}
""")

add("FastAPI", "What is dependency injection in FastAPI? Give an example.", """
Dependency injection provides reusable components (database sessions, auth checks, config) to route handlers.
* **How it works**: Define a function that yields/returns a resource. Use Depends() in route parameters.
* **Benefits**: Centralized resource management, testability (easy to mock), automatic cleanup.
""", is_coding=True, code_python="""
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Injected into route handler
    finally:
        db.close()  # Cleanup after request

# Dependency: verify authentication
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/items")
async def read_items(db = Depends(get_db), user = Depends(get_current_user)):
    return db.query(Item).filter(Item.owner_id == user.id).all()
""")

add("Node.js", "What is Node.js? How does its event-driven architecture work?", """
Node.js is a JavaScript runtime built on Chrome's V8 engine for server-side programming.
* **Event-driven architecture**:
  1. Single-threaded event loop handles all incoming requests.
  2. Blocking I/O operations (file, network, DB) are offloaded to worker threads (libuv thread pool).
  3. When I/O completes, callback is pushed to the event queue.
  4. Event loop picks up callbacks from the queue and executes them.
* **Non-blocking I/O**: The main thread never waits for I/O. It continues processing other requests.
* **Best for**: I/O-heavy applications (APIs, real-time apps). Not ideal for CPU-intensive tasks.
""")

add("Node.js", "Explain Express.js middleware. How does the middleware chain work?", """
Middleware functions in Express have access to request (req), response (res), and next().
* **Chain**: Request passes through middleware in ORDER of registration. Each middleware can:
  - Modify req/res objects.
  - End the request-response cycle (send response).
  - Call next() to pass control to the next middleware.
* **Types**: Application-level, Router-level, Error-handling (4 params), Built-in (express.json()), Third-party (cors, helmet).
* **Order matters**: Authentication middleware should come before route handlers.
""")

# ═══════════════════════════════════════════════════════════════
# JWT, SECURITY, AUTH (15)
# ═══════════════════════════════════════════════════════════════

add("Auth & Security", "What is JWT? How does JWT-based authentication work?", """
JWT (JSON Web Token) is a compact, self-contained token for secure information exchange.
* **Structure**: Header.Payload.Signature (Base64 encoded, dot-separated).
  - Header: {alg: 'HS256', typ: 'JWT'}
  - Payload: Claims (sub, name, exp, iat, custom data).
  - Signature: HMAC-SHA256(base64(header) + '.' + base64(payload), secret_key).
* **Auth flow**:
  1. User sends credentials (login).
  2. Server validates, creates JWT, returns it.
  3. Client stores JWT (httpOnly cookie or localStorage).
  4. Client sends JWT in Authorization: Bearer <token> header.
  5. Server verifies signature and extracts claims.
""")

add("Auth & Security", "JWT vs Session-based authentication: pros and cons.", """
* **Session-based**:
  - Server stores session data. Client gets session ID in cookie.
  - Pros: Easy to revoke (delete server-side session). Smaller cookie size.
  - Cons: Server memory usage. Not scalable without shared session store (Redis).
* **JWT-based**:
  - Server is stateless. All info in the token.
  - Pros: Stateless, scalable, works across microservices, no server storage.
  - Cons: Can't easily revoke (until expiry). Token size larger. Must handle refresh tokens.
* **Best practice**: Short-lived access tokens (15 min) + longer refresh tokens (7 days) with token blacklisting for logout.
""")

add("Auth & Security", "What is OAuth 2.0? Explain the authorization code flow.", """
OAuth 2.0 is an authorization framework that allows third-party apps to access user resources without sharing passwords.
* **Authorization Code Flow** (most secure):
  1. User clicks 'Login with Google' → App redirects to Google's auth server.
  2. User authenticates with Google and grants permission.
  3. Google redirects back to app with an authorization code.
  4. App exchanges code for access token (server-to-server, code is single-use).
  5. App uses access token to call Google APIs on user's behalf.
* **Key concepts**: Client ID, Client Secret, Redirect URI, Scopes, Access Token, Refresh Token.
""")

add("Auth & Security", "What is CORS? Why is it needed and how do you configure it?", """
CORS (Cross-Origin Resource Sharing) is a browser security mechanism that restricts web pages from making requests to different origins.
* **Same-origin policy**: Browser blocks requests from origin A (frontend) to origin B (API) by default.
* **CORS headers**: Server must include:
  - Access-Control-Allow-Origin: https://myapp.com (or * for any).
  - Access-Control-Allow-Methods: GET, POST, PUT, DELETE.
  - Access-Control-Allow-Headers: Content-Type, Authorization.
* **Preflight request**: For non-simple requests, browser sends OPTIONS request first to check permissions.
* **Configuration**: In FastAPI: app.add_middleware(CORSMiddleware, allow_origins=[...]). In Express: app.use(cors()).
""")

add("Auth & Security", "What are common web security vulnerabilities? OWASP Top 10.", """
* **SQL Injection**: Injecting SQL through user inputs. Prevention: Parameterized queries, ORMs.
* **XSS (Cross-Site Scripting)**: Injecting malicious scripts into web pages. Prevention: Input sanitization, CSP headers, escape output.
* **CSRF (Cross-Site Request Forgery)**: Tricking users into making unwanted requests. Prevention: CSRF tokens, SameSite cookies.
* **Broken Authentication**: Weak passwords, missing MFA, improper session management.
* **Sensitive Data Exposure**: Unencrypted data. Prevention: HTTPS, encryption at rest, hash passwords (bcrypt).
* **Security Misconfiguration**: Default credentials, open ports, verbose error messages.
""")

# ═══════════════════════════════════════════════════════════════
# WEBSOCKETS (5)
# ═══════════════════════════════════════════════════════════════

add("WebSockets", "What are WebSockets? How do they differ from HTTP?", """
WebSockets provide full-duplex, persistent communication between client and server.
* **HTTP**: Request-response model. Client initiates. Connection closed after response. Half-duplex.
* **WebSocket**: Persistent connection. Either side can send messages anytime. Full-duplex. Low overhead.
* **Handshake**: Starts as HTTP request with Upgrade: websocket header. Server responds with 101 Switching Protocols.
* **Use cases**: Real-time chat, live notifications, collaborative editing, stock tickers, online gaming, live dashboards.
* **Alternatives**: Server-Sent Events (SSE) for one-way server → client. Long polling (HTTP fallback).
""")

add("WebSockets", "How do you implement WebSockets in FastAPI?", """
FastAPI has native WebSocket support using Starlette:
""", is_coding=True, code_python="""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all connected clients
            for client in connected_clients:
                await client.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
""")

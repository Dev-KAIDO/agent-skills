---
name: backend-comprehensive
description: Complete backend skill — system design, API design (REST/GraphQL/gRPC), database architecture, caching, message queues, authentication, logging, real-time, microservices, ASP.NET, Node.js, and Python backends. Use for ANY server-side development or architecture work.
---

# Backend Comprehensive — Complete Skill

## Overview

**Single skill for all backend work.** Merges `engineering-backend-architect`, `engineering-system-designer`, `project-backend-service-architect`, `project-api-data-contracts`, `aspnet-core`, `openapi`, `mcp-builder`, `zod-validation`, `pino-logging`, `realtime-sync`, and `mcp-builder`.

---

## 1. System Design (تصميم النظام)

### 1.1 Architecture Patterns
| Pattern | When | Tradeoffs |
|---------|------|-----------|
| **Monolith** | Small team, simple domain | Simple, hard to scale independently |
| **Microservices** | Large team, complex domain | Scalable, operational complexity |
| **Serverless** | Variable load, event-driven | No ops, vendor lock-in |
| **Event-driven** | Async workflows, loose coupling | Resilient, eventual consistency |
| **CQRS** | Read/write heavy, different models | Scalable reads, complexity |
| **Service mesh** | Many microservices | Observability, complexity |

### 1.2 Design Process
```
1. Requirements → functional + non-functional
2. Estimation   → users, QPS, data size, latency
3. High-level   → components and their relationships
4. Data model   → entities, relationships, access patterns
5. API design   → endpoints, contracts, versioning
6. Deep dive    → critical paths, bottlenecks
7. Trade-offs   → CAP, consistency, complexity
8. Scaling      → horizontal, caching, queuing
```

### 1.3 Non-Functional Requirements
- **Performance:** < 200ms p95 for API, < 2s TTFB for pages
- **Availability:** 99.9% (8.7h downtime/year)
- **Scalability:** handle 10x current load
- **Consistency:** strong vs eventual (choose per use case)
- **Security:** authentication, authorization, encryption
- **Observability:** logs, metrics, traces

---

## 2. API Design (تصميم الواجهات البرمجية)

### 2.1 REST Design
```yaml
# Resource-based URLs
GET    /api/v1/users          # List users
GET    /api/v1/users/{id}     # Get user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/{id}     # Update user (full)
PATCH  /api/v1/users/{id}     # Update user (partial)
DELETE /api/v1/users/{id}     # Delete user

# Query parameters
GET /api/v1/users?page=1&limit=20&sort=name&order=asc&role=admin

# Response format
{
  "data": [...],
  "meta": { "page": 1, "limit": 20, "total": 150 },
  "links": { "next": "?page=2", "prev": null }
}

# Error format
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{ "field": "email", "issue": "required" }]
  }
}
```

### 2.2 API Versioning
```
Header:   Accept: application/vnd.api+json;version=2
URL:      /api/v2/users
Query:    /api/users?version=2
```

### 2.3 Pagination
```yaml
# Cursor-based (recommended for infinite scroll)
GET /api/items?cursor=abc123&limit=20

# Offset-based (for numbered pages)
GET /api/items?page=3&limit=20
```

### 2.4 OpenAPI Specification
```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
```

---

### 2.5 OpenAPI Codegen & Contract-First (توليد الكود)

**Contract-first workflow:** write OpenAPI → generate types/clients → implement against types.

```bash
# TypeScript stack
npm i -D openapi-typescript          # spec → .ts types
npm i openapi-fetch                  # typed fetch client
npm i @tanstack/react-query-openapi  # typed React Query hooks
npm i zod zod-openapi                # runtime validation + spec generation
```

```typescript
// generated types
import type { paths } from './api-types';
type User = paths['/users/{id}']['get']['responses']['200']
  ['content']['application/json'];
```

**3.1 essentials:** 3.1 is a JSON Schema superset — nullable via type arrays (`["string","null"]`), `discriminator` for polymorphism, `securitySchemes` for auth flows.

**Common mistakes:**
| Mistake | Fix |
|---------|-----|
| Code-first then docs | Contract-first: spec is source of truth |
| No response schemas | Define every status + shape |
| Vague errors | Reusable error components |
| Missing pagination | Document cursor/page params |
| Ignoring 4xx/5xx | Model failure paths explicitly |

---

## 3. Authentication & Authorization (المصادقة والتفويض)

### 3.1 JWT Implementation
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id, scope="read"):
    payload = {
        "sub": user_id,
        "iss": "auth.example.com",
        "aud": "api.example.com",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "scope": scope,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"],
                           audience="api.example.com",
                           issuer="auth.example.com")
        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
```

### 3.2 OAuth 2.0 Flows
| Flow | Use Case |
|------|----------|
| Authorization Code + PKCE | Web/mobile apps |
| Client Credentials | Server-to-server |
| Device Code | TV/CLI devices |

### 3.3 Session vs Token
| | Session (Cookie) | JWT (Bearer) |
|---|---|---|
| State | Server-side | Stateless |
| Scaling | Sticky sessions needed | Any server |
| Revocation | Immediate | Requires blacklist |
| Cross-domain | Limited | Works everywhere |
| Size | Small (ID only) | Larger (claims) |

---

## 4. Caching (التخزين المؤقت)

### 4.1 Cache Layers
```
Client Cache (browser) → CDN → Application Cache (Redis) → Database
```

### 4.2 Cache Strategies
| Strategy | Invalidation | Best For |
|----------|-------------|----------|
| **Cache-aside** | App manages | General purpose |
| **Write-through** | Write to cache + DB | Read-heavy |
| **Write-behind** | Write to cache, async DB | Write-heavy |
| **Read-through** | Cache fetches from DB | Consistent reads |

### 4.3 Cache Patterns
```python
# Cache-aside pattern
def get_user(user_id):
    # Check cache first
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Cache miss: fetch from DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # Populate cache
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# Cache invalidation
def update_user(user_id, data):
    db.update("UPDATE users SET ... WHERE id = %s", user_id)
    redis.delete(f"user:{user_id}")  # Invalidate stale cache
```

### 4.4 Cache Keys
```
user:{id}           → user:123
users:list:{page}   → users:list:1
config:app          → config:app
session:{token}     → session:abc123
rate:{ip}:{minute}  → rate:192.168.1.1:1704067200
```

### 4.5 Eviction Policies
| Policy | Description |
|--------|-------------|
| LRU | Least Recently Used (default, good general) |
| LFU | Least Frequently Used (good for stable data) |
| TTL | Time To Live (good for temporary data) |
| Random | Simple, unpredictable |

---

## 5. Database Patterns (أنماط قواعد البيانات)

### 5.1 Connection Pooling
```python
# Pool configuration
POOL_SIZE = 20          # active connections
MAX_OVERFLOW = 10       # temporary overflow
POOL_TIMEOUT = 30       # seconds to wait for connection
POOL_RECYCLE = 1800     # recycle connections every 30min
```

### 5.2 Query Optimization
```sql
-- ❌ N+1 queries
SELECT * FROM orders;
SELECT * FROM users WHERE id = 1;  -- per order
SELECT * FROM products WHERE id = 1; -- per order

-- ✅ JOINs or batch loading
SELECT o.*, u.name, p.name 
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id;

-- ✅ Use EXPLAIN
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
-- Ensure Index Scan, not Seq Scan
```

### 5.3 Indexing Strategy
```sql
-- Create indexes based on query patterns
CREATE INDEX idx_users_email ON users(email);           -- WHERE email = ?
CREATE INDEX idx_orders_user ON orders(user_id, created_at); -- WHERE user_id ? ORDER BY created_at
CREATE INDEX idx_posts_status ON posts(status) WHERE status = 'published'; -- partial index

-- Monitor index usage
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;  -- unused indexes
```

### 5.4 Transaction Patterns
```python
# Optimistic locking
def transfer(from_id, to_id, amount):
    with db.transaction():
        from_user = db.get("SELECT * FROM users WHERE id = %s FOR UPDATE", from_id)
        if from_user.balance < amount:
            raise InsufficientFunds()
        db.execute("UPDATE users SET balance = balance - %s WHERE id = %s", amount, from_id)
        db.execute("UPDATE users SET balance = balance + %s WHERE id = %s", amount, to_id)

# Idempotency
def create_order(request_id, items):
    # Check if already processed
    existing = db.get("SELECT * FROM orders WHERE request_id = %s", request_id)
    if existing:
        return existing  # Return existing, don't duplicate
    # ... create order
```

---

## 6. Message Queues (قوائم الرسائل)

### 6.1 When to Use
- **Background jobs:** email, image processing, reports
- **Event propagation:** order created → notify, update inventory
- **Rate limiting:** buffer bursty requests
- **Microservices:** async communication between services

### 6.2 Patterns
```python
# Producer
async def publish_order_created(order):
    await redis.publish("orders", json.dumps({
        "event": "order_created",
        "order_id": order.id,
        "user_id": order.user_id,
        "amount": order.total,
        "timestamp": time.time(),
    }))

# Consumer
async def handle_order_created(message):
    data = json.loads(message)
    await send_email(data["user_id"], "Order confirmed")
    await update_inventory(data["order_id"])

# Retry with dead letter queue
async def process_with_retry(queue, handler, max_retries=3):
    for attempt in range(max_retries):
        try:
            await handler(await queue.get())
            return
        except Exception as e:
            if attempt == max_retries - 1:
                await dead_letter_queue.put(message)  # Failed permanently
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 6.3 Queue Comparison
| Queue | Best For |
|-------|----------|
| **Redis Pub/Sub** | Simple pub/sub, no persistence |
| **Redis Streams** | Persistent, consumer groups |
| **RabbitMQ** | Complex routing, reliability |
| **Kafka** | High throughput, event sourcing |
| **SQS** | AWS, managed, simple |

---

## 7. Logging (التسجيل)

### 7.1 Structured Logging (pino)
```javascript
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: {
    paths: ['req.headers.authorization', 'password', 'token'],
    censor: '[REDACTED]',
  },
});

// Request logging with correlation ID
app.use((req, res, next) => {
  req.id = crypto.randomUUID();
  req.log = logger.child({ reqId: req.id, method: req.method, url: req.url });
  next();
});

// Usage
req.log.info({ userId: 123 }, 'User logged in');
req.log.error({ err, userId: 123 }, 'Login failed');
```

### 7.2 Log Levels
| Level | Use |
|-------|-----|
| **fatal** | System is down |
| **error** | Request failed, needs attention |
| **warn** | Unusual but handled |
| **info** | Significant business events |
| **debug** | Detailed troubleshooting |
| **trace** | Very detailed (development only) |

### 7.3 What to Log
- ✅ Authentication events (login, logout, failed attempts)
- ✅ Data mutations (create, update, delete)
- ✅ Errors with stack traces
- ✅ Performance metrics (slow queries, slow requests)
- ✅ External service calls
- ❌ Don't log: passwords, tokens, PII (without encryption), sensitive data

---

### 7.4 pino Advanced (متقدم)
```javascript
// Worker-thread transport (off main thread — no event-loop blocking)
const transport = pino.transport({
  target: 'pino/file',
  options: { destination: '/var/log/app.log' },
  workerThread: true,
});

// Multi-target: file + stdout + remote
const transport = pino.transport({
  targets: [
    { target: 'pino-pretty', level: 'info' },        // dev only
    { target: 'pino/file', options: { destination: 1 } },
    { target: 'pino-http-send', options: { url: 'https://log-collector' } },
  ],
});

// Rotation
pino.transport({ target: 'pino-roll', options: { file: 'app', size: '100m', days: 7 } });

// HTTP request logging with correlation ID
const app = require('pino-http')({
  genReqId: (req) => req.headers['x-request-id'] || crypto.randomUUID(),
  serializers: { req: (r) => ({ method: r.method, url: r.url, id: r.id }) },
});
```
- **customLevels / formatters / serializers** for structured shape control
- **Fastify:** built-in `logger` option (pino under the hood); **Hono:** `pino-logger` middleware
- **pino-pretty:** development only — never in production (it's slow, it's for humans)
- Reference: see original `pino-logging` skill for transport recipes

---

## 8. Real-Time (الوقت الحقيقي)

### 8.1 WebSocket Implementation
```javascript
// Server
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  ws.on('message', async (data) => {
    const msg = JSON.parse(data);
    switch (msg.type) {
      case 'subscribe':
        channels.set(msg.channel, ws);
        break;
      case 'message':
        broadcast(msg.channel, msg.payload);
        break;
    }
  });
});

// Client
const ws = new WebSocket('wss://api.example.com');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateUI(data);
};
```

### 8.2 SSE (Server-Sent Events)
```javascript
// Server (simpler than WebSocket for one-way)
app.get('/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  });
  
  const sendEvent = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };
  
  eventEmitter.on('update', sendEvent);
  req.on('close', () => eventEmitter.off('update', sendEvent));
});
```

### 8.3 Comparison
| | WebSocket | SSE | Polling |
|---|---|---|---|
| Direction | Bi-directional | Server → Client | Client → Server |
| Protocol | ws/wss | HTTP | HTTP |
| Complexity | Higher | Lower | Lowest |
| Use case | Chat, gaming, collaboration | Notifications, feeds | Simple updates |

### 8.4 WebTransport (HTTP/3) — Modern Alternative
- Runs over HTTP/3 (QUIC): **datagrams** (unreliable, low-latency) + reliable streams
- No head-of-line blocking, 0-RTT reconnect, built-in TLS
- Best for: games, live cursors, high-frequency telemetry
- Use when: WebSocket reconnect logic or latency becomes a problem

### 8.5 CRDT Collaboration (Yjs / Automerge)
```javascript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const ydoc = new Y.Doc();
const ytext = ydoc.getText('shared-doc');
const provider = new WebsocketProvider('wss://server', 'room-1', ydoc);

ytext.insert(0, 'Hello');   // merges conflict-free across clients
// Awareness: cursors, selections, presence via provider.awareness
```
- **CRDT guarantees:** concurrent edits merge without conflicts; undo is per-user
- **Awareness protocol:** live presence (who's online, where their cursor is)
- **Sync:** initial state exchange → update messages; sequence tracking prevents loss
- Use for: collaborative docs, whiteboards, shared code editing

### 8.6 Transactional Outbox + CDC
```
App writes business row + outbox row IN ONE TRANSACTION
  → CDC (Debezium / pgoutput) streams outbox changes
    → Kafka/queue → downstream services
      → consumer tracks sequence for exactly-once-ish processing
```
- ✅ Guarantees DB state and events stay consistent (no dual-write problem)
- ✅ Sequence tracking enables **rewind** (reprocess from offset N after a bug)
- ❌ Never write to DB and queue without outbox (dual-write loses messages)

### 8.7 High-Frequency Streams & Backpressure
- **Batch AI token streams** server-side (50-100ms flushes) — not one frame per token
- **Backpressure:** if consumer lags, buffer with drop-oldest or pause producer (never unbounded memory)
- **Serialization:** MessagePack/protobuf for 100Hz+ streams (JSON too heavy)
- **Multiplex:** many logical channels over one connection (topic subscribe)
- **Web Worker transport:** keep parsing off the main thread for UI responsiveness

---

## 9. Error Handling (معالجة الأخطاء)

### 9.1 HTTP Status Codes
| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Success |
| 201 | Created | Resource created |
| 204 | No Content | Success, no body |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate/conflict |
| 422 | Unprocessable | Semantic error |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server | Server error |
| 502 | Bad Gateway | Upstream error |
| 503 | Service Unavailable | Down/maintenance |

### 9.2 Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request contains invalid data",
    "details": [
      { "field": "email", "issue": "must be a valid email" },
      { "field": "age", "issue": "must be between 0 and 150" }
    ],
    "requestId": "abc-123-def"
  }
}
```

---

## 10. ASP.NET Core (specific)

### 10.1 Modern Patterns
```csharp
// Minimal API
app.MapGet("/users/{id}", async (int id, IUserService service) =>
{
    var user = await service.GetByIdAsync(id);
    return user is not null ? Results.Ok(user) : Results.NotFound();
});

// Result pattern
public record Result<T>(T? Value, Error? Error)
{
    public bool IsSuccess => Error is null;
    public static Result<T> Success(T value) => new(value, null);
    public static Result<T> Failure(Error error) => new(null, error);
}
```

### 10.2 Key Features
- Built-in DI, options pattern, logging
- ProblemDetails for errors
- OpenAPI (built-in in .NET 9+)
- Rate limiting middleware
- Output caching
- Health checks

---

### 10.3 App Model Selection & Platform Features
| Need | Use |
|------|-----|
| Interactive server UI | Blazor Server / Auto |
| SEO content pages | Razor Pages |
| API + rich controllers | MVC Controllers |
| Real-time push | SignalR (WebSocket fallback) |
| RPC between services | gRPC |
| Background work | `BackgroundService` / hosted services |
| Users & login | ASP.NET Core Identity (or external IdP) |

```csharp
// Program.cs composition (minimal hosting)
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(o => o.TokenValidationParameters = TokenParams);
builder.Services.AddSignalR();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddHealthChecks().AddDbContextCheck<AppDb>();

var app = builder.Build();
app.UseExceptionHandler("/error");
app.UseRateLimiter();                 // built-in rate limiting
app.MapHealthChecks("/health/ready"); // readiness vs /health/live (liveness)
app.MapControllers();
app.Run();
```
- **.NET 10 guidance:** annual LTS cadence — check breaking changes before upgrade; use `dotnet list package --outdated`

---

## 11. Validation (التحقق)

### 11.1 Zod (TypeScript)
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150),
  role: z.enum(['admin', 'user']).default('user'),
});

type User = z.infer<typeof UserSchema>;

// Validate
const result = UserSchema.safeParse(input);
if (!result.success) {
  const errors = result.error.flatten();
  throw new ValidationError(errors);
}
```

### 11.2 Pydantic (Python)
```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    
    @validator('name')
    def sanitize_name(cls, v):
        return v.strip()
```

---

### 11.3 Zod v4 Essentials (أساسيات Zod v4)
```typescript
import { z } from 'zod';

// v4 conveniences
const User = z.object({
  email: z.email(),                          // z.string().email() still works
  createdAt: z.iso.datetime(),               // ISO formats
  active: z.stringbool(),                    // "true"/"1" → boolean
  role: z.enum(['admin', 'user']).prefault('user'),
  age: z.coerce.number().int().min(0).max(150),
});

// Pipes & transforms
const EmailInput = z.pipe(z.trim().toLowerCase(), z.email());

// Discriminated unions (tagged)
const Event = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('key'), key: z.string() }),
]);

// JSON Schema export (for OpenAPI docs)
const schema = z.toJSONSchema(User, { target: 'draft-2020-12' });

// Type inference: which type do I need?
type Out = z.output<typeof User>;   // after transforms/defaults
type In  = z.input<typeof User>;    // before coercion/defaults
```
- **Error customization:** `.min(1, { message: 'اسم مطلوب' })` or `.catchMap()`
- **`zod/mini`:** tree-shakeable build for bundle-sensitive code
- **v4 notes:** `.strict()` → `z.strictObject()`; errors are `ZodError.issues[]`

---

## 12. MCP Server Development (تطوير خوادم MCP)

### 12.1 When to Build an MCP Server
- Exposing tools/resources to LLM clients (Claude Desktop, ChatGPT, custom agents)
- Wrapping an existing API as model-accessible tools
- Providing file/dataset access safely to agents

### 12.2 FastMCP (Python) — Fastest Path
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool
def search_users(query: str, limit: int = 10) -> list[dict]:
    """Search users by name or email. Returns matching user records."""
    return db.search(query, limit=limit)

@mcp.resource("config://app")
def app_config() -> dict:
    return {"version": "1.0", "env": "production"}

if __name__ == "__main__":
    mcp.run()  # stdio by default; HTTP/SSE also supported
```

### 12.3 TypeScript SDK
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);
// register tools with zod-validated input schemas
```

### 12.4 Design Rules
- ✅ **Naming:** prefix tools by domain (`search_*`, `create_*`) — descriptive, verb-first
- ✅ **Schemas:** every parameter typed with description (models read them)
- ✅ **Errors:** actionable messages ("provide `issue_id` from `list_issues`"), not stack traces
- ✅ **Context:** return compact results (models have limited context); paginate large data
- ✅ **Idempotency:** read tools pure; write tools safe to retry or clearly marked
- ✅ **Workflow:** spec (tool list + schemas) → build → refine with real model calls → ship
- ❌ Never expose credentials in tool outputs
- ❌ Never return megabytes of data in one tool call

### 12.5 Registration
```bash
# Claude Desktop / opencode config example
{
  "mcpServers": {
    "my-server": { "command": "python", "args": ["server.py"] }
  }
}
```

---

## Verification Checklist (قائمة التحقق)

- [ ] API follows REST conventions (or documented alternative)
- [ ] All endpoints have input validation
- [ ] Error responses follow standard format
- [ ] Authentication on protected endpoints
- [ ] Authorization checked server-side
- [ ] Database queries use parameterization
- [ ] Connection pooling configured
- [ ] Caching strategy defined and implemented
- [ ] Logging includes correlation IDs
- [ ] Secrets in environment variables
- [ ] Rate limiting on sensitive endpoints
- [ ] Health check endpoint exists
- [ ] API documentation (OpenAPI) is current
- [ ] Performance: p95 < 200ms
- [ ] Error handling covers all failure cases
- [ ] Graceful degradation (fallbacks)
- [ ] Graceful shutdown (drain connections)

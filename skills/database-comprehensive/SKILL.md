---
name: database-comprehensive
description: Complete database skill — schema design, PostgreSQL tuning, performance auditing, indexing, connection pooling, Supabase, Valkey/Redis caching, migrations, testing, and data integrity. Use for ANY database design, optimization, or management task.
---

# Database Comprehensive — Complete Skill

## Overview

**Single skill for all database work.** Merges `postgres-tuning`, `supabase`, `supabase-postgres-best-practices`, `valkey`, `project-database-design-modeler`, `project-database-performance-auditor`, and `project-database-test-engine`.

---

## 1. Schema Design (تصميم المخطط)

### 1.1 Design Process
```
1. Identify entities      → nouns in requirements
2. Define relationships   → one-to-one, one-to-many, many-to-many
3. Normalize              → 3NF baseline, denormalize deliberately
4. Add constraints        → NOT NULL, UNIQUE, CHECK, FK
5. Plan indexes           → based on query patterns
6. Audit fields           → created_at, updated_at, deleted_at
7. Estimate scale         → rows now, rows in 2 years
```

### 1.2 Table Template
```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) NOT NULL UNIQUE,
    name        VARCHAR(100) NOT NULL,
    role        VARCHAR(20) NOT NULL DEFAULT 'user'
                CHECK (role IN ('user', 'admin', 'editor')),
    is_active   BOOLEAN NOT NULL DEFAULT true,
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at  TIMESTAMPTZ  -- soft delete
);

-- Auto-update timestamp
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

### 1.3 Naming Conventions
- Tables: `plural`, `snake_case` (users, order_items)
- Columns: `snake_case` (created_at, is_active)
- Primary keys: `id` (UUID preferred over serial for distributed)
- Foreign keys: `{entity}_id` (user_id, product_id)
- Indexes: `idx_{table}_{columns}` (idx_users_email)
- Constraints: `chk_{table}_{rule}`, `uq_{table}_{column}`

### 1.4 UUID vs Serial
| | UUID v4 | BIGSERIAL | Snowflake |
|---|---|---|---|
| Distributed-safe | ✅ | ❌ | ✅ |
| Index performance | Good (after PG13) | Best | Good |
| Guessable | No | Yes | Partially |
| Size | 16 bytes | 8 bytes | 8 bytes |
| Recommendation | Default | Legacy / simple | High-scale |

---

## 2. PostgreSQL Performance Tuning

### 2.1 EXPLAIN ANALYZE Reading
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 42 ORDER BY created_at DESC LIMIT 20;

-- Look for:
-- ✅ Index Scan (uses index)
-- ❌ Seq Scan on large table (missing index)
-- ❌ Nested Loop on large table (should be Hash/Merge Join)
-- ❌ Sort without index (adds to time)
-- ⚠️ Rows estimated vs actual (big gap = stale statistics)
```

### 2.2 Index Types
```sql
-- B-tree (default, equality + range)
CREATE INDEX idx_users_email ON users(email);

-- Composite: column order matters (equality first, range last)
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Partial (smaller, faster for filtered queries)
CREATE INDEX idx_posts_published ON posts(created_at) WHERE status = 'published';

-- Covering (index-only scan, no table lookup)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);

-- GIN (JSONB, arrays, full-text)
CREATE INDEX idx_docs_tags ON documents USING GIN(tags);
CREATE INDEX idx_docs_body ON documents USING GIN(to_tsvector('english', body));

-- BRIN (very large tables, naturally ordered)
CREATE INDEX idx_events_time ON events USING BRIN(created_at);

-- Expression (function on column)
CREATE INDEX idx_users_lower_email ON users(lower(email));
```

### 2.3 When NOT to Index
- Small tables (seq scan is faster)
- Columns with low selectivity (boolean, few distinct values)
- Write-heavy tables (indexes slow down inserts/updates)
- Every column (only index what queries use)

### 2.4 Tuning Parameters
```ini
# postgresql.conf — starter values for web apps
shared_buffers = 25% of RAM          # e.g., 4GB for 16GB RAM
effective_cache_size = 75% of RAM
work_mem = 64MB                       # per-sort/hash operation
maintenance_work_mem = 512MB          # for VACUUM, CREATE INDEX
max_connections = 100                 # use PgBouncer for more
random_page_cost = 1.1                # SSD storage
effective_io_concurrency = 200        # SSD
```

### 2.5 Vacuum & Maintenance
```sql
-- Auto-vacuum tuning (per table if needed)
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.01,  -- vacuum at 1% churn
    autovacuum_analyze_scale_factor = 0.005
);

-- Manual vacuum for heavy updates
VACUUM (ANALYZE, VERBOSE) orders;

-- Reindex when bloated
REINDEX INDEX CONCURRENTLY idx_orders_user_created;
```

### 2.6 PostgreSQL 17/18 Modern Features (ميزات حديثة)

**Async I/O (PG17+):** `io_uring` on Linux dramatically speeds scans/backups.
```sql
-- Enable AIO (PG17+)
shared_preload_libraries = 'pg_aios'   -- or built-in async I/O in PG18
```

**UUIDv7 (PG18):** time-ordered IDs — B-tree friendly, no index bloat.
```sql
SELECT uuidv7();                    -- PG18 built-in
-- PG17: uuid_generate_v7() via pgcrypto/uuid-ossp extensions
```

**B-tree skip scan (PG18):** `WHERE created > x` on multi-column index `(user_id, created)` no longer needs a full index scan.

**Vector search (pgvector HNSW tuning):**
```sql
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);   -- higher m/ef = recall vs speed
SET hnsw.ef_search = 100;               -- per-query recall knob
```

**Observability:**
```sql
SELECT * FROM pg_stat_io;           -- I/O by backend type (PG14+, richer in 17)
SELECT * FROM pg_stat_checkpointer; -- PG17 checkpoint behavior
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, WAL) SELECT ...;
```
**Targets:** Shared Hit Ratio > 95%, checkpoint spreading over `checkpoint_timeout`, low `Buffers Written by Backends` ratio.

---

## 3. Query Optimization (تحسين الاستعلامات)

### 3.1 N+1 Queries
```sql
-- ❌ N+1: 1 query for orders + N queries for users
SELECT * FROM orders;
SELECT * FROM users WHERE id = ?;  -- per order

-- ✅ JOIN
SELECT o.*, u.name, u.email
FROM orders o JOIN users u ON u.id = o.user_id
WHERE o.user_id = 42;

-- ✅ Batch loading (IN clause)
SELECT * FROM users WHERE id IN (1, 5, 9, ...);
```

### 3.2 Pagination
```sql
-- ✅ Cursor-based (fast on large tables)
SELECT * FROM events
WHERE created_at < $cursor
ORDER BY created_at DESC
LIMIT 20;

-- ❌ Offset-based (slow on deep pages)
SELECT * FROM events ORDER BY created_at DESC OFFSET 10000 LIMIT 20;
```

### 3.3 Connection Pooling (PgBouncer)
```ini
; pgbouncer.ini
[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
pool_mode = transaction        # transaction pooling (default)
max_client_conn = 1000
default_pool_size = 25
```

---

## 4. Supabase (ساباس)

### 4.1 Key Features
| Feature | Use |
|---------|-----|
| Postgres database | Full PostgreSQL 15+ |
| Auth | Built-in authentication |
| Realtime | Postgres changes over WebSocket |
| Storage | File storage with CDN |
| Edge Functions | Deno serverless functions |
| Vector | pgvector for AI embeddings |

### 4.2 Row Level Security (RLS)
```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: users see only their own profile
CREATE POLICY "users_read_own" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "users_update_own" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Policy: public read, authenticated write
CREATE POLICY "posts_public_read" ON posts
    FOR SELECT USING (status = 'published');

CREATE POLICY "posts_auth_write" ON posts
    FOR INSERT WITH CHECK (auth.uid() = author_id);
```

### 4.3 Best Practices
- Always enable RLS on user-facing tables
- Test policies with different roles (anon, authenticated)
- Use `auth.uid()` for ownership checks
- Prefer views with SECURITY DEFINER for complex queries

### 4.4 Supabase Security Traps (فخاخ شائعة)

**⚠️ `user_metadata` vs `app_metadata` — the JWT trap:**
```
user_metadata  → USER-EDITABLE (via updateUser) → NEVER trust in policies
app_metadata   → SERVER-ONLY (via admin API)   → safe for roles/permissions
```
A user can set `user_metadata: { role: "admin" }` themselves. Only trust `app_metadata` or custom JWT claims for authorization.

**⚠️ `service_role` key:** bypasses ALL RLS. Rules:
- Server-only, never in client bundle, never in git/logs
- Rotate on any suspected leak
- Prefer per-user JWT + RLS over service_role in app code

**⚠️ Views and RLS:** Postgres views execute with the *view owner's* rights — RLS on the underlying table is bypassed. Fix:
```sql
CREATE VIEW admin_users WITH (security_invoker = true) AS
  SELECT * FROM profiles WHERE role = 'admin';
```
`security_invoker = true` makes the view run as the querying user.

**⚠️ Data API (PostgREST) exposure:**
- `GRANT SELECT` on a table = exposed via REST API automatically
- Revoke public schemas you don't want exposed: `REVOKE USAGE ON SCHEMA private FROM anon, authenticated;`
- Check the auto-generated OpenAPI in Studio before shipping

**Clients:** use `@supabase/ssr` for server/browser cookie-based auth; `supabase-js` for pure client. Enable only the Postgres extensions you need (`pgvector`, `pg_trgm`, `uuid-ossp`).

**Changelog-verification-first:** before relying on any Supabase behavior, verify it against the current changelog — features/defaults change frequently.

---

## 5. Valkey / Redis (التخزين المؤقت)

### 5.1 Data Structures
| Type | Use Case | Command |
|------|----------|---------|
| String | Cache, counters, tokens | GET/SET/INCR |
| Hash | Objects (user profile) | HGET/HSET |
| List | Queues, feeds | LPUSH/BRPOP |
| Set | Unique tags, dedup | SADD/SMEMBERS |
| Sorted set | Leaderboards, rate limits | ZADD/ZRANGE |
| Stream | Event logs, consumer groups | XADD/XREADGROUP |

### 5.2 Cache Pattern
```python
def get_user(user_id):
    # 1. Check cache
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # 2. Fetch from DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)

    # 3. Populate cache with TTL
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

def update_user(user_id, data):
    db.update(...)
    redis.delete(f"user:{user_id}")  # Invalidate
```

### 5.3 Rate Limiting (Fixed Window)
```python
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate:{user_id}:{int(time.time() // window)}"
    current = redis.incr(key)
    if current == 1:
        redis.expire(key, window)
    return current > limit
```

**Sliding window (sorted set):**
```python
def allow(user_id, limit=100, window=60):
    now = time.time()
    key = f"rl:{user_id}"
    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)  # prune old hits
    pipe.zadd(key, {f"{now}": now})
    pipe.zcard(key)
    pipe.expire(key, window)
    _, _, count, _ = pipe.execute()
    return count <= limit
```

### 5.4 Distributed Locks (أوزان موزعة)
```python
# Acquire: atomic SET NX PX (never SET + EXPIRE separately — crash = immortal lock)
lock = redis.set("lock:job:42", token, nx=True, px=5000)

# Release: compare-and-delete (only delete YOUR lock)
def release(redis, key, token):
    lua = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
    end
    return 0
    """
    redis.eval(lua, 1, key, token)
```
- ✅ Use Redlock (multiple nodes) for multi-instance safety-critical locks
- ✅ Renew with a heartbeat task if work > lock TTL
- ❌ Never use `SET` then `EXPIRE` (non-atomic)

### 5.5 Queues & Consumer Groups
```python
# Simple queue
redis.lpush("queue:emails", payload)
job = redis.brpop("queue:emails", timeout=5)     # blocking pop

# Reliable queue (consumer groups — survives worker crash)
redis.xadd("events", {"data": payload})
redis.xgroup_create("events", "workers", mkstream=True)
msg = redis.xreadgroup("workers", "worker-1", {"events": ">"}, count=1)
redis.xack("events", "workers", msg_id)          # mark processed
```

### 5.6 Operations & Persistence (التشغيل والثبات)
| Topic | Rule |
|-------|------|
| **Eviction** | `maxmemory-policy allkeys-lru` for cache; `noeviction` for durable data; `volatile-lru` if only TTL'd keys should be evicted |
| **Persistence** | RDB (fast snapshots) + AOF (`appendfsync everysec`) — AOF = at most 1s data loss |
| **Migration** | Valkey is Redis-compatible; migrate via `redis-cli --rdb` / `MIGRATE`; watch for removed Redis-proprietary modules |
| **KEYS \*** | ❌ **Never in production** — O(N) blocks the server. Use `SCAN` with COUNT instead |
| **HyperLogLog** | `PFADD` / `PFCOUNT` — count unique visitors in ~12KB regardless of cardinality |

---

## 6. Testing (اختبار قواعد البيانات)

### 6.1 Test Strategy
```python
# Isolated test DB per test session
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)      # fresh schema
    yield engine
    Base.metadata.drop_all(engine)        # cleanup

@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    transaction.rollback()                # isolation per test
    session.close()
```

### 6.2 What to Test
- Constraints: insert invalid data, expect rejection
- Migrations: up + down, verify data preserved
- Repository queries: return expected rows
- Transactions: rollback on error
- Authorization: role-based query filtering

---

## 7. Migration Safety (سلامة الترحيل)

### 7.1 Rules
- ✅ Backward compatible (old code + new schema coexist)
- ✅ Additive first (add column/table, then backfill)
- ✅ Test on production-size data copy
- ✅ Have a rollback plan
- ❌ Never modify/drop columns used by running code
- ❌ Never run destructive migration without backup

### 7.2 Expand-Contract Pattern
```
1. EXPAND    → add new column (nullable)
2. MIGRATE   → backfill data in background
3. VERIFY    → check consistency
4. CONTRACT  → switch reads to new column, then drop old
```

---

## Verification Checklist (قائمة التحقق)

- [ ] Schema normalized (or denormalization justified)
- [ ] All foreign keys have indexes
- [ ] Composite indexes match query patterns (column order correct)
- [ ] No N+1 queries (check logs for repeated similar queries)
- [ ] EXPLAIN ANALYZE shows Index Scans on hot queries
- [ ] Connection pooling configured (PgBouncer or equivalent)
- [ ] RLS enabled on user-facing tables (Supabase)
- [ ] Cache invalidation strategy defined
- [ ] Migrations tested with production-size data
- [ ] Rollback plan documented for each migration
- [ ] Backup automation verified (not just configured)
- [ ] Slow query log enabled and reviewed
- [ ] Autovacuum running (check pg_stat_user_tables)

---

## Related Skills

- `$backend-comprehensive` — for API layer that uses this database
- `$security-comprehensive` — for data encryption and access control
- `$testing-comprehensive` — for database test automation
- `$devops-comprehensive` — for database migrations in CI/CD
- `$repair-stability` — for fixing performance regressions

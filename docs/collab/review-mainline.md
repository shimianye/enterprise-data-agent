# Mainline Review

Scope: `app/db/sqlite.py`, `app/catalog`, `app/metrics`, `app/llm`, `app/agent/query_service.py`, and `app/api/app.py`. Read-only review; no production code changes made.

## Findings

### [P1] Relevant-table retrieval can omit the tables required by the generated SQL

`SchemaCatalog.relevant()` defaults to six tables and scores literal substring matches in English table/column names and short Chinese descriptions (`app/catalog/schema.py:65-72`). `QueryService` passes the entire Chinese question plus metric display names (`app/agent/query_service.py:28-30`). For questions such as “2026 年 8 月的总销售额”, none of the catalog text necessarily contains “销售额”, so ties are resolved alphabetically; `orders` can be absent from the LLM context. This is masked by `MockLLMClient`, which ignores `context`, but will cause a real Text2SQL model to hallucinate or fail. Include metric.table dependencies (and join-related tables), add Chinese aliases/keywords to the catalog, or always include a schema baseline containing the metric's source table.

### [P1] Database errors become an unhandled 500 and bypass the declared API error contract

`QueryService.query()` executes validated SQL without translating `sqlite3.Error` (`app/agent/query_service.py:31-35`). The API catches only `SQLValidationError`, `ValueError`, and `FileNotFoundError` (`app/api/app.py:23-27`). A valid-but-broken SQL query therefore returns FastAPI's generic 500 instead of the documented `db_error` response, and there is no recovery path. Catch `sqlite3.Error` at the API/service boundary, avoid returning raw SQL error details, and expose a stable error code.

### [P2] Health endpoint probes the database twice per request

`health()` calls `db.health()` independently for `status` and `db` (`app/api/app.py:21-22`). This opens two connections and can report inconsistent values during a transient failure. Store one probe result and derive both fields from it. The endpoint also reports no LLM status despite the interface contract describing it.

### [P2] Glossary filters are not included in prompt context

`MetricsGlossary.prompt_context()` emits only expression and description (`app/metrics/glossary.py:20-21`); the authoritative `filters` tuple (for example `orders.paid_amount > 0`) is omitted. The description hints at paid orders but does not provide a machine-usable predicate, making generated SQL vulnerable to the exact sales口径 drift already corrected in the eval set. Include filters explicitly in the context and test that sales prompts contain `paid_amount > 0`.

### [P2] Mock LLM is intentionally non-production and exact-string brittle

`MockLLMClient` maps exact question strings to `golden_sql` and raises `ValueError` for every unseen question (`app/llm/client.py:7-14`). This is suitable for deterministic tests, but the default API factory wires it unconditionally (`app/api/app.py:14-18`), so the running service cannot answer any new user question and has no real provider configuration. Keep mock mode explicit (for tests/eval), and fail startup or return a clear `llm_unavailable` status when no provider is configured.

### [P2] Read-only enforcement is connection-local and the low-level execute method is broader than its callers

`PRAGMA query_only = ON` is correctly set on every connection (`app/db/sqlite.py:15-18`) and protects the main database from ordinary writes. However, `SQLiteDatabase.execute()` is public and accepts arbitrary SQL; callers outside the validated QueryService could issue PRAGMA/temporary-schema operations. Keep the validator mandatory at every user-controlled entry point and consider a narrowly scoped metadata/query API for catalog access.

### [P3] Catalog metadata is cached indefinitely

`SchemaCatalog` caches `_tables` after first access (`app/catalog/schema.py:32,56-60`). This is fine for an immutable generated database, but a rebuilt or migrated `enterprise.db` in a long-running process will leave stale schema until `refresh()` is called manually. Invoke refresh on startup or document the lifecycle requirement.

## Positive checks

- Validator integration uses `catalog.to_table_infos()` and executes `safety.normalized_sql`, preserving LIMIT injection and rejecting unsafe SQL.
- `query_only` is enabled before any query and `row_factory` produces JSON-friendly dictionaries.
- Table descriptions distinguish `refunds` (funds) from `after_sales` (service), and glossary table assignments match that split.
- The 20 formal cases use SQLite `strftime`, `promotion_name`, and the authoritative `paid_amount > 0` sales filter; `MockLLMClient` loads the `question`/`golden_sql` shape correctly.

## eval/run_eval.py recommendation

Implement a CLI that loads `eval/cases.jsonl`, executes each `golden_sql` through `check_sql_safety` and `SQLiteDatabase`, then sends each question through `QueryService`. Record per-case: safety result, executable flag, normalized SQL, row count/shape, result equality against the golden query, matched metric keys, latency, and error code. Aggregate the six documented metrics (SQL executable, result correct, shape correct, safety interception, metric correctness, and end-to-end success) and emit both a human-readable table and JSON artifact. Use a deterministic database path/seed and compare rows by column names with numeric tolerance for aggregates.

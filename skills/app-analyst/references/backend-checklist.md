# Backend Audit Checklist

Use this checklist when performing the backend audit phase. Focus on findings
that have real impact — skip items that are clearly not relevant to the app's
stage or architecture.

## API Design

- [ ] Consistent URL naming convention (kebab-case, plural nouns)
- [ ] Appropriate HTTP methods (GET for reads, POST for creates, etc.)
- [ ] Consistent response envelope (same shape for success/error across endpoints)
- [ ] Proper HTTP status codes (not 200 for everything)
- [ ] Input validation on all endpoints (type checking, bounds, required fields)
- [ ] Pagination on list endpoints
- [ ] Request size limits configured
- [ ] API versioning strategy (path prefix, header, etc.)

## Security

- [ ] CORS policy restricts origins appropriately (not wildcard in production)
- [ ] Authentication on sensitive endpoints (admin, write operations)
- [ ] Authorization checks (can this user do this action?)
- [ ] Input sanitization (SQL injection, XSS via stored data)
- [ ] Rate limiting on public endpoints
- [ ] Secrets not hardcoded (use environment variables)
- [ ] .env files gitignored
- [ ] Webhook signature verification (Stripe, GitHub, etc.)
- [ ] No sensitive data in URL parameters (use headers or body)
- [ ] HTTPS enforced in production

## Architecture

- [ ] Clear separation of concerns (routes, business logic, data access)
- [ ] Error handling at appropriate layers (not swallowed silently)
- [ ] Dependency injection or clear configuration management
- [ ] Database sessions managed properly (no leaks, proper cleanup)
- [ ] Async operations handled correctly (no fire-and-forget without error handling)
- [ ] Logging at appropriate levels (not excessive, not silent)
- [ ] Configuration from environment (not hardcoded values)

## Performance

- [ ] Database queries efficient (no N+1, appropriate indexes)
- [ ] Connection pooling configured for database
- [ ] Caching strategy where beneficial (Redis, in-memory, HTTP cache headers)
- [ ] Long-running operations have timeouts
- [ ] External API calls have timeouts and retry logic
- [ ] Batch operations where possible (not individual DB calls in loops)
- [ ] Response payload size reasonable (not sending entire DB)

## Data Integrity

- [ ] Model constraints match business rules (unique, not null, foreign keys)
- [ ] Database migrations versioned and reproducible
- [ ] Relationships defined correctly (cascade behavior)
- [ ] Data validation at model level (not just API level)
- [ ] Concurrent access handled (optimistic locking, transactions)
- [ ] Audit trail for important state changes

## Error Handling

- [ ] Errors return useful messages to clients (not stack traces)
- [ ] Internal errors logged with context for debugging
- [ ] External service failures handled gracefully (fallbacks, retries)
- [ ] Validation errors return specific field-level messages
- [ ] Unhandled exception handler configured (500 errors have a response shape)
- [ ] Timeout errors distinguished from other failures

## Testing & Observability

- [ ] Critical paths have test coverage
- [ ] Health check endpoint exists and checks dependencies
- [ ] Structured logging in place
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Performance monitoring for slow endpoints

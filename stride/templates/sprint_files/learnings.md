# Project Learnings

This file captures accumulated knowledge from completed sprints. Agents read this before planning and implementation to apply patterns and avoid anti-patterns.

---

## Domain Knowledge

### {Domain Name (e.g., Authentication, Payment, Analytics)}
- [YYYY-MM-DD] {[DONE] Pattern | [FAILED] Anti-pattern} (sprint-{sprint-name}): {Learning content}
  **Context:** {Why this matters, what problem it solves/causes}
  **Applied in:** {Where this pattern is used or should be used}

**Example:**
### Authentication
- [2025-01-20] [DONE] (sprint-oauth): OAuth state must be crypto-random, not timestamp-based
  **Context:** Prevents CSRF attacks; timestamp patterns are predictable
  **Applied in:** OAuth callback handler, session initialization

- [2025-01-15] [FAILED] (sprint-user-profile): Don't store user preferences in JWT claims
  **Context:** Causes stale data when preferences change; use database instead
  **Impact:** Required token refresh logic to be redesigned

---

## Technical Patterns

### {Technical Area (e.g., Database, API Design, Error Handling)}
- [YYYY-MM-DD] {[DONE] Pattern | [FAILED] Anti-pattern} (sprint-{sprint-name}): {Pattern description}
  **Context:** {Why this pattern works or fails}
  **Pattern Code:** (optional)
  ```{language}
  {code example}
  ```

**Example:**
### Database
- [2025-01-18] [DONE] (sprint-db-perf): Always use connection pooling for DB queries
  **Context:** Reduces connection overhead by 80%, improves response time
  **Pattern Code:**
  ```typescript
  const pool = new Pool({ max: 20, idleTimeout: 30000 });
  export const query = (text, params) => pool.query(text, params);
  ```

- [2025-02-01] [FAILED] (sprint-analytics): Avoid N+1 queries in list endpoints
  **Context:** Caused 500ms+ response times for list of 50 items
  **Solution:** Use JOINs or DataLoader pattern for batching

### Error Handling
- [2025-01-22] [DONE] (sprint-api-refactor): Centralized error handling middleware pattern
  **Context:** Ensures consistent error responses, logging, and monitoring
  **Pattern Code:**
  ```typescript
  app.use((err, req, res, next) => {
    logger.error(err);
    res.status(err.status || 500).json({ error: err.message });
  });
  ```

---

## Architecture Decisions

### {Architecture Topic (e.g., API Design, Microservices, State Management)}
- [YYYY-MM-DD] {[DONE] Pattern} (sprint-{sprint-name}): {Decision description}
  **Context:** {Reasoning, tradeoffs, alternatives considered}
  **Impact:** {How this affects future development}

**Example:**
### API Design
- [2025-01-25] [DONE] (sprint-api-v2): Version APIs via URL path (/v1/, /v2/), not headers
  **Context:** Easier to test, document, and cache; clear deprecation path
  **Impact:** All new endpoints must follow /api/v{N}/ pattern

---

## Performance Insights

### {Performance Area (e.g., Caching, Query Optimization, Frontend)}
- [YYYY-MM-DD] {[DONE] Pattern} (sprint-{sprint-name}): {Optimization insight}
  **Context:** {Measured impact, benchmark results}
  **Implementation:** {How to apply this optimization}

**Example:**
### Caching
- [2025-02-05] [DONE] (sprint-perf-opt): Cache frequently accessed, rarely changing data at app level
  **Context:** Reduced DB load by 60% for user metadata lookups
  **Implementation:** In-memory LRU cache with 5min TTL

---

## Security Learnings

### {Security Domain (e.g., Input Validation, Authentication, Authorization)}
- [YYYY-MM-DD] {[DONE] Pattern | [FAILED] Anti-pattern} (sprint-{sprint-name}): {Security learning}
  **Context:** {Threat model, vulnerability type, mitigation}
  **Applied to:** {Affected components}

**Example:**
### Input Validation
- [2025-01-28] [FAILED] (sprint-xss-fix): Never trust client-side validation alone
  **Context:** XSS vulnerability from unsanitized user input in comments
  **Solution:** Server-side validation + sanitization using DOMPurify

### Authentication
- [2025-02-03] [DONE] (sprint-security): Implement rate limiting on auth endpoints
  **Context:** Prevents brute force attacks; 5 attempts per 15min window
  **Applied to:** /login, /reset-password, /verify-otp

---

## Testing Strategies

### {Testing Type (e.g., Unit Tests, Integration Tests, E2E)}
- [YYYY-MM-DD] {[DONE] Pattern | [FAILED] Anti-pattern} (sprint-{sprint-name}): {Testing insight}
  **Context:** {Why this testing approach works/fails}
  **Examples:** {Test scenarios or patterns}

**Example:**
### Unit Tests
- [2025-01-30] [DONE] (sprint-test-infra): Test edge cases explicitly, not just happy path
  **Context:** Caught 8 bugs in production from boundary conditions
  **Examples:** null/undefined inputs, empty arrays, max integer values

### Integration Tests
- [2025-02-02] [DONE] (sprint-api-testing): Use test database with seeded data, not mocks
  **Context:** Catches SQL errors, constraint violations missed by mocks
  **Setup:** Docker Compose with test DB container

---

## Statistics
- **Total Learnings:** {count}
- **Positive Patterns:** {count}
- **Anti-Patterns:** {count}
- **Most Referenced Category:** {category}
- **Last Updated:** {YYYY-MM-DD}

---

## Agent Usage Instructions

### When to Read Learnings
1. **Before Planning (`/stride:plan`):** Read relevant domain learnings to inform sprint design
2. **Before Implementation (`/stride:implement`):** Load learnings for modules being modified
3. **During Feedback (`/stride:feedback`):** Check for anti-pattern violations in proposed changes
4. **During Review (`/stride:review`):** Validate implementation follows positive patterns

### How to Apply Learnings
1. Search by domain/category relevant to current task
2. Check anti-patterns before making changes
3. Reference positive patterns in implementation decisions
4. Document when learnings are applied in implementation logs

### When to Add Learnings
1. **During Feedback (`/stride:feedback`):** When mid-sprint changes reveal new insights
2. **During Completion (`/stride:complete`):** Extract learnings from retrospective
3. **Format:** Follow category/subcategory structure above
4. **Include:** Date, sprint reference, context, and impact

### Learning Categorization
- **Domain Knowledge:** Business rules, entities, workflows
- **Technical Patterns:** Reusable code patterns, architectures, tools
- **Architecture Decisions:** System-level choices affecting structure
- **Performance Insights:** Optimizations with measured impact
- **Security Learnings:** Vulnerabilities, mitigations, best practices
- **Testing Strategies:** Effective testing approaches and patterns

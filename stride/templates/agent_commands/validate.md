---
description: Run comprehensive quality gates before sprint completion with validation report.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Guardrails**
- `/stride:validate` runs **before `/stride:complete`** to ensure quality standards.
- Executes comprehensive validation based on project type and configuration.
- Must generate a structured validation report with Pass/Fail/Upcoming status.
- Does **NOT modify code** - only validates existing implementation.
- Validates against active sprint's acceptance criteria and implementation.
- Must check for common issues: failing tests, linting errors, type errors, secrets in code.
- Provides actionable recommendations for fixing issues.

---

**Steps**

1. **Validate Sprint Context**
   - Check if `.stride/project.md` exists.
   - If missing → stop and suggest: "Run `/stride:init` to initialize the project first."
   - Identify the currently ACTIVE sprint (has `implementation.md` but no `retrospective.md`).
   - If no active sprint → stop and say: "No active sprint found. Start a sprint with `/stride:plan` first."
   - Read `plan.md` to understand strides and tasks.
   - Read `implementation.md` to see what has been implemented.

2. **Detect Project Type & Configuration**
   Analyze the project to determine what validation tools to use:

   **a) Detect Language & Framework**:
   - Scan for:
     - `package.json` → Node.js/TypeScript project
     - `requirements.txt` or `pyproject.toml` → Python project
     - `pom.xml` or `build.gradle` → Java project
     - `Cargo.toml` → Rust project
     - `go.mod` → Go project
     - `.csproj` → C# project

   **b) Detect Available Tools**:
   Check which validation tools are configured:
   - **Linting**: ESLint, Pylint, Flake8, Clippy, golangci-lint, etc.
   - **Type Checking**: TypeScript, mypy, Flow, etc.
   - **Testing**: Jest, pytest, JUnit, Cargo test, Go test, etc.
   - **Security**: detect-secrets, Gitleaks, trufflehog, npm audit, etc.
   - **Formatting**: Prettier, Black, rustfmt, gofmt, etc.

   **c) Read Configuration Files**:
   - Check for config files: `.eslintrc`, `pytest.ini`, `mypy.ini`, `tsconfig.json`, etc.
   - Read test commands from `package.json` scripts, `Makefile`, or CI config.

3. **Define Validation Categories**

   Based on project type, create validation checklist:

   **Category 1: Type Checking** (if applicable)
   ```
   IF TypeScript project:
       Run: npx tsc --noEmit
   ELSE IF Python with mypy:
       Run: mypy <source_dir>
   ELSE IF typed language:
       Run appropriate type checker
   ```

   **Category 2: Linting**
   ```
   IF ESLint configured:
       Run: npx eslint .
   ELSE IF Pylint/Flake8:
       Run: pylint <source> OR flake8 <source>
   ELSE IF Clippy (Rust):
       Run: cargo clippy
   ELSE IF golangci-lint:
       Run: golangci-lint run
   ```

   **Category 3: Tests**
   ```
   IF package.json has "test" script:
       Run: npm test
   ELSE IF pytest configured:
       Run: pytest
   ELSE IF Cargo.toml exists:
       Run: cargo test
   ELSE IF Go project:
       Run: go test ./...
   ELSE:
       Check for test files and suggest how to run tests
   ```

   **Category 4: Security Scanning**
   ```
   ALWAYS:
       Run secret detection (detect-secrets, gitleaks, or manual scan)
       Check for hardcoded passwords, API keys, tokens
       Look for patterns: API_KEY=, password=, token=, secret=

   IF Node.js:
       Run: npm audit (check for vulnerable dependencies)

   IF Python:
       Run: pip-audit OR safety check
   ```

   **Category 5: Code Formatting** (optional, warnings only)
   ```
   IF Prettier configured:
       Run: npx prettier --check .
   ELSE IF Black configured:
       Run: black --check .
   ELSE IF rustfmt:
       Run: cargo fmt --check
   ```

4. **Execute Validation Checks**

   For each validation category:

   **a) Run the Check**:
   - Execute the command (e.g., `npm test`, `mypy .`, `eslint .`)
   - Capture stdout, stderr, and exit code
   - Parse output for errors, warnings, and passes

   **b) Classify Results**:
   - **PASS**: Exit code 0, no errors
   - **FAIL**: Exit code != 0, or errors found
   - **UPCOMING**: Will be fixed in future strides (explained below)
   - **SKIP**: Tool not available or not applicable

   **c) Extract Issues**:
   - Parse error messages
   - Extract file paths and line numbers
   - Categorize by severity (critical, error, warning, info)

5. **Analyze Against Sprint Plan**

   Compare validation failures with sprint strides:

   **Rule 1: Upcoming Fixes**
   ```
   FOR each validation failure:
       Check if corresponding fix is mentioned in upcoming strides

       Example:
       - Failure: "Type error in auth.ts:42"
       - Check plan.md for future strides like:
         "Stride 4: Add TypeScript types for authentication"

       IF match found:
           Mark as "UPCOMING - Will be fixed in Stride 4"
       ELSE:
           Mark as "FAIL - Must fix before completion"
   ```

   **Rule 2: Completed vs Pending**
   ```
   FOR each failed test:
       Check if test is for implemented strides or future strides

       IF test is for completed stride:
           Mark as "FAIL - Critical issue"
       ELSE IF test is for upcoming stride:
           Mark as "UPCOMING - Expected to pass after Stride N"
   ```

6. **Generate Validation Report**

   Create a structured report with three status levels:

   **Report Structure**:
   ```markdown
   # Validation Report

   Sprint: {sprint_id}
   Date: {timestamp}
   Status: {PASS / FAIL / PARTIAL}

   ## Summary
   - ✅ PASS: {count} checks
   - ❌ FAIL: {count} checks
   - 🔜 UPCOMING: {count} checks (will be fixed)
   - ⏭️  SKIP: {count} checks (not applicable)

   ---

   ## 1. Type Checking
   Status: {PASS/FAIL/UPCOMING}

   Command: `tsc --noEmit`
   Result: {summary}

   Issues:
   - ❌ src/auth.ts:42 - Type 'string' is not assignable to type 'number'
   - 🔜 src/api.ts:15 - Missing return type (fixed in Stride 4)

   ---

   ## 2. Linting
   Status: {PASS/FAIL}

   Command: `eslint .`
   Result: {summary}

   Issues:
   - ❌ src/utils.ts:8 - Unused variable 'result'
   - ❌ src/config.ts:22 - Prefer const over let

   ---

   ## 3. Tests
   Status: {FAIL}

   Command: `npm test`
   Result: 8 passed, 2 failed

   Failed Tests:
   - ❌ auth.test.ts - "should validate JWT tokens" (critical - blocking)
   - 🔜 api.test.ts - "should handle rate limiting" (Stride 5 implementation)

   ---

   ## 4. Security Scan
   Status: {PASS/FAIL}

   Secrets Detection: {PASS/FAIL}
   Dependency Audit: {PASS/FAIL}

   Issues:
   - ❌ CRITICAL: API key found in src/config.ts:12
   - ⚠️  Warning: 2 moderate vulnerabilities in dependencies

   ---

   ## Recommendations

   ### Critical (Must Fix Before Completion)
   1. Remove hardcoded API key from src/config.ts - use environment variables
   2. Fix failing test: auth.test.ts - JWT validation
   3. Fix type error in src/auth.ts:42

   ### Fix Now (Blocking Issues)
   1. Remove unused variable in src/utils.ts:8
   2. Update dependencies with vulnerabilities

   ### Can Wait (Upcoming Strides)
   1. Type annotations in src/api.ts - scheduled for Stride 4
   2. Rate limiting tests - scheduled for Stride 5

   ### Optional (Warnings)
   1. Consider using const instead of let (linting warning)
   2. Add missing JSDoc comments

   ---

   ## Overall Status

   ❌ **VALIDATION FAILED**

   You have 3 critical issues that must be resolved before running `/stride:complete`:
   1. Hardcoded API key (security)
   2. Failing authentication test (functionality)
   3. Type error in authentication (correctness)

   2 issues are scheduled for upcoming strides and can be deferred.

   Next Steps:
   1. Fix the 3 critical issues above
   2. Re-run `/stride:validate` to verify
   3. Once all critical issues pass, proceed with `/stride:complete`
   ```

7. **Classify Validation Status**

   Determine overall validation status:

   ```
   IF critical_failures > 0 OR security_issues > 0:
       status = "FAIL - Cannot complete sprint"
       message = "Fix {count} critical issue(s) before completion"

   ELSE IF test_failures > 0 (excluding upcoming):
       status = "FAIL - Tests must pass"
       message = "Fix {count} failing test(s)"

   ELSE IF blocking_errors > 0 (type errors, linting errors):
       status = "PARTIAL - Non-critical issues found"
       message = "Consider fixing {count} issue(s) or document why skipped"

   ELSE:
       status = "PASS - Ready for completion"
       message = "All validation checks passed! ✅"
   ```

8. **Present Results**

   Display the validation report in a clear, actionable format:

   **Success Case**:
   ```
   ✅ Validation Passed!

   All checks completed successfully:
   - ✅ Type Checking: No errors
   - ✅ Linting: Clean code
   - ✅ Tests: 15/15 passed
   - ✅ Security: No secrets or vulnerabilities

   Your sprint is ready for `/stride:complete`! 🎉
   ```

   **Failure Case**:
   ```
   ❌ Validation Failed

   Critical Issues (must fix):
   1. [SECURITY] Hardcoded API key in src/config.ts:12
   2. [TESTS] Failing: auth.test.ts - JWT validation
   3. [TYPE] Type error in src/auth.ts:42

   Upcoming (will be fixed in future strides):
   1. [TYPE] Missing return types (Stride 4)
   2. [TESTS] Rate limiting tests (Stride 5)

   Fix the 3 critical issues, then re-run `/stride:validate`.
   ```

---

**When to Trigger**

The command MUST trigger when the user says:
- "Run validation"
- "Validate the sprint"
- "Check quality gates"
- "Run tests and checks"
- "Am I ready to complete?"
- "Validate before completion"
- "Check if sprint is done"

---

**When NOT to Trigger**

- During active implementation (wait until ready to complete)
- When no sprint is active
- For validating sprint document structure (use CLI `stride validate` instead)
- During planning phase

---

**Output Example**

```
Validation Report - SPRINT-A3F2E
Generated: 2024-01-15 14:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

- ✅ PASS: 3 checks
- ❌ FAIL: 2 checks
- 🔜 UPCOMING: 2 checks
- ⏭️  SKIP: 1 check

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. Type Checking
Status: ✅ PASS

Command: `npx tsc --noEmit`
Result: No type errors found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 2. Linting
Status: ✅ PASS

Command: `npx eslint .`
Result: 0 errors, 2 warnings

Warnings:
- ⚠️  src/utils.ts:45 - Prefer const over let

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3. Tests
Status: ❌ FAIL

Command: `npm test`
Result: 12 passed, 1 failed

Failed Tests:
- ❌ auth.test.ts - "should validate JWT tokens"
     Expected: valid token
     Received: undefined
     Location: tests/auth.test.ts:42

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 4. Security Scan
Status: ❌ FAIL

Secrets Detection: FAIL
Dependency Audit: PASS

Issues:
- ❌ CRITICAL: Possible API key at src/config.ts:12
     Pattern: "API_KEY = 'sk-...'"
     Recommendation: Use environment variables

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 5. Code Formatting
Status: ⏭️  SKIP (Prettier not configured)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Recommendations

### Critical (Must Fix)
1. Remove hardcoded API key from src/config.ts:12
   → Move to .env file: API_KEY=your_key_here
   → Access via: process.env.API_KEY

2. Fix failing test: auth.test.ts:42
   → Test expects valid token but receives undefined
   → Check if JWT signing is working correctly

### Optional (Warnings)
1. src/utils.ts:45 - Use const instead of let
2. Consider adding Prettier for code formatting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Overall Status: ❌ FAIL

You have 2 critical issues that must be resolved:
1. Hardcoded API key (security risk)
2. Failing authentication test (broken functionality)

Next Steps:
1. Fix the API key issue by using environment variables
2. Debug and fix the failing JWT validation test
3. Re-run `/stride:validate` to verify fixes
4. Once validation passes, proceed with `/stride:complete`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Rules**

- MUST validate against currently active sprint only
- MUST detect project type and available validation tools automatically
- MUST provide actionable recommendations for each failure
- MUST distinguish between critical failures and warnings
- MUST check for secrets/API keys in code (security-critical)
- MUST map failures to sprint strides when possible
- MUST support "UPCOMING" status for planned fixes
- MUST NOT modify any code - read-only validation
- Output MUST be structured, clear, and actionable
- MUST prevent completion if critical issues exist

---

**Reference**

- `.stride/project.md` — project context
- `.stride/sprints/SPRINT-*/plan.md` — strides and tasks to check against
- `.stride/sprints/SPRINT-*/implementation.md` — what has been implemented
- Project configuration files — determine what tools to run
- Test output — parse to extract failures
- Sprint acceptance criteria — validate implementation meets goals

<!-- STRIDE:END -->

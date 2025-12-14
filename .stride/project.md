# **Stride - Agent-First Sprint Framework**

## **1. Project Summary**

* **Purpose:**
  Stride transforms chaotic AI coding sessions into structured, trackable, and reproducible workflows. It enables 20+ AI coding agents (Claude, Cursor, Windsurf, etc.) to autonomously plan, implement, and document software features while developers monitor progress from the terminal.
* **Primary Goals:**
  - Provide persistent context across AI agent chat sessions
  - Establish unified methodology for multi-agent development
  - Enable real-time monitoring of AI-driven development via CLI
  - Capture and preserve learnings through automated retrospectives
  - Eliminate context loss and agent inconsistency in AI-powered development
* **Intended Users:**
  - Indie hackers shipping features without losing context
  - Startup CTOs aligning multiple AI tools with unified methodology
  - Enterprise developers requiring validation pipelines and audit trails
  - AI-first developers tracking agent implementations across sprints

---

## **2. Functional Overview**

* **Core Features:**
  - Sprint lifecycle management (Proposed → Active → Completed)
  - Multi-agent command installation and template conversion
  - CLI-based sprint monitoring and analytics
  - Automated documentation generation from completed sprints
  - Quality gate validation before sprint completion
  - Interactive agent selection and configuration
  - File-based state management with Git integration
* **User Flows:**
  - Initialize Stride in project → Select AI agents → Install slash commands
  - Create sprint proposal → Plan with strides/tasks → Implement with tracking → Validate quality → Complete with retrospective
  - Monitor sprints via CLI (list, status, show, metrics)
  - Generate project documentation from completed sprints
  - Derive new sprints from existing ones
* **Critical Behaviors:**
  - Sprint state must be determinable from file existence alone
  - All sprint data must be fully portable and version-controlled
  - Template conversion must correctly format for 20 different agents
  - CLI must provide real-time visibility into agent progress
  - Quality validation must block completion until critical issues resolved

---

## **3. Non-Functional Requirements**

### **3.1 Performance**

* CLI commands must respond within 2 seconds for normal operations
* Sprint listing must handle 1000+ sprints without degradation
* Template conversion must complete in <100ms per template
* Analytics calculation should cache results and update incrementally

### **3.2 Reliability**

* File operations must be atomic to prevent corruption
* Invalid sprint states must be detected and reported clearly
* Template parsing errors must provide actionable feedback
* Agent registry must gracefully handle unknown agent types

### **3.3 Security**

* No sensitive data in sprint files (use environment variables for secrets)
* Authentication tokens stored in system keyring (via keyring library)
* Validation must scan for accidentally committed secrets
* Supabase integration uses secure credential management

### **3.4 Compliance**

* MIT license compliance for open-source distribution
* No telemetry without explicit user consent
* Privacy-first: all data stored locally in `.stride/` by default
* Cloud features (Supabase analytics) are strictly opt-in

---

## **4. Technical Stack**

* **Languages:** Python 3.8+
* **Frameworks:**
  - Typer (CLI framework with automatic help generation)
  - Rich (terminal formatting, tables, progress bars)
  - Pydantic (data validation and models)
  - PyYAML (template and config parsing)
  - Questionary (interactive prompts)
* **Database(s):**
  - File-based storage (Markdown files in `.stride/`)
  - Optional: Supabase (for cloud analytics and auth)
* **Infrastructure / hosting:**
  - PyPI package distribution
  - GitHub repository hosting
  - MkDocs Material for documentation site
* **Build, test, deployment tools:**
  - setuptools for package building
  - pytest for unit testing
  - pytest-cov for coverage reporting
  - black for code formatting (line length: 100)
  - isort for import sorting
  - mypy for type checking

---

## **5. Architecture Snapshot**

* **High-level design pattern:**
  Modular monolith with clear separation between CLI interface, business logic, and file management. File-based state machine using markdown documents as the source of truth.

* **Major components and their responsibilities:**
  - `stride/cli.py`: Typer app entry point and command routing
  - `stride/commands/`: CLI command implementations (init, list, status, show, validate, metrics, docs)
  - `stride/core/sprint_manager.py`: Sprint lifecycle and state management
  - `stride/core/markdown_parser.py`: Parse and extract data from sprint markdown files
  - `stride/core/agent_registry.py`: Manage 20 agent configurations
  - `stride/core/template_converter.py`: Convert templates to 9 agent formats
  - `stride/core/documentation_generator.py`: Generate MkDocs from sprints
  - `stride/core/analytics.py`: Calculate sprint metrics and insights
  - `stride/core/validator.py`: Quality gate checks and validation
  - `stride/models.py`: Pydantic data models for sprints, agents, configs
  - `stride/templates/`: Sprint file templates, agent command templates

* **How components communicate:**
  - CLI commands invoke core business logic functions
  - Core modules read/write markdown files via file_manager
  - Models validate data flowing between layers
  - Utils provide cross-cutting concerns (logging, formatting)

* **How data flows:**
  1. CLI receives command → 2. Command validates input → 3. Core logic reads `.stride/` files → 4. Business logic processes/transforms data → 5. Core logic writes updated markdown files → 6. CLI formats and displays results with Rich

---

## **6. Standards & Conventions**

### **6.1 Coding Rules**

* **Naming conventions:**
  - snake_case for functions, variables, file names
  - PascalCase for classes
  - UPPER_CASE for constants
  - Private functions prefixed with `_`
* **Folder structure:**
  ```
  stride/
  ├── commands/       # CLI command implementations
  ├── core/          # Business logic
  ├── templates/     # Markdown templates
  ├── cli.py         # Main entry point
  ├── models.py      # Data models
  ├── constants.py   # Global constants
  └── utils.py       # Utility functions
  ```
* **Formatting:**
  - Black formatter with 100 character line length
  - isort for import organization (black profile)
  - Type hints required for public functions
* **Required comments or documentation:**
  - Module-level docstrings for all files
  - Function docstrings with Args, Returns, Raises sections
  - Inline comments for complex logic only
  - README updates for new features

### **6.2 Version Control Workflow**

* **Branching model:**
  - `main` branch for production releases
  - Feature branches: `feature/<name>`
  - Bugfix branches: `fix/<name>`
  - Version tags: `v1.0.0`, `v1.0.1`, etc.
* **Commit message style:**
  - Conventional Commits format
  - Examples: `feat: add metrics command`, `fix: sprint ID generation`, `docs: update README`
* **PR review rules:**
  - All changes require PR review before merge
  - Tests must pass
  - Black/isort formatting enforced
  - No merge conflicts

### **6.3 Testing Strategy**

* **Required test types:**
  - Unit tests for core business logic
  - Integration tests for file operations
  - CLI command tests using Typer's testing utilities
* **Coverage expectations:**
  - Minimum 70% code coverage (target: 85%+)
  - Core logic must have >90% coverage
* **What must be mocked vs. tested directly:**
  - Mock: File I/O in unit tests, external APIs (Supabase), system keyring
  - Test directly: Data validation, markdown parsing, template conversion, sprint state logic

---

## **7. Domain Knowledge (Critical for QA Behavior)**

* **Key domain entities:**
  - **Sprint**: A discrete unit of work with unique ID (SPRINT-XXXXX)
  - **Stride**: Milestone within a sprint containing tasks
  - **Task**: Individual work item within a stride
  - **Agent**: AI coding tool (20 supported types)
  - **Template**: Agent-specific command format (9 types)
  - **Sprint Status**: PROPOSED (proposal.md only), ACTIVE (proposal + plan/design/implementation), COMPLETED (all files including retrospective)

* **Entity relationships:**
  - Project (1) → Sprints (many)
  - Sprint (1) → Strides (many) → Tasks (many)
  - Agent (1) → Templates (9 format variations)
  - Sprint (1) → Sprint Files (5-6 markdown documents)

* **Business rules / invariants:**
  - Sprint IDs must be unique within a project
  - Sprint status determined by file existence: PROPOSED (proposal.md), ACTIVE (+ implementation.md), COMPLETED (+ retrospective.md)
  - All sprint data must be parseable as valid markdown
  - Template frontmatter must contain required fields for agent type
  - Quality validation must pass before sprint completion
  - Retrospective must document what worked and what didn't

* **Edge cases that commonly break:**
  - Malformed YAML frontmatter in templates
  - Sprint files with inconsistent markdown structure
  - Missing `.stride/` directory causing file operations to fail
  - Agent types not in registry attempting to use commands
  - Empty or incomplete sprint files
  - Concurrent file modifications during sprint updates

* **Historical issues:**
  - Early versions didn't validate sprint state before operations
  - Template conversion initially didn't handle all edge cases for YAML/TOML formats
  - Analytics calculations were expensive without caching
  - Documentation generation could fail on incomplete sprints

---

## **8. Constraints**

### **8.1 Technical Constraints**

* Python 3.8+ required (cannot use newer syntax features for compatibility)
* Must work on Windows, macOS, and Linux
* CLI-only interface (no GUI dependencies)
* Markdown files must remain human-readable and Git-friendly
* No required databases or infrastructure setup
* Package size should remain under 5MB

### **8.2 Business Constraints**

* MIT license must be maintained (open source)
* PyPI package name: `stridekit` (not `stride` - taken)
* Must support 20 agents without requiring per-agent maintenance
* Documentation site hosted on GitHub Pages
* Free tier compatibility for optional cloud features

### **8.3 Operational Constraints**

* Must work fully offline (cloud features optional)
* No persistent background processes
* File operations must be safe with manual Git operations
* CLI commands must work in CI/CD environments
* Should integrate with standard development workflows

---

## **9. External Dependencies**

* **APIs or services used:**
  - Supabase (optional): Analytics storage and user authentication
  - PyPI: Package distribution
  - GitHub: Repository hosting and issue tracking

* **SDKs:**
  - supabase-py (>=2.0.0): Supabase client library
  - keyring (>=24.0.0): Secure credential storage

* **Rate limits:**
  - Supabase: Free tier limits apply (50,000 rows, 500MB storage)
  - PyPI: Standard upload limits for package publishing

* **Authentication mechanisms:**
  - Supabase: Email/password via `stride auth login`
  - GitHub: OAuth for repository access (future feature)
  - Keyring: System-level credential storage

* **Failure modes and fallback strategy:**
  - Supabase unavailable → Gracefully disable analytics features, continue with local-only mode
  - Keyring unavailable → Prompt for credentials each time (no persistent storage)
  - Template file missing → Use embedded default templates
  - Invalid sprint file → Display clear error, suggest validation command

---

## **10. Validation Criteria**

### **10.1 Acceptance Criteria Format**

* **Preconditions:**
  - `.stride/` directory exists with valid structure
  - Active sprint has required files (proposal.md, plan.md)
  - Python 3.8+ environment available

* **Expected behavior:**
  - Commands execute successfully and display formatted output
  - Sprint state changes reflected in file system immediately
  - Validation errors provide actionable remediation steps
  - Quality gates block completion when critical issues present

* **Edge cases:**
  - Empty sprint directory → Display helpful "no sprints" message
  - Corrupted sprint file → Parse error with file path and line number
  - Multiple active sprints → Allow and display all
  - Sprint ID collision → Generate new unique ID

* **Failure-handling expectations:**
  - File I/O errors → Display clear error with path and permission info
  - Validation failures → List all issues with severity levels (FAIL, UPCOMING, PASS)
  - Template parsing errors → Show YAML/TOML error with context
  - Network errors → Fail gracefully with offline mode fallback

### **10.2 Definition of Done**

* **Feature completeness:**
  - Implemented as specified in sprint plan
  - All strides and tasks completed
  - Quality validation passes with no FAIL statuses

* **Documentation updated:**
  - README.md updated for user-facing changes
  - CHANGELOG.md entry added
  - Docstrings written for new functions
  - Example usage added if applicable

* **Tests passed:**
  - All unit tests pass
  - Integration tests pass
  - Coverage threshold met (70%+)
  - Manual testing completed for CLI flows

* **No regression introduced:**
  - Existing CLI commands still work
  - Sprint parsing still handles all templates
  - Agent registry still supports all 20 agents
  - Documentation generation still works

### **10.3 Quality Gates**

* **Linting must pass:**
  - Black formatting (100 char lines)
  - isort import ordering
  - No unused imports or variables

* **Security checks must pass:**
  - No hardcoded secrets or tokens
  - No SQL injection vulnerabilities
  - No path traversal vulnerabilities
  - Dependency security scan clean

* **Test coverage threshold reached:**
  - Minimum 70% overall coverage
  - Core modules >90% coverage
  - New code >80% coverage

* **Performance budgets met:**
  - CLI commands <2s response time
  - Sprint listing handles 1000+ sprints
  - Template conversion <100ms per template
  - Memory usage <100MB for typical operations

---

## **11. Known Risks & Assumptions**

* **Risks that could affect delivery:**
  - Markdown parsing edge cases may break with unusual formatting
  - Agent template requirements may change, requiring format updates
  - File system concurrency issues if multiple processes modify `.stride/` simultaneously
  - Large repositories (10,000+ sprints) may cause performance degradation
  - Breaking changes in dependencies (Typer, Rich, Pydantic) could require major refactoring

* **Open questions or ambiguous areas:**
  - Should Stride support nested sprints or sprint dependencies?
  - How to handle sprint archiving/cleanup for completed sprints?
  - Should there be a GUI or web interface in the future?
  - How to scale analytics beyond file-based parsing?
  - Should Stride integrate directly with AI agent APIs for automation?

* **Assumptions that AI should explicitly confirm or challenge:**
  - Users understand basic Git workflows and version control
  - Markdown is an acceptable format for all sprint documentation
  - CLI is sufficient for all monitoring and management tasks
  - 5-character hex IDs provide sufficient uniqueness for sprint identification
  - AI agents will follow the slash command conventions consistently
  - Quality validation tools (linters, type checkers, test runners) are available in user environments
  - Users prefer local-first, offline-capable workflows over cloud-based solutions
  - Sprint methodology is appropriate for all types of software changes

---

---
description: Generate comprehensive project documentation from completed sprints.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Guardrails**
- `/stride:docs` analyzes **only completed sprints** (those with `retrospective.md`).
- Does **NOT include sprint process documentation** - only the final project documentation.
- Creates/updates the `docs/` folder with all necessary documentation.
- Must validate `.stride/project.md` exists before proceeding.
- Analyzes actual codebase implementation alongside sprint files.
- Generates standard documentation structure: index, features, getting-started.
- Creates `mkdocs.yml` configuration for MkDocs documentation site.

---

**Steps**

1. **Validate Project Context**
   - Check if `.stride/project.md` exists.
   - If missing → stop and suggest: "Run `/stride:init` to initialize the project first."
   - If present → extract project name from the first H1 heading.

2. **Identify Completed Sprints**
   - Scan `.stride/sprints/` directory for all sprint folders.
   - For each sprint, check if `retrospective.md` exists.
   - Filter to get only **COMPLETED** sprints.
   - If no completed sprints → inform user: "No completed sprints found. Complete a sprint with `/stride:complete` first."

3. **Analyze Each Completed Sprint**
   For each completed sprint:

   **a) Read Sprint Files**:
   - Read `proposal.md` - Extract feature description and goals
   - Read `plan.md` - Extract technical approach
   - Read `design.md` (if exists) - Extract architecture decisions
   - Read `implementation.md` - Extract implementation details
   - Read `retrospective.md` - Extract summary and learnings

   **b) Extract Feature Information**:
   - **Feature Name**: From sprint title (first H1 in proposal.md)
   - **Description**: From "Description" section in proposal.md
   - **Goals**: From "Acceptance Criteria" in proposal.md
   - **Technical Approach**: From plan.md overview
   - **Implementation Summary**: From retrospective.md "What We Built" section
   - **Key Decisions**: From retrospective.md "Decisions" section

   **c) Analyze Codebase**:
   - Find files mentioned in implementation.md logs
   - Read actual implemented code to verify functionality
   - Extract code examples for documentation
   - Identify API endpoints, functions, classes created
   - Note configuration changes made

4. **Generate Documentation Structure**

   Create/update the following files in `docs/`:

   **a) `docs/index.md`** (Project Overview):
   ```markdown
   # {Project Name}

   ## Overview
   {Brief description from project.md}

   ## Features
   - Feature 1: {brief description}
   - Feature 2: {brief description}
   ...

   ## Project Structure
   {High-level architecture overview}

   ## Quick Links
   - [Getting Started](getting-started.md)
   - [Features Documentation](features.md)
   ```

   **b) `docs/features.md`** (Feature Documentation):
   ```markdown
   # Features

   ## 1. {Feature Name}

   **Description**: {Detailed feature description}

   **Key Capabilities**:
   - Capability 1
   - Capability 2

   **Usage**:
   {Code examples and usage instructions}

   **API Reference** (if applicable):
   {API endpoints, parameters, responses}

   ---

   ## 2. {Next Feature}
   ...
   ```

   **c) `docs/getting-started.md`** (Setup Guide):
   ```markdown
   # Getting Started

   ## Prerequisites
   {List requirements}

   ## Installation
   {Installation steps}

   ## Configuration
   {Configuration instructions}

   ## Quick Start
   {Minimal example to get running}

   ## Next Steps
   - Link to feature docs
   - Link to advanced guides
   ```

   **d) `docs/mkdocs.yml`** (MkDocs Configuration):
   ```yaml
   site_name: {Project Name} Documentation
   site_description: {Description}
   site_author: Stride Framework

   theme:
     name: material
     palette:
       primary: indigo
       accent: indigo
     features:
       - navigation.instant
       - navigation.sections
       - navigation.expand
       - toc.integrate

   nav:
     - Home: index.md
     - Getting Started: getting-started.md
     - Features: features.md

   markdown_extensions:
     - admonition
     - codehilite
     - toc:
         permalink: true

   extra:
     generator: Stride Framework
   ```

5. **Organize Content by Category**

   Group features by logical categories:

   **Rule 1: Feature Grouping**
   ```
   IF multiple features are related:
       Group them under a common section in features.md
       Example: "Authentication Features", "Data Management Features"
   ```

   **Rule 2: Advanced Documentation**
   ```
   IF any sprint includes complex architecture:
       Create additional `docs/architecture.md`
       Add to mkdocs.yml nav
   ```

   **Rule 3: API Documentation**
   ```
   IF project has API endpoints:
       Create `docs/api-reference.md`
       Document all endpoints with examples
       Add to mkdocs.yml nav
   ```

6. **Generate Code Examples**

   Extract real code from implementation to include in docs:

   - **Function Signatures**: From actual implementation files
   - **Usage Examples**: Create realistic examples based on implementation
   - **Configuration Examples**: From actual config files created
   - **API Examples**: Real request/response examples if applicable

7. **Format Documentation**

   **Formatting Rules**:
   - Use proper markdown headings (H1 for title, H2 for main sections, H3 for subsections)
   - Include code blocks with language syntax highlighting
   - Add admonitions for warnings, tips, and notes
   - Use tables for structured data (parameters, API endpoints)
   - Include links between related documentation pages
   - Keep descriptions concise but comprehensive
   - Focus on "what" and "how", not the sprint process

8. **Create MkDocs Configuration**

   Generate `docs/mkdocs.yml` with:
   - Material theme (modern, responsive)
   - Navigation structure based on generated docs
   - Markdown extensions for enhanced features
   - Search functionality enabled
   - Table of contents integration

9. **Report Generation Results**

   Inform user of what was generated:

   ```
   Documentation generated successfully! ✅

   Created/Updated:
   - docs/index.md (project overview)
   - docs/features.md ({n} features documented)
   - docs/getting-started.md (setup guide)
   - docs/mkdocs.yml (MkDocs configuration)

   Documented {n} completed sprints:
   - {sprint-1-name}
   - {sprint-2-name}
   - {sprint-3-name}

   Next Steps:
   1. Run `stride docs` to start the documentation server
   2. Visit http://127.0.0.1:8000 to view the docs
   3. Customize mkdocs.yml for your needs
   4. Add any additional manual documentation
   ```

---

**Documentation Content Rules**

**DO Include**:
- Final feature descriptions and capabilities
- How to use implemented features
- Code examples from actual implementation
- API reference if applicable
- Configuration options
- Setup and installation instructions
- Architecture decisions (high-level)
- Integration guides

**DO NOT Include**:
- Sprint process details (strides, tasks, logs)
- Implementation timeline or history
- Sprint-specific retrospectives
- References to sprint IDs or sprint structure
- Development workflow details
- Stride framework references in user-facing docs

**Focus**: The documentation should represent the **final product**, not how it was built.

---

**When to Trigger**

The command MUST trigger when the user says:
- "Generate documentation"
- "Create docs"
- "Update documentation"
- "Generate the docs"
- "Create project documentation"
- "Generate docs from sprints"

---

**When NOT to Trigger**

- When user wants to **view** documentation (use `stride docs` CLI instead)
- When creating sprint documentation (that's in `.stride/sprints/`)
- For status updates or reports
- During implementation work

---

**Output Example**

```
Documentation generated successfully! ✅

Created/Updated:
├── docs/index.md (project overview)
├── docs/features.md (5 features documented)
├── docs/getting-started.md (setup guide)
└── docs/mkdocs.yml (MkDocs configuration)

Documented 5 completed sprints:
✓ User Authentication System
✓ Database Schema & Models
✓ REST API Endpoints
✓ Frontend Dashboard
✓ Error Handling & Logging

Features Documented:
1. User Authentication - JWT-based auth with role management
2. Data Models - Complete database schema with relationships
3. REST API - 12 endpoints with full CRUD operations
4. Dashboard UI - Responsive admin interface
5. Error System - Centralized error handling and logging

Next Steps:
1. Run `stride docs` to start the documentation server
2. Visit http://127.0.0.1:8000 to view your docs
3. Customize docs/mkdocs.yml for your project needs
4. Review and enhance getting-started.md with specifics

The documentation is ready! You can now serve it with `stride docs` 📚
```

---

**Rules**

- MUST validate `.stride/project.md` exists before proceeding
- MUST only analyze sprints with `retrospective.md` (completed sprints)
- MUST create `docs/` directory if it doesn't exist
- MUST generate all four core files: index.md, features.md, getting-started.md, mkdocs.yml
- MUST analyze actual implementation files, not just sprint documents
- MUST exclude sprint process details from generated documentation
- MUST use proper markdown formatting and structure
- Output MUST be user-facing documentation, not developer process documentation
- MUST inform user how to view the documentation after generation

---

**Reference**

- `.stride/project.md` — project context and name
- `.stride/sprints/SPRINT-*/retrospective.md` — identifies completed sprints
- `.stride/sprints/SPRINT-*/proposal.md` — feature descriptions
- `.stride/sprints/SPRINT-*/implementation.md` — implementation details
- Actual codebase files — real implementation to document
- `docs/mkdocs.yml` — MkDocs configuration (will create if missing)

<!-- STRIDE:END -->

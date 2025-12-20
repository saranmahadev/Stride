---
description: Initialize or validate the Stride project context.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If project context is missing or incomplete:

1. **Auto-Detection First**:
   - Scan repository for existing documentation (README.md, package.json, pyproject.toml, etc.)
   - Analyze directory structure for tech stack clues
   - Detect dependencies and frameworks from config files
   - Infer domain from code patterns and naming
   - Extract project purpose from existing docs

2. **Targeted Questions Only** (for missing critical info):
   - Ask ONLY specific, narrow questions about undetectable information
   - Never ask: "Tell me about your project" (too broad)
   - Good examples:
     - "What is the primary business purpose? (e.g., e-commerce platform, data analytics tool)"
     - "What's the target deployment environment? (cloud/on-premise/hybrid)"
     - "Any specific compliance requirements? (GDPR, HIPAA, SOC2)"
   
3. **Question Priority** (ask in order, skip if detectable):
   - **High Priority**: Project purpose, primary tech stack (if not detected)
   - **Medium Priority**: Target users, deployment constraints
   - **Low Priority**: Nice-to-haves that can be updated later
   
4. **Never Prompt For**:
   - Information clearly present in README or docs
   - Tech stack visible in dependencies
   - Architecture patterns evident in code structure
   - Standard conventions for detected frameworks

5. **Accept Minimal Input**:
   - If user provides brief answers, infer reasonable defaults
   - Don't repeatedly ask for more detail
   - Generate sensible project.md with available information
   - Note what can be refined later

6. **Proceed** to create `.stride/project.md` with gathered + detected information

---

**Steps**

1. **Project Analysis**
   - **Tech Stack**: Identify languages, frameworks, and key libraries.
   - **Architecture**: Determine architectural patterns (MVC, Microservices, Monolith, etc.).
   - **Current State**: Assess code quality, test coverage, and documentation status.

2. **Lite Sprint Detection**
   - Analyze the scope of potential work.
   - If the task is small (single file change, minor bug fix), suggest a **Lite Sprint**.
   - If the task is complex (new feature, refactoring), suggest a **Full Sprint**.

3. **NICE Marker Check**
   - Scan for existing NICE markers in the codebase.
   - If markers are missing or sparse, suggest running `/stride:annotate` to improve agent understanding.

4. **Context Creation**
   - Generate `.stride/project.md` using the template.
   - **Initialize `learnings.md`**:
     - Copy `.stride/templates/learnings.md` to `.stride/learnings.md`
     - Add first learning entry with project context:
       ```markdown
       ## Architecture
       - [Project: {name}] Tech stack: {stack}. Architecture: {pattern}. (sprint-init)
       ```
   - Ensure `marker.md` is present (copy from `.stride/templates/marker.md` if missing).

---

**Guardrails**
- Follow `.stride/project.md` template exactly—no added/removed sections.
- Do not generate sprint files during init.
- Ensure `learnings.md` and `marker.md` are initialized.
- Ask only targeted questions when the repo lacks enough context.
- Never overwrite an existing valid `.stride/project.md` without explicit confirmation.
- Keep initialization strictly focused on establishing project-level understanding (not sprint planning).

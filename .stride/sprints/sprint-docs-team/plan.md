# Plan

## Overview

This sprint systematically documents all v1.5 team collaboration features across 6 key files. The approach follows a layered strategy: start with high-level user-facing documentation (README, FEATURES), then add release notes (CHANGELOG), create comprehensive workflow guide (team-workflow.md), enhance CLI reference, and update website index. Total estimated documentation: ~1,260 lines across 4 strides.

**Strategy:** Document from general to specific - start with overview sections that drive discovery, then provide detailed command references, workflow examples, and troubleshooting guidance. Each stride produces complete, publishable documentation for its target audience.

**Key Concerns:**
- Accuracy: Documentation must exactly match implemented behavior
- Completeness: Cover all 20 new commands and 4 enhanced commands
- Usability: Examples must be practical and copy-pasteable
- Consistency: Match existing Stride documentation tone and style
- Discoverability: Users must easily find team features from README

The work directly supports v1.5 release announcement and positions Stride for team user adoption per ROADMAP.md Phase 2 goals.

---

## Strides

### **Stride 1: Core Documentation Updates (README, FEATURES)**

**Purpose:**  
Update primary user-facing documentation (README.md and FEATURES.md) to introduce team collaboration features and provide command overview.

**Tasks:**  
- [ ] Task 1.1: Add "Team Collaboration" section to README.md after Quick Start (~50 lines)
- [ ] Task 1.2: Write 4-6 sentence overview explaining Git-based, zero-infrastructure team model
- [ ] Task 1.3: Add quick example showing `stride team init` → `stride assign` → `stride approve status` workflow
- [ ] Task 1.4: Update feature highlights to mention team collaboration
- [ ] Task 1.5: Add link to detailed team-workflow.md guide
- [ ] Task 1.6: Create "Team Collaboration (v1.5)" section in FEATURES.md (~500 lines)
- [ ] Task 1.7: Document all 7 `stride team` commands (init, add, remove, edit, list, show) with parameters
- [ ] Task 1.8: Document all 3 `stride assign` commands (assign, unassign, workload) with AI recommendations
- [ ] Task 1.9: Document all 4 `stride approve` commands (approve, revoke, status, pending) with workflow
- [ ] Task 1.10: Document all 6 `stride comment` commands (add, list, resolve, unresolve, stats) with threading
- [ ] Task 1.11: Explain workload balancing complexity formula: `(strides * 5) + tasks` normalized to 0-100
- [ ] Task 1.12: Explain balance score formula: `100 - (stdev as % of mean)`
- [ ] Task 1.13: Include Rich output examples for key commands (team list, assign workload, approve status)
- [ ] Task 1.14: Add subsection explaining Git-based collaboration model (offline-capable, no servers)

**Completion Definition:**  
- README.md has complete team section with working example
- FEATURES.md has comprehensive v1.5 section covering all commands
- Examples tested and copy-pasteable
- Formulas accurately represent workload_analyzer.py implementation
- Follows existing Stride documentation style (similar to v1.0 sections)

---

### **Stride 2: Release Notes & Changelog**

**Purpose:**  
Document v1.5 release in CHANGELOG.md with complete list of additions, changes, and notes for PyPI release.

**Tasks:**  
- [ ] Task 2.1: Create [1.5.0] section in CHANGELOG.md with release date 2025-12-14
- [ ] Task 2.2: Add "Added" subsection listing all 20 new team commands by category
- [ ] Task 2.3: List 9 new core modules: team_file_manager, assignment_manager, approval_manager, comment_manager, workload_analyzer
- [ ] Task 2.4: List 4 new command modules: team.py, assign.py, approve.py, comment.py
- [ ] Task 2.5: Document 8 new Pydantic models: TeamConfig, TeamMember, SprintMetadata, Comment, Approval, ApprovalPolicy, MetadataEvent
- [ ] Task 2.6: Mention workload analyzer with complexity scoring algorithm
- [ ] Task 2.7: Add "Changed" subsection for enhanced commands (stride list, stride metrics)
- [ ] Task 2.8: Document `--assignee` filter for `stride list`
- [ ] Task 2.9: Document workload panel integration in `stride metrics`
- [ ] Task 2.10: Add "Notes" subsection emphasizing backward compatibility with v1.0 solo workflows
- [ ] Task 2.11: Add note that team features are optional (solo mode still fully supported)
- [ ] Task 2.12: Reference ROADMAP.md Phase 2 completion
- [ ] Task 2.13: Follow Keep a Changelog format conventions

**Completion Definition:**  
- CHANGELOG.md [1.5.0] section complete with all modules and commands listed
- Follows existing changelog format (matches [1.0.0] and [1.0.1] structure)
- Emphasizes backward compatibility
- Ready for PyPI release notes
- No placeholder text or TODOs

---

### **Stride 3: Team Workflow Guide**

**Purpose:**  
Create comprehensive team workflow documentation (docs/team-workflow.md) explaining Git-based collaboration patterns, approval policies, and end-to-end examples.

**Tasks:**  
- [ ] Task 3.1: Create docs/team-workflow.md file (~400 lines)
- [ ] Task 3.2: Write introduction explaining "repo-first, zero-infrastructure" philosophy
- [ ] Task 3.3: Document team initialization workflow: `stride team init` → add members → configure policy
- [ ] Task 3.4: Explain approval policy options (N reviewers, role restrictions, enabled/disabled)
- [ ] Task 3.5: Document assignment workflow: interactive vs direct mode
- [ ] Task 3.6: Explain AI assignee recommendations with scoring factors (workload, roles, history)
- [ ] Task 3.7: Document approval workflow: approve → status → threshold → complete
- [ ] Task 3.8: Explain comment system: threading, file/line anchoring, resolution
- [ ] Task 3.9: Document workload balancing: distribution analysis, overload detection, recommendations
- [ ] Task 3.10: Show balance score visualization with progress bars
- [ ] Task 3.11: Provide Example 1: Small team (3 devs) setting up first sprint
- [ ] Task 3.12: Provide Example 2: Assignment with AI recommendations and reassignment
- [ ] Task 3.13: Provide Example 3: Approval workflow with 2-reviewer policy
- [ ] Task 3.14: Provide Example 4: Comment-based code review with resolution
- [ ] Task 3.15: Provide Example 5: Workload balancing across team members
- [ ] Task 3.16: Add troubleshooting section (team.yaml not found, permission errors, Git conflicts)
- [ ] Task 3.17: Add "Best Practices" section (role assignment, approval policies, workload monitoring)
- [ ] Task 3.18: Include navigation links to cli-commands.md for command details

**Completion Definition:**  
- Complete workflow guide with 5 practical examples
- Covers all major team features (team mgmt, assignment, approval, comments, workload)
- Troubleshooting section addresses common errors
- Examples are tested and accurate
- Follows MkDocs Material markdown conventions
- Includes diagrams or formatted examples using code blocks

---

### **Stride 4: CLI Reference & Website Updates**

**Purpose:**  
Update CLI command reference (docs/cli-commands.md) with team commands and refresh website index (docs/index.md) for v1.5 announcement.

**Tasks:**  
- [ ] Task 4.1: Add "Team Management" section to docs/cli-commands.md (~50 lines)
- [ ] Task 4.2: Document `stride team init` with syntax, description, parameters, examples, exit codes
- [ ] Task 4.3: Document `stride team add/remove/edit/list/show` commands
- [ ] Task 4.4: Add "Sprint Assignment" section (~50 lines)
- [ ] Task 4.5: Document `stride assign <sprint-id>` with interactive vs direct mode
- [ ] Task 4.6: Document `stride unassign` and `stride assign workload` commands
- [ ] Task 4.7: Explain JSON export format for `stride assign workload --export`
- [ ] Task 4.8: Add "Approval Workflow" section (~40 lines)
- [ ] Task 4.9: Document all `stride approve` commands with approval threshold behavior
- [ ] Task 4.10: Add "Comments & Communication" section (~40 lines)
- [ ] Task 4.11: Document all `stride comment` commands with threading examples
- [ ] Task 4.12: Document --force flags for destructive operations (team remove, approve revoke)
- [ ] Task 4.13: Include help text excerpts from actual CLI output for accuracy
- [ ] Task 4.14: Update docs/index.md with v1.5 announcement banner (~30 lines)
- [ ] Task 4.15: Add "Team Collaboration" to feature list on index page
- [ ] Task 4.16: Update "Getting Started" flow to mention optional team setup
- [ ] Task 4.17: Add navigation link to team-workflow.md in MkDocs nav
- [ ] Task 4.18: Validate MkDocs build succeeds: `mkdocs build`
- [ ] Task 4.19: Test local preview: `mkdocs serve`
- [ ] Task 4.20: Verify all internal links work (no 404s)

**Completion Definition:**  
- docs/cli-commands.md has complete team command reference
- All commands documented with consistent format (matches existing commands)
- docs/index.md updated with v1.5 announcement
- MkDocs site builds without errors
- Navigation includes team-workflow.md
- All examples and links verified working

---

## Approach

**Documentation Strategy:**
- **Accuracy First**: Reference sprint-team-collab implementation.md for exact behavior
- **User-Centric**: Write for developers discovering features, not implementers
- **Example-Heavy**: Provide copy-pasteable commands and expected output
- **Layered Detail**: README (overview) → FEATURES (commands) → team-workflow (patterns) → cli-commands (reference)

**Technical Implementation:**
- Use existing Stride documentation tone (concise, technical, example-driven)
- Follow MkDocs Material markdown conventions (admonitions, code blocks, tables)
- Match FEATURES.md style for command documentation (v1.0 sections as template)
- Use Rich output examples (color codes like `[green]`, `[cyan]`) for terminal output
- Include actual YAML snippets for team.yaml, .metadata.yaml, .comments.yaml

**Quality Assurance:**
- Cross-reference implementation.md logs for accurate command behavior
- Test all examples in actual Stride project before documenting
- Verify formulas against workload_analyzer.py source code
- Run `mkdocs build` after each stride to catch syntax errors early
- Compare tone/style with existing docs (README, FEATURES, sprint-lifecycle.md)

**Sequencing Rationale:**
1. **Stride 1** establishes visibility (README/FEATURES) - users discover features
2. **Stride 2** provides release context (CHANGELOG) - official announcement ready
3. **Stride 3** deep-dives workflows (team-workflow.md) - self-service onboarding
4. **Stride 4** completes reference material (cli-commands, index) - comprehensive coverage

This approach ensures each stride produces complete, publishable documentation that can be committed independently.

---

## Dependencies

**Technical:**
- Sprint-team-collab completed ✓ (all features implemented)
- MkDocs Material theme installed ✓ (docs site infrastructure ready)
- Rich library available ✓ (for output examples)

**Information:**
- Access to sprint-team-collab/implementation.md (completed logs for accuracy)
- Access to source code: stride/commands/*.py, stride/core/*_manager.py
- Access to workload_analyzer.py for formula verification

**Environmental:**
- Working MkDocs development environment
- Ability to run `mkdocs serve` for local preview
- Git repository up-to-date

**Blocking:** None. All information and tooling available.

**Nice-to-Have:** Screenshots of Rich terminal output (not required, text examples sufficient)

---

## Risks

**Risk:** Documentation describes behavior that differs from implementation  
**Impact:** High - Users follow incorrect examples, file bug reports  
**Mitigation:** Cross-reference all examples with implementation.md logs and source code. Test commands before documenting.

**Risk:** MkDocs build fails with syntax errors  
**Impact:** Medium - Site deployment blocked, delays release  
**Mitigation:** Run `mkdocs build` incrementally after each stride. Use markdown linters.

**Risk:** Examples become outdated if commands change post-documentation  
**Impact:** Medium - Users confused by incorrect examples  
**Mitigation:** Document after feature freeze. Add note in implementation.md to update docs if APIs change.

**Risk:** Complexity formulas documented incorrectly  
**Impact:** Low - Users misunderstand workload scoring  
**Mitigation:** Directly copy formula from workload_analyzer.py comments. Include reference to source code.

**Risk:** Documentation style inconsistent with existing docs  
**Impact:** Low - Unprofessional appearance  
**Mitigation:** Use FEATURES.md v1.0 sections as style template. Review before committing each stride.

---

## Validation Plan

### Functional Validation

**Per Stride:**
- [ ] All documented commands executable in test Stride project
- [ ] Examples produce expected output (match implementation)
- [ ] Links resolve correctly (no 404s)
- [ ] Code blocks have correct syntax highlighting

**Final Validation:**
- [ ] Run `mkdocs build` successfully
- [ ] Run `mkdocs serve` and manually review all pages
- [ ] Test all example workflows in clean Stride project
- [ ] Verify formulas match workload_analyzer.py implementation
- [ ] Check that all 20 new commands documented

### Technical Validation

- [ ] Markdown syntax valid (no broken formatting)
- [ ] Follows MkDocs Material conventions (admonitions, tables)
- [ ] YAML snippets use correct schema (match models.py)
- [ ] Rich color codes match actual CLI output
- [ ] All internal cross-references work

### Quality Gates

- [ ] No TODOs or placeholder text
- [ ] No spelling errors (run spellcheck)
- [ ] All 4 strides completed
- [ ] Total documentation ~1,260 lines added
- [ ] CHANGELOG.md ready for v1.5 release
- [ ] Documentation reviewed against acceptance criteria in proposal.md

### Completeness Check

- [ ] README.md updated ✓
- [ ] FEATURES.md updated ✓
- [ ] CHANGELOG.md updated ✓
- [ ] docs/team-workflow.md created ✓
- [ ] docs/cli-commands.md updated ✓
- [ ] docs/index.md updated ✓
- [ ] MkDocs navigation updated ✓

---

## Completion Conditions

A sprint is complete when:

- All 4 strides marked complete
- All 6 documentation files updated/created
- All 20 new commands documented with examples
- CHANGELOG.md [1.5.0] section ready for release
- MkDocs site builds and deploys successfully
- No placeholder text or TODOs remain
- Examples tested in actual Stride project
- Documentation reviewed for accuracy against implementation
- Ready for v1.5 public announcement

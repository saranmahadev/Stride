---
description: Execute small changes using Five-Stage Workflow entirely in chat without creating sprint files.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (change description) is not provided:

1. **Prompt User**:
   - Ask: "What small change do you need?"
   - Examples to guide user:
     - "Fix a typo in the header"
     - "Update button styling"
     - "Add a configuration option"
   - Wait for response

2. **Analyze Scope**:
   - Estimate lines and files affected
   - Check eligibility against lite criteria

3. **If Eligible**:
   - Proceed to Talk stage with change description

4. **If Not Eligible**:
   - Explain which criteria failed
   - Suggest: "This needs a full sprint. Use `/stride-plan [description]`"
   - STOP (do not continue)

---

**Guardrails**
- `/stride-lite` is for **small changes only** (< 50 lines, < 3 files, single concern).
- Must NEVER create sprint files or directories.
- Must follow ALL five stages: Talk → Plan → Confirm → Implement → Complete.
- Must validate lite-eligibility BEFORE starting work.
- Must abort and suggest `/stride-plan` if scope exceeds limits.
- All communication happens in chat only.
- No logging to implementation.md.
- No retrospective generation.

---

**Lite-Eligibility Criteria**

Before proceeding, validate the change meets ALL criteria:

✅ **Complexity Check**: The change is straightforward and well-understood.
✅ **No Deep Architecture**: Does not require significant architectural restructuring or new design documents.
✅ **No High Risk**: Does not involve critical security or core infrastructure changes that need a full review process.

If ANY criterion fails → **ABORT** and suggest `/stride-plan` instead.

---

**Stage 1: TALK (Discovery)**

### Goal
Understand the change and validate it qualifies for lite mode.

### Steps

1. **Ask Clarifying Questions**
   - What exactly needs to change?
   - Why is this needed?
   - Which files are affected?
   - Are there any edge cases?

2. **Estimate Scope**
   - Files to modify: ?
   - Complexity: Low/Medium/High

3. **Validate Lite-Eligibility**
   Check against the complexity criteria above.
   
   **If ELIGIBLE**:
   - Confirm: "✅ Eligible for lite mode"
   - Proceed to PLAN stage
   
   **If NOT ELIGIBLE**:
   - Explain which criteria failed (e.g., "Too complex", "Requires architecture design")
   - Suggest: "This change requires a full sprint. Use `/stride-plan <sprint-name>` instead."
   - STOP (do not continue)

4. **Present Estimate**
   ```
   Estimated scope: X files
   Complexity: [Low/Medium]
   ✅ Eligible for lite mode
   ```

---

**Stage 2: PLAN (Design)**

### Goal
State exactly what will change and get preliminary approval.

### Steps

1. **List All Affected Files**
   ```
   Files to modify:
   - path/to/file1.ext (line N)
   - path/to/file2.ext (lines M-P)
   ```

2. **Describe Changes**
   For each file:
   - What will be added/modified/removed
   - Why this change is necessary
   - Expected outcome
   - **NICE Markers**: Identify if markers need to be added or updated.

3. **Explain Reasoning**
   - Technical justification
   - Impact analysis (low/medium)
   - Any dependencies or side effects

4. **Show Before/After Snippets** (Optional)
   ```python
   # Before
   old_code_here
   
   # After
   new_code_here
   ```

5. **Request Approval**
   End with: **"Proceed with this plan?"**

### Example Output
```
[PLAN]

Files to modify:
- src/components/Button.tsx (line 42)
- src/styles/button.css (lines 15-17)

Changes:
1. Button.tsx: Update onClick handler to prevent double-clicks
2. button.css: Adjust padding for better mobile touch targets

Reasoning:
- Fixes reported double-submission bug
- Improves mobile UX (follows Material Design guidelines)

Impact: Low (UI behavior only, no data changes)

Proceed with this plan?
```

---

**Stage 3: CONFIRM (Approval)**

### Goal
Get explicit user confirmation before making changes.

### Steps

1. **Wait for User Response**
   Valid confirmations:
   - "Proceed"
   - "Yes"
   - "Go ahead"
   - "Do it"
   - "Approved"

2. **Handle User Feedback**
   
   **If user says "Proceed"**:
   - Acknowledge: "✅ Confirmed. Moving to implementation."
   - Proceed to IMPLEMENT stage
   
   **If user requests changes**:
   - Update the plan
   - Check if still lite-eligible (scope may have grown)
   - If still eligible → re-present plan and ask "Proceed?"
   - If no longer eligible → abort and suggest `/stride-plan`
   
   **If user expands scope**:
   - Re-estimate lines and files
   - If exceeds limits → abort:
     ```
     ⚠️ Updated scope exceeds lite mode limits.
     
     New estimate: X lines, Y files
     Limit: 50 lines, 3 files
     
     Let's create a proper sprint instead.
     Use `/stride-plan <sprint-name>` to continue.
     ```

3. **Never Skip This Stage**
   - Must wait for explicit approval
   - No assumptions or auto-proceeding

---

**Stage 4: IMPLEMENT (Execution)**

### Goal
Make the approved changes and explain them clearly.

### Steps

1. **Make Code Changes**
   - Execute the changes exactly as planned
   - One file at a time
   - Ensure correctness
   - **Update NICE Markers**: Ensure markers reflect the new code state.

2. **Monitor Scope**
   - Track complexity and impact.
   - If scope grows significantly (e.g., requires new architecture or major refactoring) → warn user.
   - If complexity becomes unmanageable → STOP and abort:
     ```
     ⚠️ Scope exceeded during implementation.
     
     Reason: Change requires architectural design or full sprint planning.
     
     Changes rolled back. Use `/stride-plan` for this work.
     ```

3. **Explain Each Modification**
   For each file changed:
   ```
   filename.ext (line N):
   - [What changed]
   - [Why it matters]
   - [NICE Marker updates]
   ```
   
   **Do NOT dump full files** - show summaries or diffs only.

4. **Highlight Side Effects**
   - Mention any unintended impacts
   - Note if other files might need updates
   - Flag any manual testing needed

5. **Confirm Changes Applied**
   ```
   ✅ Changes applied
   ✅ [Any validations performed]
   ```

### Example Output
```
[IMPLEMENT]

Changes applied:

src/components/Button.tsx (line 42):
- Added debounce wrapper to onClick handler
- Prevents double-clicks within 300ms

src/styles/button.css (lines 15-17):
- padding: 12px 24px; (was 8px 16px)
- min-height: 48px; (meets touch target size)

✅ Double-click prevention active
✅ Mobile touch targets meet accessibility standards
✅ No other components affected
```

---

**Stage 5: COMPLETE (Verification)**

### Goal
Summarize the work and close the lite session.

### Steps

1. **Provide Final Summary**
   ```
   Lite change completed!
   
   Summary:
   - Modified: [list of files]
   - Lines changed: X
   - Type: [Bug fix/Styling/Docs/Config]
   ```

2. **List All Changes**
   - File-by-file breakdown
   - Total line count
   - Change categories

3. **Confirm Quality**
   - Mention if tests passed (if applicable)
   - Note any manual validation performed
   - Highlight any edge cases addressed

   **Optional: Quick Validation**
   For code changes that affect functionality:
   - If tests exist for affected code, run them quickly
   - Note: For comprehensive validation, use `/stride:validate` in a full sprint

4. **Offer Follow-Up**
   Ask if:
   - User wants to run tests manually
   - Related changes needed
   - Any concerns or questions
   - Should create a full sprint for more comprehensive work

5. **No Files Created**
   - Confirm no sprint files were generated
   - This was a chat-only lite session

### Example Output
```
[COMPLETE]

Lite change completed!

Summary:
- Modified: 2 files (src/components/Button.tsx, src/styles/button.css)
- Lines changed: 8 total
- Type: Bug fix + UX improvement

Changes:
✅ Button.tsx: Added double-click prevention
✅ button.css: Improved mobile touch targets

Quality checks:
✅ Follows existing code style
✅ Meets accessibility standards (WCAG 2.1)
✅ No breaking changes

Would you like me to check if any other buttons need similar updates?
```

---

**When to Trigger**

The command MUST trigger when the user says:
- "Quick fix for..."
- "Small change to..."
- "Lite mode: [change description]"
- "Just need to fix..."
- "Typo in..."
- "Update styling for..."
- "Change config..."
- "Fix this bug (it's small)"

---

**When NOT to Trigger**

- When change affects > 50 lines
- When change affects > 3 files
- When change involves architecture decisions
- When user wants a feature (not a fix)
- When security or auth is involved
- When multiple concerns need addressing
- When design.md would be needed
- During active sprint implementation (use `/stride-feedback`)

---

**Abort Conditions (During Workflow)**

Stop immediately and suggest `/stride-plan` if:

1. **Complexity Explodes**
   - Change turns out to require deep architectural changes.
   - Multiple unrelated concerns emerge that need separate tracking.

2. **Architecture Needed**
   - Design decisions required
   - API contracts need defining
   - Data model changes discovered

3. **Security Concerns**
   - Authentication changes
   - Authorization logic
   - Sensitive data handling

**Abort Message Template**:
```
⚠️ This change is too complex for lite mode.

Reason: [specific issue]
Current scope: [Description]

Let's create a proper sprint to handle this correctly.
Use `/stride-plan <sprint-name>` to continue with full planning.
```

---

**Rules**

- MUST validate lite-eligibility in TALK stage
- MUST follow all 5 stages (no skipping)
- MUST get explicit approval in CONFIRM stage
- MUST abort if complexity exceeds limits
- MUST NOT create any files or directories
- MUST NOT log to implementation.md
- MUST NOT update project.md
- MUST NOT generate retrospective.md
- ALL communication happens in chat
- Changes MUST be manageable without full sprint planning

---

**Reference**

- Stride Instructions — for understanding when full sprints are required
- `.stride/project.md` — check alignment with project standards (read-only)
- Five-Stage Workflow — same stages as full sprints, just in chat

<!-- STRIDE:END -->

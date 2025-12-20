# Module: {MODULE_NAME}

## Overview
{2-3 sentence description of module purpose and responsibilities}
{Extracted from file-level NICE marker @desc if available}

## Intent Blocks
List of all NICE markers in this module for quick reference:

- `{uid}` - **{intent_type}**: {brief_description} (Line {start}-{end})
- `{uid}` - **{intent_type}**: {brief_description} (Line {start}-{end})
- ...

## Navigation Map

### Dependencies
This module depends on:
- `{dependency_uid}` → {description} ({file_path})
- ...

### Dependents
This module is used by:
- `{dependent_uid}` ← {description} ({file_path})
- ...

## API Reference

### {function_name}
**Location:** Line {X}-{Y}
**UID:** `{nice_uid}`
**Intent Type:** {ENTRY|FLOW|LOGIC|etc.}

**Description:**
{Extracted from @desc tag}

**Signature:**
```{language}
{actual_function_signature}
```

**Inputs:**
{Extracted from @inputs tag, formatted as bullet list}

**Outputs:**
{Extracted from @outputs tag}

**Constraints:**
{Extracted from @constraints, @pre, @post tags}
- Pre-conditions: {from @pre}
- Post-conditions: {from @post}
- Rules: {from @constraints}

**Expected Failures:**
{Extracted from @fail tag}
- {failure_mode_1}: {description}
- {failure_mode_2}: {description}

**Agent Permissions:** {read|extend|refactor|forbidden}
**Change Safety:** {cosmetic|local|structural|systemic}

---

{Repeat for each public function/class with NICE marker}

## Constraints Summary
Key constraints that apply across this module:
- {constraint_1}
- {constraint_2}

## Change History
- {YYYY-MM-DD} - {sprint_name}: {change_summary}
- {YYYY-MM-DD} - {sprint_name}: {change_summary}

---

## Notes
{Any additional context, known issues, or future plans}

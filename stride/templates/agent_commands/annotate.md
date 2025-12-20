# `/stride:annotate` Command

## Purpose
Scan codebase to identify logical units and generate `SPEC.md` files for documentation and agent understanding.

## Workflow

### 1. Analysis Phase
- Scan the entire project to identify high-level modules and components.
- Identify logical units (directories with significant logic).
- Analyze existing NICE markers to understand intent.

### 2. Root SPEC Creation
- Create or update `SPEC.md` in the project root.
- This file serves as the **System Map**.
- It must contain:
  - **System Overview**: High-level purpose of the application.
  - **Module Index**: A structured list of links to all module-level `SPEC.md` files (e.g., `- [Auth Module](src/auth/SPEC.md)`).
  - **Global Constraints**: Rules that apply to the whole system.

### 3. Module SPEC Generation
- For each identified module/directory, generate a `SPEC.md` inside that directory.
- Module `SPEC.md` must contain:
  - **Module Purpose**: Specific responsibility of this directory.
  - **Public Interface**: Key classes/functions exposed to other modules.
  - **Dependencies**: What it relies on.
  - **NICE Markers**: List of relevant markers found in the code.
  - **Back Link**: A link back to the Root `SPEC.md`.

### 4. Reporting Phase
- Display summary of the Spec network created.
- List any areas that might need manual review.

## Arguments
- `path` (optional) - Specific file/directory to scan. Defaults to entire project.

## Safety Rules
- Do not overwrite existing `SPEC.md` content without checking for conflicts.
- Preserve manual edits in `SPEC.md` if possible (append or update specific sections).
- Do not modify source code files (only generate documentation).

## Example Usage
```
/stride:annotate src/auth
/stride:annotate
```

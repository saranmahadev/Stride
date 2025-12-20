# NICE Marker Guide for AI Agents

## Overview
NICE (Navigation and Intent Context Engine) markers are semantic annotations embedded in source code comments that enable deterministic AI navigation, intent-safe refactoring, and constraint-aware reasoning.

## Marker Structure
All NICE markers follow this pattern using the host language's single-line comment syntax:

[comment] @intent <TYPE> <ID>
[comment] @uid <UNIQUE_IDENTIFIER>
[comment] @desc <DESCRIPTION>
[comment] @[TAG] <VALUE>
[comment] @end

## Mandatory Tags
- @intent <TYPE> <ID> - Declares intent category and human-readable identifier
- @end - Closes the intent block

## Intent Types
Choose the appropriate type based on code responsibility:

- ENTRY: Execution entry points (APIs, main functions, request handlers)
- FLOW: Orchestration across multiple components (coordinators, workflows)
- LOGIC: Core business rules or algorithms (calculations, validations)
- TRANSFORM: Data transformation or normalization (mappers, serializers)
- IO: External boundaries (database, filesystem, network, APIs)
- STATE: Persistent or shared state (stores, caches, sessions)
- UI: Presentation or layout logic (components, templates)
- INVARIANT: Rules that must never be violated (constraints, contracts)
- HOTSPOT: Performance-critical regions (tight loops, heavy computation)
- EXPERIMENT: Safe-to-change exploratory logic (feature flags, A/B tests)
- DEPRECATED: Legacy logic marked read-only (scheduled for removal)

## Recommended Tags

### Identity & Description
- @uid <IDENTIFIER> - Immutable global identifier
  Format: nice:{type}:{domain}:{id}:v{version}
  Example: nice:logic:auth:token_verify:v1

- @alias <NAME> - Alternate human-facing name
  Example: @alias verifyJWT

- @desc <TEXT> - Single-line explanation of purpose
  Example: @desc Validates JWT token signature and expiration

### Functional Semantics
- @scope <BOUNDARY> - Responsibility boundary
  Example: @scope module-level, function-level, class-level

- @inputs <LIST> - Logical inputs (comma-separated)
  Example: @inputs token:string, publicKey:string

- @outputs <RETURN> - Logical outputs
  Example: @outputs TokenClaims | ValidationError

- @depends <DEPS> - Dependencies with strength
  Format: [strength:]<uid>
  Example: @depends hard:nice:io:db:user_repo:v1

### Constraints & Contracts
- @constraints <RULES> - Non-negotiable rules
  Example: @constraints token must be non-empty, signature must match

- @pre <CONDITION> - Pre-condition
  Example: @pre token is valid JWT format

- @post <CONDITION> - Post-condition
  Example: @post returns claims if valid, throws error if invalid

- @fail <MODES> - Expected failure modes
  Example: @fail TOKEN_EXPIRED, INVALID_SIGNATURE, MALFORMED_TOKEN

### Governance & Safety
- @agents <PERMISSION> - Allowed agent actions
  Values: read | extend | refactor | forbidden
  Example: @agents refactor

- @change_safe <LEVEL> - Allowed change radius
  Values: cosmetic | local | structural | systemic
  Example: @change_safe local

- @forbid <OPERATIONS> - Explicitly forbidden operations
  Example: @forbid delete, rename without migration

### Temporal Context
- @introduced <DATE> - When this intent was added
  Example: @introduced 2025-01-20

- @expires <DATE> - Planned removal date
  Example: @expires 2025-12-31

- @reason <TEXT> - Why it exists in current form
  Example: @reason Temporary workaround for legacy API compatibility

## UID Generation Pattern
UIDs must follow this deterministic pattern:

nice:{type}:{domain}:{id}:v{version}

Components:
- type: Lowercase intent type (entry, flow, logic, etc.)
- domain: Functional domain (auth, payment, analytics, etc.)
- id: Specific identifier (token_verify, create_order, etc.)
- version: Integer version number (1, 2, 3, etc.)

Examples:
- nice:entry:api:user_login:v1
- nice:logic:payment:calculate_tax:v2
- nice:io:db:user_repository:v1
- nice:flow:checkout:process_order:v1

## When to Add Markers

### Always Mark
- All API entry points (controllers, handlers, routes)
- Core business logic functions
- Database/external system interactions
- State management functions
- Security-critical code paths
- Performance hotspots

### Optional
- Pure utility functions (formatDate, isEmpty, etc.)
- Simple getters/setters without logic
- Auto-generated code
- Test helper functions

## Marker Examples by Language

### TypeScript
// @intent LOGIC token_verification
// @uid nice:logic:auth:token_verify:v1
// @desc Validates JWT token signature and expiration
// @inputs token:string, publicKey:string
// @outputs TokenClaims | ValidationError
// @pre token is non-empty and well-formed
// @post returns claims if valid, throws if invalid
// @constraints signature must match, token not expired
// @agents refactor
// @change_safe local
// @fail TOKEN_EXPIRED, INVALID_SIGNATURE, MALFORMED_TOKEN
// @end
export function verifyToken(token: string, publicKey: string): TokenClaims {
  // Implementation
}

### Python
# @intent IO database_query
# @uid nice:io:db:user_find:v1
# @desc Retrieves user by ID from database
# @inputs user_id:int
# @outputs User | None
# @depends hard:nice:io:db:connection_pool:v1
# @constraints user_id must be positive integer
# @agents extend
# @change_safe local
# @end
def find_user_by_id(user_id: int) -> Optional[User]:
    # Implementation

### Java
// @intent ENTRY api_endpoint
// @uid nice:entry:api:create_user:v1
// @desc REST endpoint for user creation
// @inputs UserCreateRequest
// @outputs UserResponse | ErrorResponse
// @constraints email must be unique, password min 8 chars
// @agents read
// @change_safe structural
// @fail DUPLICATE_EMAIL, WEAK_PASSWORD, VALIDATION_ERROR
// @end
@PostMapping("/users")
public ResponseEntity<UserResponse> createUser(@RequestBody UserCreateRequest request) {
    # Implementation
}

## Agent Workflow During Implementation

1. **Before Writing Code:**
   - Determine intent type based on code responsibility
   - Plan UID following naming convention
   - Identify required tags based on function contract

2. **After Writing Code:**
   - Add NICE marker block immediately above function/class
   - Fill all relevant tags based on implementation
   - Ensure @agents permission matches code safety level
   - Set @change_safe based on impact radius

3. **During Code Review:**
   - Verify all new/modified functions have markers
   - Check UID uniqueness and convention compliance
   - Validate @depends references exist
   - Ensure @constraints are testable

## SPEC.md Integration
NICE markers are the source of truth for SPEC.md generation. After adding markers:
1. Extract all markers from module
2. Group by intent type
3. Generate navigation map from @depends
4. Create API reference from @inputs/@outputs
5. Document constraints and safety levels

## Validation Rules
- @intent and @end are mandatory
- @uid should follow nice:{type}:{domain}:{id}:v{N} pattern
- @uid must be unique across project
- @depends references must point to existing UIDs
- @agents must be one of: read, extend, refactor, forbidden
- @change_safe must be one of: cosmetic, local, structural, systemic

## Anti-Patterns to Avoid
- [FAILED] Adding markers to trivial utility functions (formatDate, isEmpty)
- [FAILED] Using generic IDs like "function1", "handler"
- [FAILED] Omitting @uid (makes navigation impossible)
- [FAILED] Copy-pasting markers without updating UID
- [FAILED] Using @agents forbidden without strong justification
- [FAILED] Incomplete @inputs/@outputs (missing types)
- [FAILED] Non-testable @constraints (vague rules)

## Summary
NICE markers transform code from unstructured text into a navigable semantic graph. Always add markers to significant code blocks during implementation, follow UID conventions strictly, and use tags to document contracts, constraints, and governance rules.

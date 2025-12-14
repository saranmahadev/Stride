# Stride Product Roadmap

**Repo-First, CLI-Native, Agent-Centric Work Orchestration**

## Vision

Stride is a **repo-native work orchestration system** that scales from a solo developer to a regulated enterprise **without rewrites, migrations, or lock-in**.
The repository remains the source of truth at every phase. Infrastructure is optional. AI collaboration is foundational, not bolted on.

---

## Phased Scaling Strategy

| Version  | Focus                         | Target Users          | Timeline   |
| -------- | ----------------------------- | --------------------- | ---------- |
| **v1.0** | Solo workflows                | Individual developers | Now        |
| **v1.1** | Navigation & context          | All users             | Q1 2025    |
| **v1.5** | Repo-based teams              | Small teams (2–10)    | Q1–Q2 2025 |
| **v1.8** | Cloud-optional teams          | Medium teams (10–50)  | Q3–Q4 2025 |
| **v2.0** | Enterprise scale              | Large orgs (50+)      | 2026       |

Stride evolves **linearly**, not disruptively. Each phase builds on the previous one with no breaking changes.

---

## Core Principles (Non-Negotiable)

* **Repo-First**
  All state lives in `.stride/`, fully Git-versioned and portable.

* **CLI-Native**
  Terminal is the primary interface. GUI is optional and non-authoritative.

* **Dual Collaboration Model**

  * Human ↔ AI Agent
  * Human ↔ Human
    Both are first-class.

* **Graceful Scaling**
  Solo → Team → Enterprise with no rewrites or migrations.

* **Privacy by Default**
  Offline-first. Cloud is explicitly opt-in.

* **Zero Lock-In**
  Sprint data functions without Stride infrastructure.

---

## Phase 2: Repo-Based Team Collaboration (v1.3–v1.5)

**Target:** Small teams using Git as the synchronization layer
**Infrastructure:** None

### 1. Team Initialization (v1.3)

* `stride team init` generates `.stride/team.yaml`
* Defines members, roles, and policies
* AI-assisted role suggestions derived from `project.md`

### 2. Member Management (v1.4)

* `stride team add | remove | edit`
* Role-based permissions enforced in the CLI
* Git-based onboarding (clone repo to join)

### 3. Assignment & Workflow (v1.4)

* `stride assign` with AI-suggested assignees
* Sprint metadata: ownership, approvals, workflow state
* Approval gates (N required reviewers)
* AI-assisted workload balancing

### 4. Comments & Communication (v1.5)

* Threaded comments on files and lines
* Sprint-scoped discussion
* Feedback loop for AI learning
* Stored in `.stride/sprints/<ID>/.comments.yaml`

**Outcome:**
Teams collaborate entirely via Git. No servers. No SaaS dependency.

---

## Phase 3: Cloud-Optional Hybrid Collaboration (v1.6–v1.8)

**Target:** Medium teams requiring real-time collaboration
**Infrastructure:** Optional, user-controlled

### Cloud Opt-In (v1.6)

* `stride cloud init` enables cloud sync
* Local daemon syncs `.stride/` ↔ Supabase backend
* Fully offline-capable; syncs opportunistically

### Real-Time Presence & Co-Editing (v1.6)

* Live cursors and presence indicators
* Operational transformation for concurrent edits
* No file locking required

### Electron Desktop Application (v1.7)

* Optional GUI for non-CLI users
* Kanban boards, visual sprint editors, analytics
* Reads and writes the same `.stride/` files as the CLI

### Team Dashboards (v1.7)

* Burndown charts and velocity tracking
* Dependency and workflow graphs
* AI-generated insights and trend analysis

### External Integrations (v1.8)

* Slack and Microsoft Teams webhooks
* GitHub PR automation
* CI/CD pipeline triggers
* Custom outbound webhooks

**Outcome:**
Real-time collaboration without surrendering repo ownership or offline capability.

---

## Phase 4: Enterprise Scale (v1.9–v2.0)

**Target:** Large organizations and regulated environments

### Enterprise Capabilities

* Multi-tenancy: Organization → Division → Team
* SSO (SAML, OIDC)
* Advanced RBAC and immutable audit logs
* REST and GraphQL APIs
* On-premise deployment (Docker, Kubernetes)
* Compliance: SOC 2, GDPR, HIPAA
* BI and data warehouse exports

**Outcome:**
Enterprise-grade governance without abandoning the repo-first model.

---

## Human–Agent Collaboration Matrix

| Capability    | v1.0            | v1.5       | v1.8            | v2.0           |
| ------------- | --------------- | ---------- | --------------- | -------------- |
| Human ↔ Agent | Yes (20 agents) | Same       | Same            | Same           |
| Human ↔ Human | No              | Git-based  | Real-time       | Multi-org      |
| Agent ↔ Agent | Single          | Sequential | Parallel        | Orchestrated   |
| Assignment    | Self            | Manual     | AI-suggested    | Auto-optimized |
| Reviews       | Self            | Peer       | Peer + AI       | Policy-driven  |
| Communication | Logs            | Comments   | Chat & presence | Full suite     |

---

## Agent Orchestration (Planned v1.6+)

Multiple AI agents collaborate on a single sprint, each owning distinct strides.

### Capabilities

* Parallel agent execution
* Explicit stride ownership
* Context-aware handoffs
* AI-to-AI conflict resolution

### Example Commands

```bash
stride agent assign SPRINT-A3F2E --agent claude --strides 1,2
stride agent-handoff SPRINT-A3F2E --from claude --to cursor --stride 3
stride agent status SPRINT-A3F2E
```

---

## Architecture Evolution

### v1.5 – Repo-Only

* `.stride/` + Git
* Zero infrastructure
* Fully portable

### v1.8 – Cloud-Optional

* `.stride/` + sync daemon + Supabase
* Real-time collaboration
* Offline-first preserved

### v2.0 – Enterprise

* Multi-tenant database
* API gateway and SSO
* On-premise deployment option

---

## Pricing Strategy

### Free Tier (v1.0–v1.5)

* Unlimited sprints and team members
* Full CLI functionality
* 20 AI agents
* No cloud or integrations

### Team Plan (v1.6–v1.8) — **$15/user/month**

* Cloud sync
* Desktop and web dashboards
* Integrations
* Advanced analytics

### Enterprise (v2.0)

* Custom pricing
* Multi-tenancy, SSO, RBAC
* On-prem deployment
* SLA and dedicated support

---

## Strategic Differentiation

Stride is not another Jira clone.

* Cloud is optional, not mandatory
* The repo remains the source of truth
* CLI-first at every stage
* Seamless scaling with no migrations
* AI collaboration is native, not auxiliary
* Zero vendor lock-in

**Stride competes with Jira, Linear, and Azure DevOps by refusing to become them.**

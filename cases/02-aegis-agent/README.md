# Aegis Agent

**Status:** `1.0.0-rc1 · local-first multi-agent cognitive twin`

Aegis Agent is a local-first multi-agent cognitive twin at release candidate 1.0.0-rc1, requiring human approval for consequential actions.

## What It Is

A multi-agent system running locally that acts as a cognitive twin. Human approval gates are required before high-impact actions execute. At release candidate stage.

## What It Is Not

- Not hosted multi-tenant SaaS.
- Not a fully autonomous system.
- Not a production-released product (rc1 status).

## Problem

Local AI agent systems that act without human oversight create risk. Aegis Agent is designed with explicit human approval gates to keep consequential decisions under human control.

## Scope

Local-first deployment. Multi-agent cognitive workflows. Human-in-the-loop approval gate as a first-class architectural constraint.

## Architecture

Multi-agent coordination layer with an explicit human approval gate required before consequential actions. Local-first: no cloud dependency for core operation.

## Engineering Decisions

- Local-first architecture to avoid multi-tenant hosting concerns.
- Human approval gate enforced by design, not convention.
- rc1 status: feature-complete candidate, not yet full release.

## Stack

Documented in the source repository.

## Testing

Refer to the source repository for current test coverage and status.

## Deployment Model

Local-first. A live demo endpoint is available for evaluation.

## Live Links

| Resource | URL |
|----------|-----|
| Live | https://aegis-agent-haka.onrender.com |
| Docs | https://aegis-agent-haka.onrender.com/docs |

## Technical Evidence

Refer to the source repository.

## Measurable Results

No results claimed beyond what is evidenced in the source repository.

## Source Repository

https://github.com/aminazimi42-coder/aegis-agent

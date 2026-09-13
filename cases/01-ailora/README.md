# AILORA

**Status:** `Production-Grade Candidate · Active Qualification`

AILORA is an AI system that has reached production-grade candidate status and is currently undergoing active qualification.

## What It Is

A software system tracking through a formal qualification process toward production readiness, with a published status contract and live endpoints under active evaluation.

## What It Is Not

- Not Production-Ready.
- Not Production-Qualified.
- Not an IBM product.

## Problem

Building AI systems to production-grade standards requires a verifiable qualification process — not just a working prototype. AILORA defines and tracks that process explicitly.

## Scope

Qualification of a candidate AI system: implementation evidence, test evidence, deployment evidence, security review, and operational evidence, gated by a published status contract.

## Architecture

Live API with docs and health endpoints. Qualification gates tracked in `docs/qualification/status-contract.md` within the source repository.

## Engineering Decisions

- Explicit status naming (`Production-Grade Candidate · Active Qualification`) to prevent premature production claims.
- Public status contract published in source repository for accountability.
- Release tag marks the candidate build: `candidate-2026-08-29`.

## Stack

Documented in the source repository.

## Testing

Evidence tracked as part of qualification gates. Refer to the source repository for current test status.

## Deployment Model

Hosted on Render. Live endpoints verified at qualification time.

## Live Links

| Resource | URL |
|----------|-----|
| Live | https://ailora-web.onrender.com |
| Docs | https://ailora-web.onrender.com/docs |
| Health | https://ailora-web.onrender.com/health/live |
| Demo | https://youtu.be/_zB-dZruUbE |

## Technical Evidence

| Evidence | Location |
|----------|----------|
| Status contract | `docs/qualification/status-contract.md` in source repo |
| Release tag | https://github.com/azimilab2025-ai/ailora/releases/tag/candidate-2026-08-29 |

## Measurable Results

Tracked within the qualification process. No results claimed beyond what the status contract documents.

## Source Repository

https://github.com/azimilab2025-ai/ailora

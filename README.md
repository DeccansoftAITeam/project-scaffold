# Deccansoft Project Scaffold

The **standard template repository** from Deccansoft SDLC v2 (P2 Scaffold). Every new project is generated from it, so every practice is in place on day one ("nothing is adopted per project"). It is a [Copier](https://copier.readthedocs.io) template: projects can pull later scaffold releases with `copier update`.

Owner: Platform/Standards Owner. Released as SemVer tags.

## Generate a project

```sh
uvx copier copy --trust --vcs-ref v1.0.0 gh:DeccansoftAITeam/project-scaffold my-project
```

Or let the agent do it with the `scaffold` skill from [`agent-bundle`](https://github.com/DeccansoftAITeam/agent-bundle), which derives the answers from `docs/constitution.md`.

Prerequisites: git, Python 3.12+, uv, Node 22+, pnpm, Docker, access to `DeccansoftAITeam/agent-bundle`.

## What you get (v1.0.0)

| Area | Contents | Standard |
|---|---|---|
| Layout | pnpm + Nx monorepo: `backend/`, `apps/web`, `packages/core`, `infra/`, `prompts/`, `docs/` | AD-01 |
| Backend | FastAPI, SQLAlchemy 2 async, Alembic (owner role), pydantic-settings, Problem Details errors, OTel, `/healthz` + `/readyz` | AD-02, AD-19 |
| Multi-tenancy | `tenant_session()` (SET LOCAL `app.tenant_id`), `TenantOwned` mixin, `enable_rls()` migration helper, separate owner and runtime roles (NOBYPASSRLS) | ADR template |
| Tests | Health, Problem Details, **RLS isolation tests** (runtime role can't read or write another tenant, can't disable RLS), **architecture tests** (no SQL in routers, no cloud SDK in domain code, every `tenant_id` table has forced RLS, file length) | AD-09 |
| Web | Next.js 16 + TypeScript + Vitest; `/api` proxied to the backend | — |
| Local DB | `docker compose up -d db` (Postgres 17 + pgvector, roles from `db/init/`) | — |
| LOCAL gate | `.pre-commit-config.yaml`, **auto-installed**: gitleaks, ruff, hygiene, conventional commits; pre-push: mypy strict, tests + 80% coverage, Nx affected typecheck/test, squawk, file length, public env check (~45 s warm) | AD-08 |
| PR gate | `.github/workflows/pr-gate.yml` (v1 subset: hygiene, backend, web) | P5 |
| Agent guardrails | `.claude/settings.json` (deny/ask lists, bundle plugin pinned), `.vscode/settings.json` (Copilot terminal rules), `CODEOWNERS` | 03 |
| Agent bundle | Post-generation install of `agent-bundle` at a pinned ref (skills, org rules, Copilot agents and hooks) | L1–L5 |
| Docs | All SDLC templates in `docs/templates/`; `AGENTS.md` skeleton | — |

## Roadmap (added by later releases, pulled with `copier update`)

| Release | Adds | Course module |
|---|---|---|
| v1.1 | Full PR gate: contract tests, migration safety, mutation, security, e2e-smoke, agent attribution, conformance | M6 |
| v1.2 | Preview environments + `infra/` (OpenTofu, Azure Container Apps) | M6 |
| v1.3 | Nightly + weekly workflows, unattended agent jobs | M8 |
| v1.4 | Release workflow (release-please, signing, SBOM), deploy scripts | M9–M10 |

## Developing the scaffold

Generate into a scratch folder and run the gate:

```sh
uvx copier copy --trust --defaults -d project_name=Demo -d description=Demo -d github_owner=me . ../_gen
cd ../_gen && docker compose up -d db && git add -A && git commit -m "chore: scaffold" \
  && uvx pre-commit run --hook-stage pre-push --all-files
```

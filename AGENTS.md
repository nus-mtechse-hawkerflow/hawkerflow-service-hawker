# AGENTS.md

Welcome! This document provides essential instructions, architectural context, and coding conventions for AI agents working in this repository (`hawkerflow-service-hawker`).

---

## 🚨 MANDATORY AGENT DIRECTIVE: Check `graphify-out/` First

**BEFORE answering any questions about architecture, cross-module dependencies, data flows, entity relationships, or system design, you MUST inspect the pre-built knowledge graph in `graphify-out/`.**

- **Primary Graph Artifacts:**
  - `graphify-out/graph.json`: Complete knowledge graph containing all extracted AST symbols, documents, relations, and clusters.
  - `graphify-out/GRAPH_REPORT.md`: Architectural summary including god nodes, cross-module bridges, cluster cohesion, and surprising connections.
  - `graphify-out/graph.html`: Visual interactive map of the codebase architecture.
- **Querying the Graph:**
  - Run `graphify query "<question>"` (or use NetworkX traversal over `graphify-out/graph.json`) to trace paths, verify callers/callees, and understand component relationships.
  - Use `/graphify path "<SourceNode>" "<TargetNode>"` to find structural coupling between services or components.
  - When changes are made to the codebase, update the graph using `/graphify . --update` or re-run `/graphify .`.

---

## 🏗️ Project Architecture & Directory Structure

`hawkerflow-service-hawker` is a FastAPI-based microservice designed for the HawkerFlow ecosystem, following a **Layered Clean Architecture** pattern.

```
.
├── .github/
│   └── workflows/
│       └── ci.yml               # CI pipeline (Ruff, Pytest, Pip-Audit, Bandit, Gitleaks, SAM validate)
├── docs/                        # Specifications, local dev runbooks, proposals, and openapi.yaml
├── graphify-out/                # Persisted knowledge graph, reports, and visualizer
├── infra/
│   ├── SECURITY_BASELINE.md     # Infrastructure security baseline documentation
│   └── template.yaml            # AWS SAM serverless infrastructure definition
├── resources/
│   └── config.yml               # Application configuration file
├── src/
│   ├── configurations/          # Pydantic Settings & YAML configuration loader
│   │   ├── app_config.py        # AppConfig (Pydantic BaseSettings with YAML source)
│   │   └── datasource.py        # Datasource model definition
│   ├── drivers/                 # Database driver abstractions
│   │   ├── driver.py            # Abstract Driver base class (ABC)
│   │   ├── postgres_driver.py   # PostgreSQL engine driver implementation
│   │   └── sqlite_driver.py     # SQLite engine driver implementation
│   ├── factory/                 # Factory pattern implementations
│   │   ├── database_factory.py  # Database connection/engine factory
│   │   └── driver_factory.py    # Driver resolution factory
│   ├── entities/                # SQLModel database table definitions (ORM)
│   │   ├── stalls.py            # Stalls table entity
│   │   ├── stall_menu.py        # StallMenu table entity
│   │   └── stall_owner.py       # StallOwner table entity
│   ├── models/                  # Pydantic API DTOs and request/response schemas
│   │   └── hawker_details.py    # HawkerDetails schema
│   ├── repository/              # Data access layer
│   │   └── hawker_repository.py # Repository for database CRUD operations
│   ├── session/                 # Database session lifecycle
│   │   └── db_session.py        # DBSession context manager & engine binding
│   ├── hawker_service/          # Business logic service layer
│   │   └── hawker_service.py    # Core domain orchestration
│   ├── endpoints/               # FastAPI routing & presentation layer
│   │   └── hawker_routes.py     # APIRouter definitions and route handlers
│   ├── lifecycle/               # Application startup and teardown lifespans
│   │   └── lifespan.py          # FastAPI lifespan context manager & table creation
│   └── main.py                  # Application entry point & HawkerFlowCustomer bootstrapper
├── tests/                       # Pytest unit and integration test suite
├── pyproject.toml               # Tool configuration (Ruff, Pytest)
├── requirements.txt             # Production runtime dependencies
└── requirements-dev.txt         # Development and CI dependencies
```

### Architectural Layering & Data Flow

```
[HTTP Request]
      │
      ▼
Endpoints (`src/endpoints/`)
      │  (DTOs / Schemas in `src/models/`)
      ▼
Hawker Service (`src/hawker_service/`)
      │
      ▼
Repository Layer (`src/repository/`)
      │  (ORM Entities in `src/entities/`)
      ▼
DB Session & Factory (`src/session/`, `src/factory/`, `src/drivers/`)
      │
      ▼
[Database (SQLite / PostgreSQL)]
```

---

## 🎨 Code Style & Standards

### 1. Python Version & Environment
- **Python Version**: Python 3.12+
- **Virtual Environment**: Always use the virtual environment at `.venv` (`source .venv/bin/activate`).

### 2. Formatting & Linting
- Configuration is declared in `pyproject.toml`.
- **Linter & Formatter**: [Ruff](https://github.com/astral-sh/ruff)
- **Line Length**: `110` characters.
- **Target Version**: `py312`.
- **Lint Rules Enabled**:
  - `E`, `W`: pycodestyle errors and warnings
  - `F`: Pyflakes (undefined names, unused imports)
  - `I`: isort (import ordering)
  - `B`: flake8-bugbear (common design flaws and bugs)
- Run `ruff check .` before submitting any changes.

### 3. Type Annotations & Schemas
- Use explicit type hints everywhere for function parameters and return types.
- Use Python 3.10+ modern union syntax (e.g. `str | None` instead of `Optional[str]`, `list[str]` instead of `List[str]`).
- Use **Pydantic V2 / SQLModel** for data validation, serialization, and ORM entity mapping.

### 4. Layer Isolation & Dependency Injection
- Keep endpoints thin; delegate all business logic to `HawkerService`.
- Keep database queries confined within `HawkerRepository`.
- Use FastAPI `Depends()` for dependency injection (e.g., injecting service and repository instances).

### 5. Error Handling & Security
- Never hardcode secrets, credentials, or connection strings.
- Pass secrets via environment variables mapped through `AppConfig`.
- Maintain clean input validation on all API endpoints.

---

## 🛠️ Common Developer & Agent Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests
pytest -q

# Run lint checks
ruff check .

# Run security / vulnerability checks
pip-audit -r requirements-dev.txt
bandit -r src

# Start service locally
python src/main.py

# Re-index knowledge graph after code changes
/graphify . --update
```

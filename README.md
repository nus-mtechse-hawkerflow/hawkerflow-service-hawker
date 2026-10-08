# hawkerflow-service-hawker

The HawkerFlow **hawker service**: registers a hawker and their stall, lists
stalls and menus for diners, and looks up the stall a signed-in hawker owns.

FastAPI + SQLModel on PostgreSQL. The other HawkerFlow services (order,
customer, analytics) and the two web apps (`hawker-ui`, `diner-ui`) live in
their own repositories.

## API

Served under `/hawker` on port 8080.

| Method | Path | Purpose |
|---|---|---|
| POST | `/hawker/v1/hawker/register` | Register a hawker and their stall |
| GET | `/hawker/v1/hawker/stalls` | List stalls and menus |
| GET | `/hawker/v1/hawker/me/stall/{hawker_sub}` | The stall owned by a Cognito user |
| GET | `/hawker/health` | Health check used by the load balancer |

## Data model

Tables `stalls`, `stall_menu` and `stall_owner`, created at startup in the
shared `hawkerflow` database.

## Configuration

`resources/config.yml` holds the service settings. The database host, port,
name, user and password come from the `DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USERNAME` and `DB_PASSWORD` environment variables.

## Deployment

The service runs on ECS Fargate behind API Gateway and an internal load
balancer, defined in the `hawkerflow-terraform` repository. To release a
change, run from that repository:

```bash
./scripts/release-service.sh hawker ../hawkerflow-service-hawker
```

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

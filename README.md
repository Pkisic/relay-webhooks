# Relay

Self-hosted toolkit for debugging webhook integrations. Relay gives you a URL that captures any inbound HTTP request, streams it live, and lets you replay it against another target, so you can see exactly what a third-party provider sends and how your service reacts.

> **Status:** early development. The application skeleton (configuration, app factory, health endpoint, test and quality tooling) is in place. The features below are planned; see the [roadmap](ROADMAP.md) for progress.

## Planned features (MVP)

- **Capture** – create endpoints and record every request (method, headers, query, body, source, timing).
- **Live feed** – watch requests arrive in real time over Server-Sent Events.
- **Configurable responses** – choose the status code, body and delay an endpoint returns, to test how a sender handles failures and retries.
- **Replay** – re-send a captured request to any target URL, optionally modified, with retries and a full attempt log.
- **Signature verification** – check HMAC signatures for common providers and see why a signature fails.

## Stack

- **Current:** Python 3.13, FastAPI, Pydantic v2, pytest, ruff, mypy
- **Planned:** PostgreSQL, SQLAlchemy 2.0 (async), Alembic, Redis, Docker Compose

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (manages the Python version and dependencies)
- GNU Make

uv installs the Python version pinned in `.python-version` automatically.

### Install and run

```bash
make install            # install locked dependencies
cp .env.example .env    # local configuration (not committed)
make dev                # start the API with auto-reload
```

The API listens on `http://127.0.0.1:8000`. Interactive API documentation is served at `/docs` (Swagger UI), and the liveness probe at `GET /health`.

To use a different address: `make dev HOST=0.0.0.0 PORT=9000`.

### Configuration

Settings are read from environment variables prefixed with `RELAY_`, or from a `.env` file in the project root. Invalid values fail at startup.

| Variable | Default | Description |
|---|---|---|
| `RELAY_APP_NAME` | `Relay` | Title shown in the API documentation |
| `RELAY_ENVIRONMENT` | `development` | One of `development`, `testing`, `production` |
| `RELAY_DEBUG` | `false` | Enable framework debug mode |
| `RELAY_LOG_LEVEL` | `INFO` | One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

## Development

All common tasks are available through `make`. Run `make help` to list them.

| Command | Description |
|---|---|
| `make install` | Install locked dependencies |
| `make dev` | Run the API with auto-reload |
| `make lint` | Lint with ruff |
| `make format` | Format code and apply safe lint fixes |
| `make format-check` | Verify formatting without changing files |
| `make typecheck` | Type-check with mypy (strict) |
| `make test` | Run the test suite |
| `make check` | Run lint, format check, type check and tests in order |
| `make build` | Build the sdist and wheel |

`make check` is the quality gate; run it before every commit. Commands run with `uv run --locked`, so they fail if `uv.lock` is out of date with `pyproject.toml`. After changing dependencies, run `uv lock` and commit the updated lockfile.

### Project layout

```
src/relay/
  main.py          application factory and lifespan
  config.py        typed settings
  api/             HTTP routers
tests/             test suite
```

## Documentation

- [Roadmap](ROADMAP.md)

## License

Released under the [MIT License](LICENSE).

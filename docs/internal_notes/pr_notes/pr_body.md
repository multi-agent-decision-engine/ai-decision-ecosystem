### What
- Adds detailed simulation endpoint returning round-by-round agent transcript.
- Serves lightweight dashboard at /ui and updates UI to render transcript.
- Pins LangChain deps to avoid pip backtracking during Docker image build.

### How to test
- Run: `python -m pytest tests/test_api_scenario_get_endpoints.py tests/test_agent_message_schema.py tests/test_aggregator.py tests/test_classifier.py -q`
- Start: `docker compose up --build -d` then open http://localhost:8000/ui

### Notes
- DB migrations in container: `python -m alembic upgrade head`

.PHONY: start

start:
	./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
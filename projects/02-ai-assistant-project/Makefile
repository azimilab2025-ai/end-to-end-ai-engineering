.PHONY: install run test check up down logs

install:
	python3 -m pip install -r apps/api/requirements.txt

run:
	PYTHONPATH=apps/api uvicorn app.main:app --reload

test:
	PYTHONPATH=apps/api pytest -q apps/api/tests

check:
	python3 -m compileall -q apps/api/app apps/api/tests apps/api/migrations

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f api

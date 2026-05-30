# Linux / macOS 向けショートカット（Windows は bat/ を使用）
export PYTHONPATH := src

.PHONY: test health screening analyze publish help

help:
	@echo "Targets: test health screening analyze publish analyze-publish screening-notify"

test:
	pytest -q

health:
	python src/kaburadar/cli/healthcheck.py --require-db

screening:
	bash sh/screening.sh

analyze:
	bash sh/analyze.sh

publish:
	bash sh/publish.sh

analyze-publish:
	bash sh/analyze_and_publish.sh

screening-notify:
	bash sh/screening_notify.sh

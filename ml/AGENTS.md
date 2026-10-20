# Python ML/LLM

Соблюдать корневой AGENTS.md и docs/adaptation.md. Павел владеет retrieval/ranking/eval (docs/agents/r2-ml.md); Денис — адаптером LLM, анализом и verification (docs/agents/r5-infra.md). Общие server/handlers/schemas и pyproject/uv.lock согласовать до редактирования. Единственная машина состояний run находится в Go, Python возвращает план/результаты/verification gaps. Не загружать legacy ruBERT/SBERT по умолчанию в новом пути; их допустимость не подтверждена. Все LLM-вызовы через один проверяемый allowlist и бюджетный адаптер.

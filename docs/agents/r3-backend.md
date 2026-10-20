# R3 — Роман Шваров: Go API и собственная агентная оркестрация

## Что изучить

AGENTS.md, architecture, contracts, security; `backend/internal/app/app.go`, `backend/internal/controller/http/v1/router.go`, `backend/internal/analytics/worker.go`, usecase/repo/client. Не переписывать Go на FastAPI. Текущий сбор → relevance → sentiment не выполняет нужный цикл PLAN/tools/context/VERIFY.

## Владение

`backend/internal/insights/`, новые controller/usecase/client для runs, API middleware, RunContext и трасса. Entity/repo/migrations координировать с Романом Аксеновым. Python adapter и бюджет вызовов — Денис; Go владеет общим состоянием run и его лимитами.

## A1 — контракт и вертикальный mock

Согласовать CompanyContext/RunContext/Insight и OpenAPI с командой, выложить shared fixtures. Добавить list/context companies, POST analysis-runs (202 + idempotency key), GET run, source details и feedback по contracts.md. Typed mock за внутренним интерфейсом, обязательный признак mock. Не удалять сразу legacy routes.

Готовность: общий fixture проходит API→UI; queued/running/completed/partial/failed, одинаковый idempotency key не создаёт дубли; errors без stack trace. Тестировать поведение и права, не только DTO.

## A2 — машина состояний

Реализовать PLAN→PROFILE→RETRIEVE→RANK→ANALYZE→VERIFY и ветку уточнённого поиска; max 2 analysis attempts, deadline/tool limits, контекст/источники/история шага на run. Валидировать модельный план перед tool call. Все Python-вызовы через согласованный клиент с timeout/request id. После исчерпания — PARTIAL/FAILED с причиной, не бесконечный retry.

Готовность: инструментальная трасса и кейс реального повторного поиска; сохранённый контекст между шагами; недоступность LLM не теряет собранные материалы. Не переносить старый full cross-product news×brands на большие LLM-вызовы.

## A3 — доступ и надёжность

Привязать тестовую сессию к разрешённым company IDs; проверить доступ к company, run, sources, cache и связям, scope не доверять из тела запроса. Legacy mock endpoint и инфраструктурные маршруты закрыть/отключить в режиме защиты. Read-only tools, без произвольного URL/shell. Централизованный LLM-budget не дублировать независимым счётчиком в Go.

## Первый prompt агенту

«Реализуй только A1 из docs/agents/r3-backend.md на ветке feat/r3-analysis-api. Сначала согласуй JSON schemas и fixtures; сохрани Go структуру, реализуй typed mock и API states, проверь идемпотентность и изоляцию, обнови note/OpenAPI. Не внедряй реальные LLM-вызовы этой задачей».

Reviewer: Роман Аксенов; интеграция Python — Денис.

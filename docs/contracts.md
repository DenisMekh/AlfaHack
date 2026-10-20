# Контракты v0.1 — предложение для согласования R1/R3

Структуры в `contracts/*.schema.json`; API endpoints ниже — проект, сервер пока отсутствует. Все даты ISO 8601 UTC. Денежные поля с валютой; неизвестно = null, отсутствующие признаки перечисляются в missing_fields. Для расчётов денежных сумм применять decimal, не float. Company id всегда синтетический строковый идентификатор.

- `GET /api/v1/companies` — доступные сессии компании; пагинация.
- `GET /api/v1/companies/{id}/context` — CompanyContext.
- `POST /api/v1/analysis-runs` body `{company_id, role, period_from, period_to}` → 202 `{run_id,status}`; ключ идемпотентности в заголовке.
- `GET /api/v1/analysis-runs/{run_id}` → статус, этап, карточки Insight, пробелы, признаки mock, показатели бюджета. При необходимости polling.
- `GET /api/v1/sources/{source_id}` → разрешённые метаданные и фрагменты, не произвольный URL fetch.
- `POST /api/v1/feedback` → `{insight_id,rating,reason?}`.

Роли v0.1: `cfo`, `ceo`, `treasury`. Статусы: queued/running/completed/partial/failed. Ошибка `{code,message,request_id}`; stack trace клиенту не отдавать. Доступ проверять для company, run и source. UI не вычисляет бизнес-ранг самостоятельно.

Evidence содержит устойчивый source_id, вид источника company/news/bank, locator (поле CSV или страница/chunk), точную цитату. Claim содержит kind fact/bank_view/ai_inference, текст и evidence_ids. AI inference ссылается на основания, не выдаётся за цитату. Insight содержит хотя бы один исходный новостной источник и один признак компании; отсутствие аналитики банка отражается bank_status=missing. Проверить соответствие company_id, разрешённых источников и реальность цитат должен сервер, JSON Schema этого не гарантирует.

R1/R3 добавляют schema CompanyContext, RunContext и API OpenAPI в первом PR, синхронизируют mock fixtures. Версию контракта повышать при несовместимом изменении.

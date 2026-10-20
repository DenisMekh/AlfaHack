# R5 — Денис: разрешённые LLM, интерпретация и интеграция

## Что изучить

AGENTS.md, requirements, architecture, deployment, security; `ml/src/server/server.py`, handlers/schemas, `ml/pyproject.toml`, `ml/uv.lock`, root Compose и Dockerfiles. Текущий server загружает sentiment/relevance/clusterization из MinIO при старте; новый API-путь не должен требовать эти веса.

## Владение

Новые `ml/src/llm/`, `ml/src/insights/`, `ml/src/verification/`, внутренние FastAPI routes и prompt templates; root Compose, infra/scripts/CI/notices. Python retrieval/ranking — Павел; общий server/pyproject/lock — согласованный PR. Роман Аксенов помогает с инфраструктурой после данных.

## A1 — адаптер и ограничение расходов

Получить endpoint, точные разрешённые model IDs, цены, token limits и reset timezone. Реализовать mock/API интерфейс без автоматической загрузки legacy-моделей. Mock явно маркировать. Не предполагать OpenAI-совместимость. API allowlist, timeout, bounded retry, typed output, cache с model/prompt/data versions. Атомарная резервация верхней оценки стоимости до каждого вызова, reconciliation usage, общий дневной лимит 500 ₽ для всех процессов/ключевых сценариев.

Готовность: разрешённый ID работает; неизвестный отвергается; при лимите/неизвестном тарифе нет тихого перерасхода; конкурентные вызовы не обходят бюджет; ключи только серверные, логи без секретов. Изолированный adapter mock тестируется без сети.

## A2 — план, влияние и проверка

По контракту Go/Python модель возвращает план нужных read-only tools, затем структурированный анализ с подтверждёнными фактами, позицией банка и AI inference. Вызов инструментов/состояния остаются у Go. Проверять evidence IDs, quotes, client features и даты; отсутствие банка/долговых сумм не заполнять догадками. Возвращать verification verdict и конкретный gap для уточнённого поиска. Go ограничивает цикл двумя analysis attempts.

Готовность: две разные компании и новая новость; содержательная причинная связь из нескольких признаков; запрос повторного поиска при нехватке; unsupported claim блокируется. Совместно с Павлом экспертно оценить смысл, не только JSON.

## A3 — сборка, local spike и сдача

Восстановить воспроизводимость: версии Go по go.mod (1.26.1), frontend менеджер с Верой, locked Python; healthchecks и synthetic seed. Реализовать mock/API Compose режимы, закрыть БД/Redis/inference, убрать demo passwords для внешнего стенда. Не менять bytes baseline молча: каждое изменение отдельным PR и запись в migration-report.

Домашний ПК: Windows 11, RTX 3060 Ti 8 GB, i7-12700K, RAM 32 GB. Основной путь — API. Local эксперимент только на точном разрешённом checkpoint с проверенной лицензией/квантованием; максимум выделенный рабочий блок до решения go/no-go по RAM/VRAM/latency. Не выбирать другую меньшую LLM. VPS аренда только отдельной задачей после бюджета; GPU нужен по замерам, обычный VPS может обслужить web/API при внешнем inference.

## Первый prompt агенту

«Реализуй только A1 из docs/agents/r5-infra.md на ветке feat/r5-llm-adapter. Сначала внутренний контракт и mock без legacy weight loading, затем API только при наличии проверенных model ID/цен. Не публикуй ключи. Проверь ошибки, allowlist и конкурентный бюджет; запиши результаты и недостающую информацию».

Reviewer: Павел (LLM/качество), Роман Шваров (контракт/доступ).

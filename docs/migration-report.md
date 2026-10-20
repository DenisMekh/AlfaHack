# Перенос BrandRadar — отчёт

Дата: 20 октября 2026. Источник: https://github.com/DenisMekh/BrandRadar, commit `4254f75ee158098b61b7a5ea061254246c7be84e`, tree `e042dd66a4aba7c80b8b40c89d0a639df7f47cee`. Назначение: DenisMekh/AlfaHack, ветка `chore/brandradar-base`, исходный main `55c66535109059f3452599eaee19d88317981521`.

## Состав и точность

Все 379 файлов исходного Git tree получены и перенесены с проверкой Git blob SHA-1 по байтам; бинарная frontend/public/favicon.ico получена в base64 и проверена после декодирования. Режимы всех исходных файлов — 100644. Полный список в upstream/import-manifest.json. История исходного репозитория не переписана и не объединена с историей AlfaHack; происхождение зафиксировано commit SHA, манифестом и лицензией. Исходный BrandRadar не менялся.

Перемещены только конфликтующие корневые файлы:

| Источник | Назначение |
|---|---|
| README.md | docs/upstream/BrandRadar-README.md |
| LICENSE | LICENSE.brandradar |
| .gitignore | docs/upstream/BrandRadar.gitignore |

Остальные 376 исходных файлов сохранены по прежним путям. README/AGENTS/CONTRIBUTING/контракты и документация AlfaHack сохранены; целевая документация обновлена отдельным этапом под Go/React/Python. Унаследованные .gitignore правила добавлены в root .gitignore. Веса моделей, содержимое MinIO/БД и внешние источники в Git tree не входили и не переносились. Образцы env сохранены; реальный .env не добавлен.

Проведён поиск типовых GitHub/AWS/AI token patterns и private key headers в полученных текстовых файлах: совпадений не найдено. Это ограниченная проверка, не полный аудит секретов. Известные demo passwords остаются в исходном Compose, замена для внешнего стенда — задача R5.

## Проверки и результат

| Проверка | Результат и предел вывода |
|---|---|
| `python scripts/verify_upstream_import.py` | PASS: 379 исходных файлов совпадают по байтам |
| `python -m compileall -q ml/src scripts/verify_upstream_import.py` | PASS: синтаксис Python; импорты, зависимости и модели не запускались |
| `node --check frontend/server.js` | PASS: синтаксис server.js, не сборка frontend |
| `docker compose config --quiet` | PASS: Compose разбирается; образы не собирались, сервисы не запускались |
| `git diff --check HEAD~1..HEAD` (коммит документации) | PASS: новые документы без whitespace ошибок |
| `git diff --check origin/main..HEAD` (весь перенос) | Обнаружены унаследованные trailing whitespace/blank EOF в исходниках BrandRadar. Сохранены ради точности baseline; не являются ошибкой копирования |
| Локальные ссылки новой документации и JSON | PASS: проверены после подготовки; исходные компонентные README не переписывались |
| `npm ci --offline --ignore-scripts --no-audit --no-fund` | Не завершён: ENOTCACHED. Пакеты отсутствуют в локальном кэше |
| `npm ci --ignore-scripts --no-audit --no-fund --fetch-retries=0 --fetch-timeout=10000 --cache /tmp/alfahack-npm-cache` | Заблокирован средой: EPERM при соединении с настроенным proxy. Пакеты не установлены; build/test не запускались |
| Docker daemon через явный локальный socket | Заблокирован средой: operation not permitted. Full-stack runtime не проверен |
| Go build/test | Не выполнены: Go toolchain отсутствует; /usr/bin/go в среде не является компилятором Go. Требование проекта — Go 1.26.1 |

## Обнаруженные работы до адаптированного запуска

1. ML lifespan требует sentiment/relevance/clusterization артефакты из S3; пустой MinIO их не содержит. Новый mock/API путь должен работать без загрузки этих моделей. Их допустимость в кейсе не подтверждена.
2. В npm peer constraints: Vite 8 вне диапазона plugin-react-swc 3.11.0 (4–7); date-fns 4 вне диапазона react-day-picker 8.10.1 (2/3). Это наблюдённые предупреждения, не подтверждение, что Bun-сборка падает. Выбрать и проверить один менеджер/lock с Верой.
3. backend/go.mod требует Go 1.26.1, Dockerfile задаёт 1.26-alpine; swag устанавливается @latest, некоторые Docker images не закреплены. Для воспроизводимости зафиксировать версии и выполнить clean build.
4. analytics worker проверяет ML health до сбора; все пары материалов/брендов идут через relevance/sentiment. Разделить durable ingestion и анализ; большие LLM-вызовы делать после отбора кандидатов.
5. WebCrawler применяет HTML article/h2/meta селекторы и к типу RSS; добавить настоящий RSS и проверить реальные разрешённые источники. Ограничить размер ответа, URL/redirect и network scope.
6. Hash dedup отмечает текст до успешного сохранения/анализа и не сохраняет все альтернативные первоисточники. Перенести границу дедупликации к сохранённому документу и не терять повтор после сбоя.
7. Mentions.tsx подставляет confidence 0.7 и relevant=true при пропусках; для нового UI показывать неизвестное. Кэш и асинхронную выдачу изолировать по компании/роли.
8. Унаследованные public routes включают mock endpoint; в wiring подключён rate limiter, изоляции компаний это не обеспечивает. Добавить доступ company/run/source, ограничить mock и наружные порты, убрать demo credentials перед внешним стендом.
9. Требования кейса — CompanyContext/связи, банковский поиск, объяснимый rank, структурированные claims/evidence, собственный цикл PLAN/tools/context/VERIFY, общий бюджет. Их ещё нужно реализовать; миграция их не добавляет.

Задачи разбиты на A1–A3 в docs/agents/. Полный результат запуска и метрики будут внесены после реализации и проверки; старые accuracy из BrandRadar не переносить в отчёт хакатона.

# Backend — Go/Gin

Соблюдать корневой AGENTS.md и docs/adaptation.md. Здесь сохранён исходный BrandRadar. Новый API и единственная машина состояний — Роман Шваров (docs/agents/r3-backend.md); профиль/импорт/связи/документы — Роман Аксенов (docs/agents/r1-data.md). Общие entity, repo, migrations и app wiring согласовывать между ними. Не переписывать Go на Python и не менять старые миграции. Старые ML/брендовые endpoints не считать реализацией требований кейса. Go version задаётся go.mod, в baseline 1.26.1.

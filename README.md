# KOVXO3-operations

MVP веб-сервис управления агрооперациями (аналог Cropwise-подхода, но проще и удобнее для кастомизации).

## Что есть в MVP

- Авторизация (login/password через cookie-сессию)
- Роли пользователей (manager/agronom/operator) с ограничением действий
- Справочник полей/культур
- Добавление агроопераций
- Карточка поля с историей операций
- Сводка по площадям
- Экспорт операций в Excel: `/export/operations.xlsx?season=2026`
- Импорт операций из Excel (manager only)
- Audit log действий (manager only)
- API отчёта по сезону: `GET /api/report/{season}`

## Быстрый старт (локально)

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Открыть: <http://127.0.0.1:8000/dashboard>

Нажми `Seed demo data`, затем добавляй операции.

Демо-аккаунты после seed:
- `oleg / oleg123` (manager)
- `agronom1 / agro123` (agronom)
- `operator1 / op123` (operator)

## Docker

```bash
docker compose up --build
```

## Дальше (v2)

- роли и права (агроном/руководитель)
- полноценные статусы и фактические площади
- карта полей (PostGIS + MapLibre)
- отчёты Excel/PDF
- интеграция с внешними системами

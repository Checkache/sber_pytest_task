## Проект интеграционных тестов GigaChat API

Этот проект содержит интеграционные тесты для эндпоинта
`POST /api/v1/chat/completions` сервиса GigaChat.

### Структура проекта

- **tests/**: все тесты и общие фикстуры
  - `conftest.py` — общие фикстуры и базовая конфигурация (URL, таймаут, модель, токены)
  - `test_auth_token.py` — проверки различных состояний токена авторизации
  - `test_model_and_messages.py` — проверки полей `model` и `messages`

### Зависимости

Зависимости указаны в `requirements.txt`. Установить их можно так:

```bash
pip install -r requirements.txt
```

### Переменные окружения

- **GIGACHAT_VALID_TOKEN** — валидный токен доступа GigaChat (обязателен для
  интеграционных тестов, которые требуют успешной авторизации).
- **GIGACHAT_API_URL** — (опционально) URL эндпоинта GigaChat, по умолчанию
  `https://gigachat.devices.sberbank.ru/api/v1/chat/completions`.
- **GIGACHAT_REQUEST_TIMEOUT** — (опционально) таймаут HTTP-запросов в секундах,
  по умолчанию `10`.
- **GIGACHAT_MODEL_NAME** — (опционально) имя модели GigaChat, используемой
  по умолчанию в тестах, по умолчанию `GigaChat`.

### Запуск тестов

После установки зависимостей и задания переменных окружения запустите:

```bash
pytest
```


## Проект интеграционных тестов GigaChat API

Этот проект содержит интеграционные тесты для эндпоинта
`POST /api/v1/chat/completions` сервиса GigaChat.

### Структура проекта

- **tests/** — тесты и общая логика
  - `api.py` — хелперы: `post_chat`, `is_success`, `make_payload` (запросы к API и проверки)
  - `conftest.py` — фикстуры: URL, таймаут, модель, токены, `auth_headers`
  - `test_auth_token.py` — авторизация: валидация токена, 401 при невалидном токене
  - `test_model_and_messages.py` — поля `model`, `messages`, обязательные поля, `attachments`; коды 404, 400/422
  - `test_response.py` — структура успешного ответа (JSON), потоковая генерация (Content-Type)

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

### Отчёты в Allure

Для генерации Allure-отчётов используется плагин `allure-pytest` и файл `pytest.ini`.

1. Установите плагин (если ещё не установлен):

```bash
pip install allure-pytest
```

2. Запустите тесты (результаты будут сохранены в папку `allure-results` автоматически,
   путь задан в `pytest.ini`):

```bash
pytest
```

3. Сгенерируйте и откройте HTML-отчёт (требуется установленный Allure Commandline):

```bash
allure serve allure-results
```

Либо можно сгенерировать отчёт в папку и открыть его вручную:

```bash
allure generate allure-results -o allure-report --clean
```


import os

import pytest


# Базовая конфигурация для интеграционных тестов GigaChat API.
# Вынесена в conftest.py, чтобы переиспользовать во всех тестовых модулях.


@pytest.fixture(scope="session")
def gigachat_url() -> str:
    """
    Базовый URL эндпоинта GigaChat для генерации ответа.
    При необходимости можно переопределить через переменную окружения.
    """
    return os.getenv(
        "GIGACHAT_API_URL",
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
    )


@pytest.fixture(scope="session")
def gigachat_timeout() -> int:
    """
    Таймаут HTTP-запросов в секундах.
    """
    return int(os.getenv("GIGACHAT_REQUEST_TIMEOUT", "10"))


@pytest.fixture(scope="session")
def gigachat_model() -> str:
    """
    Имя модели GigaChat, используемой по умолчанию в тестах.
    Можно переопределить через переменную окружения GIGACHAT_MODEL_NAME.
    """
    return os.getenv("GIGACHAT_MODEL_NAME", "GigaChat")


@pytest.fixture(
    params=["valid_token", "empty_token", "invalid_token", "old_token"],
    ids=["valid_token", "empty_token", "invalid_token", "old_token"],
)
def auth_token(request):
    """
    Фикстура для предоставления разных состояний токена и ожидаемого результата.

    Ожидается, что для сценария "valid_token" в переменной окружения
    GIGACHAT_VALID_TOKEN будет лежать реальный валидный токен.
    В репозитории токен не хранится.
    """
    case = request.param

    if case == "valid_token":
        raw_token = os.getenv("GIGACHAT_VALID_TOKEN")
        if not raw_token:
            pytest.skip(
                "Переменная окружения GIGACHAT_VALID_TOKEN не задана, "
                "пропускаем сценарий с валидным токеном."
            )
        token = f"Bearer {raw_token}"
        expected_success = True
    elif case == "empty_token":
        token = ""
        expected_success = False
    elif case == "invalid_token":
        token = "Bearer INVALID_TOKEN"
        expected_success = False
    elif case == "old_token":
        token = "Bearer OLD_TOKEN"
        expected_success = False
    else:
        pytest.fail(f"Неизвестный сценарий токена: {case}")

    return token, expected_success


@pytest.fixture
def valid_auth_header():
    """
    Фикстура для получения заголовка Authorization с валидным токеном.

    Используется в интеграционных тестах полей model и messages,
    чтобы ошибки были связаны именно с телом запроса, а не с авторизацией.
    """
    raw_token = os.getenv("GIGACHAT_VALID_TOKEN")
    if not raw_token:
        pytest.skip(
            "Переменная окружения GIGACHAT_VALID_TOKEN не задана, "
            "пропускаем тесты, завязанные на валидный токен."
        )
    return {"Authorization": f"Bearer {raw_token}"}


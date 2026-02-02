import os
import sys
from pathlib import Path

import pytest

# Корень проекта в sys.path, чтобы при запуске `pytest` из корня работал импорт tests.api
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


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


AUTH_TOKEN_CASES = {
    "valid_token": (None, True),   # значение подставится из env
    "empty_token": ("", False),
    "invalid_token": ("Bearer INVALID_TOKEN", False),
    "old_token": ("Bearer OLD_TOKEN", False),
}


@pytest.fixture(
    params=list(AUTH_TOKEN_CASES),
    ids=list(AUTH_TOKEN_CASES),
)
def auth_token(request):
    """
    Разные состояния токена и ожидаемый результат.
    Для "valid_token" требуется переменная окружения GIGACHAT_VALID_TOKEN.
    """
    case = request.param
    token_value, expected_success = AUTH_TOKEN_CASES[case]
    if case == "valid_token":
        raw = os.getenv("GIGACHAT_VALID_TOKEN")
        if not raw:
            pytest.skip("GIGACHAT_VALID_TOKEN не задана, пропускаем сценарий valid_token.")
        token_value = f"Bearer {raw}"
    return token_value, expected_success


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


@pytest.fixture
def auth_headers(valid_auth_header):
    """Заголовки для авторизованного JSON-запроса (Authorization + Content-Type)."""
    return {**valid_auth_header, "Content-Type": "application/json"}


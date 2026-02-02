import pytest
import requests


def test_auth_token_validation(auth_token, gigachat_url, gigachat_timeout, gigachat_model):
    """
    Интеграционный тест: проверка поведения сервера при разных состояниях токена.

    Фикстура auth_token возвращает пару (token, expected_success).
    Остальные фикстуры предоставляют конфигурацию GigaChat API.
    """
    token, expected_success = auth_token
    headers = {"Authorization": token}

    # Минимально валидное тело запроса для генерации ответа
    payload = {
        "model": gigachat_model,
        "messages": [
            {"role": "user", "content": "Тестовое сообщение для проверки токена."}
        ],
    }

    # Отправляем POST-запрос к сервису с таймаутом
    try:
        response = requests.post(
            gigachat_url,
            headers=headers,
            json=payload,
            timeout=gigachat_timeout,
        )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Запрос к Gigachat API не удался: {exc}")

    if expected_success:
        # Если ожидался успех, проверяем статус-код
        assert 200 <= response.status_code <= 299, (
            f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"
        )
    else:
        # Если ожидалась ошибка, проверяем, что статус-код не в пределах 2xx
        assert not (200 <= response.status_code <= 299), (
            f"Странно, ожидали ошибку, получили успешный ответ: {response.status_code}"
        )


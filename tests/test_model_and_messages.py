import pytest
import requests


@pytest.mark.parametrize(
    "model, expected_success",
    [
        pytest.param(
            None,
            False,
            id="missing_model",
        ),
        pytest.param(
            "",
            False,
            id="empty_model",
        ),
        pytest.param(
            "NonExistingModel123",
            False,
            id="invalid_model",
        ),
    ],
)
def test_model_field_validation(
    valid_auth_header,
    gigachat_url,
    gigachat_timeout,
    gigachat_model,
    model,
    expected_success,
):
    """
    Интеграционный тест для проверки поведения API при разных значениях поля model.

    Сценарий с валидной моделью проверяется отдельно, чтобы явно видеть,
    что базовая конфигурация работает корректно.
    """
    effective_model = gigachat_model if model is None else model

    payload = {
        "model": effective_model,
        "messages": [
            {"role": "user", "content": "Тестовая проверка поля model."}
        ],
    }

    headers = {
        **valid_auth_header,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            gigachat_url,
            headers=headers,
            json=payload,
            timeout=gigachat_timeout,
        )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Запрос к Gigachat API не удался: {exc}")

    # Для всех параметризованных сценариев ожидаем ошибку (не 2xx)
    assert not (200 <= response.status_code <= 299), (
        f"Ожидали ошибку для model='{effective_model}', "
        f"получили успешный статус-код: {response.status_code}"
    )


def test_model_field_with_valid_value(
    valid_auth_header,
    gigachat_url,
    gigachat_timeout,
    gigachat_model,
):
    """
    Отдельный позитивный тест: проверяем, что при корректной модели
    и валидном токене API возвращает успешный статус-код.
    """
    payload = {
        "model": gigachat_model,
        "messages": [
            {"role": "user", "content": "Позитивный тест поля model."}
        ],
    }

    headers = {
        **valid_auth_header,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            gigachat_url,
            headers=headers,
            json=payload,
            timeout=gigachat_timeout,
        )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Запрос к Gigachat API не удался: {exc}")

    assert 200 <= response.status_code <= 299, (
        f"Ожидали успешный ответ для модель='{gigachat_model}', "
        f"получили статус-код: {response.status_code}, тело: {response.text}"
    )


@pytest.mark.parametrize(
    "messages, expected_success",
    [
        pytest.param(
            [{"role": "user", "content": "Тестовая проверка поля messages."}],
            True,
            id="valid_messages",
        ),
        pytest.param(
            [],
            False,
            id="empty_list",
        ),
        pytest.param(
            [{"role": "user"}],  # нет content
            False,
            id="missing_content",
        ),
        pytest.param(
            "не список сообщений",
            False,
            id="wrong_type",
        ),
    ],
)
def test_messages_field_validation(
    valid_auth_header,
    gigachat_url,
    gigachat_timeout,
    gigachat_model,
    messages,
    expected_success,
):
    """
    Интеграционный тест для проверки поведения API при разных значениях поля messages.
    """
    payload = {
        "model": gigachat_model,
        "messages": messages,
    }

    headers = {
        **valid_auth_header,
        "Content-Type": "application/json",
    }

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
        assert 200 <= response.status_code <= 299, (
            "Ожидали успешный ответ для корректного messages, "
            f"получили статус-код: {response.status_code}, тело: {response.text}"
        )
    else:
        assert not (200 <= response.status_code <= 299), (
            "Ожидали ошибку для некорректного messages, "
            f"получили успешный статус-код: {response.status_code}"
        )


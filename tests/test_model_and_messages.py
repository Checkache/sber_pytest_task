import pytest

from tests.api import is_success, make_payload, post_chat


@pytest.mark.parametrize(
    "model, expected_success",
    [
        pytest.param(None, False, id="missing_model"),
        pytest.param("", False, id="empty_model"),
        pytest.param("NonExistingModel123", False, id="invalid_model"),
    ],
)
def test_model_field_validation(
    auth_headers, gigachat_url, gigachat_timeout, gigachat_model, model, expected_success
):
    """Проверка поведения API при разных значениях поля model."""
    effective_model = gigachat_model if model is None else model
    payload = make_payload(
        effective_model,
        [{"role": "user", "content": "Тестовая проверка поля model."}],
    )
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert not is_success(response), (
        f"Ожидали ошибку для model='{effective_model}', получили: {response.status_code}"
    )


def test_invalid_model_returns_404(auth_headers, gigachat_url, gigachat_timeout):
    """При несуществующей модели API возвращает 404."""
    payload = make_payload("NonExistingModel123", [{"role": "user", "content": "Проверка 404."}])
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert response.status_code == 404, f"Ожидали 404, получили: {response.status_code}, тело: {response.text}"


@pytest.mark.parametrize(
    "payload_builder, description",
    [
        pytest.param(lambda m: {"model": m}, "missing_messages", id="missing_messages"),
        pytest.param(lambda _: {"messages": [{"role": "user", "content": "Текст"}]}, "missing_model", id="missing_model"),
    ],
)
def test_missing_required_fields_returns_4xx(
    auth_headers, gigachat_url, gigachat_timeout, gigachat_model, payload_builder, description
):
    """При отсутствии обязательных полей model или messages API возвращает 400 или 422."""
    payload = payload_builder(gigachat_model)
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert response.status_code in (400, 422), (
        f"Ожидали 400 или 422 ({description}), получили: {response.status_code}, тело: {response.text}"
    )


def test_model_field_with_valid_value(auth_headers, gigachat_url, gigachat_timeout, gigachat_model):
    """При корректной модели и валидном токене API возвращает успешный статус."""
    payload = make_payload(gigachat_model, [{"role": "user", "content": "Позитивный тест поля model."}])
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert is_success(response), f"Ожидали 2xx для модель='{gigachat_model}', получили: {response.status_code}, тело: {response.text}"


@pytest.mark.parametrize(
    "messages, expected_success",
    [
        pytest.param([{"role": "user", "content": "Тестовая проверка поля messages."}], True, id="valid_messages"),
        pytest.param([], False, id="empty_list"),
        pytest.param([{"role": "user"}], False, id="missing_content"),
        pytest.param("не список сообщений", False, id="wrong_type"),
    ],
)
def test_messages_field_validation(
    auth_headers, gigachat_url, gigachat_timeout, gigachat_model, messages, expected_success
):
    """Проверка поведения API при разных значениях поля messages."""
    payload = make_payload(gigachat_model, messages)
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    if expected_success:
        assert is_success(response), f"Ожидали 2xx, получили: {response.status_code}, тело: {response.text}"
    else:
        assert not is_success(response), f"Ожидали ошибку для messages, получили: {response.status_code}"


def test_attachments_empty_array_accepted(auth_headers, gigachat_url, gigachat_timeout, gigachat_model):
    """Запрос с полем attachments: [] принимается (200)."""
    payload = make_payload(
        gigachat_model,
        [{"role": "user", "content": "Проверка attachments."}],
        attachments=[],
    )
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert is_success(response), f"Ожидали успех при attachments: [], получили: {response.status_code}, тело: {response.text}"


@pytest.mark.parametrize(
    "attachments_value",
    ["not_an_array", {"key": "value"}, 123],
    ids=["string", "object", "number"],
)
def test_attachments_invalid_type_returns_4xx(
    auth_headers, gigachat_url, gigachat_timeout, gigachat_model, attachments_value
):
    """При неверном типе attachments (не массив) API возвращает 400 или 422."""
    payload = make_payload(
        gigachat_model,
        [{"role": "user", "content": "Проверка."}],
        attachments=attachments_value,
    )
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)
    assert response.status_code in (400, 422), (
        f"Ожидали 400 или 422 при неверном типе attachments, получили: {response.status_code}, тело: {response.text}"
    )


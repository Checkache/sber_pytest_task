import pytest

from tests.api import is_success, make_payload, post_chat


def test_auth_token_validation(auth_token, gigachat_url, gigachat_timeout, gigachat_model):
    """
    Интеграционный тест: проверка поведения сервера при разных состояниях токена.
    """
    token, expected_success = auth_token
    headers = {"Authorization": token}
    payload = make_payload(
        gigachat_model,
        [{"role": "user", "content": "Тестовое сообщение для проверки токена."}],
    )
    response = post_chat(gigachat_url, gigachat_timeout, headers=headers, json_payload=payload)

    if expected_success:
        assert is_success(response), f"Неверный статус: {response.status_code}, тело: {response.text}"
    else:
        assert not is_success(response), f"Ожидали ошибку, получили: {response.status_code}"


@pytest.mark.parametrize(
    "token_value",
    ["", "Bearer INVALID_TOKEN", "Bearer OLD_TOKEN"],
    ids=["empty_token", "invalid_token", "old_token"],
)
def test_auth_returns_401_on_invalid_token(
    gigachat_url, gigachat_timeout, gigachat_model, token_value
):
    """При невалидном/пустом токене API возвращает 401."""
    headers = {"Authorization": token_value}
    payload = make_payload(gigachat_model, [{"role": "user", "content": "Проверка 401."}])
    response = post_chat(gigachat_url, gigachat_timeout, headers=headers, json_payload=payload)
    assert response.status_code == 401, f"Ожидали 401, получили: {response.status_code}, тело: {response.text}"


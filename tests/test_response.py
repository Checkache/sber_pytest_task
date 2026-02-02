"""Тесты структуры успешного ответа и потоковой генерации."""
import json

import pytest

from tests.api import make_payload, post_chat


def test_success_response_structure(auth_headers, gigachat_url, gigachat_timeout, gigachat_model):
    """При успешном ответе (200) тело — валидный JSON с ожидаемой структурой."""
    payload = make_payload(gigachat_model, [{"role": "user", "content": "Ответь одним словом: ок."}])
    response = post_chat(gigachat_url, gigachat_timeout, headers=auth_headers, json_payload=payload)

    assert response.status_code == 200, f"Ожидали 200, получили: {response.status_code}, тело: {response.text}"
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        pytest.fail(f"Ответ не является валидным JSON: {e}")

    assert isinstance(data, dict), "Тело ответа должно быть объектом"
    has_choices = "choices" in data and isinstance(data.get("choices"), list) and len(data["choices"]) > 0
    if has_choices:
        first = data["choices"][0]
        assert isinstance(first, dict), "choices[0] должен быть объектом"
        if "message" in first:
            assert "content" in first["message"] or "role" in first["message"], (
                "choices[0].message должен содержать content или role"
            )
    else:
        assert "choices" in data or "id" in data or "model" in data, (
            f"Ожидали в ответе поле choices, id или model; ключи: {list(data.keys())}"
        )


def test_streaming_response_headers(auth_headers, gigachat_url, gigachat_timeout, gigachat_model):
    """При запросе с stream=true ответ 200 и Content-Type: text/event-stream."""
    payload = make_payload(
        gigachat_model,
        [{"role": "user", "content": "Скажи привет."}],
        stream=True,
    )
    response = post_chat(
        gigachat_url, gigachat_timeout,
        headers=auth_headers, json_payload=payload, stream=True,
    )

    assert response.status_code == 200, (
        f"Ожидали 200 при потоковом запросе, получили: {response.status_code}"
    )
    content_type = response.headers.get("Content-Type", "")
    assert "text/event-stream" in content_type.lower(), (
        f"Ожидали Content-Type: text/event-stream, получили: {content_type}"
    )

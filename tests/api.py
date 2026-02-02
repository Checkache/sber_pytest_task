"""
Общие хелперы для запросов к GigaChat API и проверок ответов.
"""
import pytest
import requests


def post_chat(url, timeout, *, headers=None, json_payload=None, stream=False):
    """
    Выполняет POST к эндпоинту chat/completions.
    При сетевой ошибке вызывает pytest.skip().
    """
    try:
        return requests.post(
            url,
            headers=headers,
            json=json_payload,
            timeout=timeout,
            stream=stream,
        )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Запрос к Gigachat API не удался: {exc}")


def is_success(response):
    """Проверка, что статус в диапазоне 2xx."""
    return 200 <= response.status_code <= 299


def make_payload(model, messages, **extra):
    """Собирает тело запроса: model, messages и произвольные доп. поля."""
    payload = {"model": model, "messages": messages}
    payload.update(extra)
    return payload

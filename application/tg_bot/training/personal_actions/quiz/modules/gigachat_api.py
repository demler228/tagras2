import json
import requests
import uuid
from modules.utils import remove_empty_lines


client_id = "ce7d7680-4bf7-4ff3-b172-3be3794aa5b8"
secret = "338c3cfd-1038-4d2b-9e27-5af3a3d7f728"
auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="


def get_token(scope="GIGACHAT_API_PERS"):
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth}",
    }
    payload = {"scope": scope}
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.json().get("access_token", None)
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return None


def get_quiz_questions(auth_token, text):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Сгенерируй 10 вопросов по тексту. Каждый вопрос должен быть в следующем формате:
- Вопрос
- 4 варианта ответа (пронумерованные от 1 до 4)
- Правильный ответ (указанный в формате "Правильный ответ: X)")

Верни ответ в формате JSON, как в примере ниже:

[
    {{
        "question": "Почему Бу не смог провести успешные переговоры с американцами?",
        "answers": [
            "Он не знал английский язык.",
            "Он не подготовился к переговорам.",
            "Он не смог договориться с американцами.",
            "Он не был уверен в себе."
        ],
        "correct_answer": "Он не подготовился к переговорам."
    }},

Вот текст: {text}

Убедись, что ответ строго соответствует этому формату JSON. Не добавляй лишних символов или комментариев.""",
                }
            ],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 2048,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.json()
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return None
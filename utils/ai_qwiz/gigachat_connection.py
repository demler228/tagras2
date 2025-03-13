client_id = "ce7d7680-4bf7-4ff3-b172-3be3794aa5b8"
secret = "338c3cfd-1038-4d2b-9e27-5af3a3d7f728"
auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="

import requests
import uuid

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    payload = {
        'scope': scope
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

response = get_token(auth)
if response != 1:
  print(response.text)
  giga_token = response.json()['access_token']

import requests

url = "https://gigachat.devices.sberbank.ru/api/v1/models"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {giga_token}'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)

import requests
import json

def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1

answer = get_chat_completion(giga_token, 'Как на Пайтоне сделать GET запрос?')

answer.json()

print(answer.json()['choices'][0]['message']['content'])

from IPython.display import display, Markdown
display(Markdown(answer.json()['choices'][0]['message']['content']))


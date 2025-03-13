import requests
from bs4 import BeautifulSoup

response = requests.get("https://habr.com/ru/articles/709116/")
response.raise_for_status()  # Проверяем, что запрос успешен
soup = BeautifulSoup(response.text, "html.parser")
        
# Удаляем ненужные элементы, такие как скрипты и стили
for script in soup(["script", "style"]):
    script.decompose()
        
# Извлекаем текст из тегов <p>, <h1>, <h2>, и т.д.
text = soup.get_text(separator="\n")
print(text)
import requests
from bs4 import BeautifulSoup
from modules.utils import remove_empty_lines


def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")
        return remove_empty_lines(text)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None
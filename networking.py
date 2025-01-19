import requests
from bs4 import BeautifulSoup

class NetworkUtil:
    def __init__(self, cookies):
        self.cookies = cookies
        self.session = requests.Session()

    def fetch_index_page(self, url):
        """
        Функция для загрузки index.php с использованием cookie.
        """
        try:
            response = self.session.get(url, cookies=self.cookies)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Ошибка: статус ответа {response.status_code}")
        except Exception as e:
            print(f"Ошибка при загрузке index.php: {e}")
        return None

    def fetch_user_token(self, base_url):
        """
        Функция для получения user_token.
        """
        try:
            response = self.session.get(base_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                token_input = soup.find('input', {'name': 'user_token'})
                return token_input['value'] if token_input else None
        except Exception as e:
            print(f"Ошибка получения user_token: {e}")
        return None

    def attempt_login(self, base_url, username, password, user_token):
        """
        Функция для отправки запроса на сервер DVWA.
        """
        try:
            params = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            if user_token:
                params['user_token'] = user_token

            response = self.session.get(base_url, params=params, cookies=self.cookies)
            return 'Welcome to the password protected area' in response.text
        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return False

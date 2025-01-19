import hashlib
from itertools import product
import multiprocessing
import time

def get_password_from_index(index, letters):
    length = len(letters)
    password = ""
    for _ in range(5):  # Fixed password length of 5
        password = letters[index % length] + password
        index //= length
    return password

def brute_force(md5_hashes, sha256_hashes, letters, start_index=0, step=1):
    total_combinations = len(letters) ** 5
    for i in range(start_index, total_combinations, step):
        password = get_password_from_index(i, letters)
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()

        if md5_hash in md5_hashes:
            print(f"Найден пароль для MD5: {password} -> {md5_hash}")
        if sha256_hash in sha256_hashes:
            print(f"Найден пароль для SHA-256: {password} -> {sha256_hash}")

def single_threaded_mode(md5_hashes, sha256_hashes, letters):
    start_time = time.time()
    brute_force(md5_hashes, sha256_hashes, letters)
    end_time = time.time()
    print(f"Однопоточный режим завершен за: {end_time - start_time:.2f} секунд")

def multi_threaded_mode(md5_hashes, sha256_hashes, letters, thread_count):
    start_time = time.time()
    processes = []
    for i in range(thread_count):
        process = multiprocessing.Process(
            target=brute_force,
            args=(md5_hashes, sha256_hashes, letters, i, thread_count)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Многопоточный режим завершен за: {end_time - start_time:.2f} секунд")

def read_hashes_from_file(file_path):
    md5_hashes = []
    sha256_hashes = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if len(line) == 32:
                    md5_hashes.append(line)
                elif len(line) == 64:
                    sha256_hashes.append(line)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return md5_hashes, sha256_hashes

def read_hashes_from_console():
    md5_hashes = []
    sha256_hashes = []
    print("Введите хэш-значения (MD5 или SHA-256), по одному на строку. Введите 'end' для завершения ввода:")
    while True:
        user_input = input().strip()
        if user_input.lower() == "end":
            break
        elif len(user_input) == 32:
            md5_hashes.append(user_input)
        elif len(user_input) == 64:
            sha256_hashes.append(user_input)
        else:
            print("Неверное хэш-значение. Введите MD5 (32 символа) или SHA-256 (64 символа).")
    return md5_hashes, sha256_hashes

if __name__ == "__main__":
    letters = "abcdefghijklmnopqrstuvwxyz"

    print("Выберите источник хэш-значений: 1 - Файл, 2 - Ввод с консоли, 3 - использовать введённые в программу")
    choice = input().strip()

    md5_hashes = []
    sha256_hashes = []

    if choice == "1":
        file_path = input("Введите путь к файлу с хэш-значениями: ").strip()
        md5_hashes, sha256_hashes = read_hashes_from_file(file_path)
    elif choice == "2":
        md5_hashes, sha256_hashes = read_hashes_from_console()
    elif choice == "3":
        md5_hashes = ["7a68f09bd992671bb3b19a5e70b7827e"]
        sha256_hashes = [
            "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
            "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
            "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f"
        ]
    else:
        print("Неверный выбор источника хэш-значений.")
        exit()

    print("Выберите режим: 1 - Однопоточный, 2 - Многопоточный")
    mode = input().strip()

    if mode == "1":
        single_threaded_mode(md5_hashes, sha256_hashes, letters)
    elif mode == "2":
        thread_count = int(input("Введите количество потоков: ").strip())
        multi_threaded_mode(md5_hashes, sha256_hashes, letters, thread_count)
    else:
        print("Неверный выбор. Завершение программы.")

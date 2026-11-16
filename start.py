import subprocess
import urllib.request
import json
import time
import os
import sys

def get_game_name(app_id):
    url = f"https://steampowered.com{app_id}&cc=us"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        data = json.loads(req.read().decode('utf-8'))
        if data[app_id]['success']:
            return data[app_id]['data']['name']
    except Exception:
        pass
    return "Неизвестная игра"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(base_dir, "steam_api64.dll")
    games_path = os.path.join(base_dir, "games.txt")
    worker_path = os.path.join(base_dir, "worker.py")

    if not os.path.exists(dll_path):
        print("ОШИБКА: Положите файл steam_api64.dll в папку со скриптом!")
        return

    if not os.path.exists(games_path):
        print("ОШИБКА: Файл games.txt не найден!")
        return

    with open(games_path, "r", encoding="utf-8") as f:
        app_ids = [line.strip() for line in f if line.strip().isdigit()]

    if not app_ids:
        print("Список games.txt пуст! Добавьте туда ID игр.")
        return

    print(f"Найдено игр: {len(app_ids)}. Запускаем...\n")
    processes = []

    for app_id in app_ids:
        name = get_game_name(app_id)
        p = subprocess.Popen([sys.executable, worker_path, app_id])
        processes.append(p)
        print(f"[+] Запущено: {name} (ID: {app_id})")
        time.sleep(1)

    print("\nВсе игры запущены! Чтобы остановить, нажмите в этом окне Ctrl + C")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nОстанавливаем накрутку...")
        for p in processes:
            p.terminate()
        print("Готово!")

if __name__ == "__main__":
    main()

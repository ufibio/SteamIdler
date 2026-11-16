import ctypes
import sys
import time
import os

if len(sys.argv) < 2:
    sys.exit()

app_id = sys.argv[1]
os.environ["SteamAppId"] = app_id
os.environ["SteamGameId"] = app_id

dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "steam_api64.dll")

try:
    steam_api = ctypes.CDLL(dll_path)
    success = False

    # Пробуем старый метод (для старых DLL)
    if hasattr(steam_api, "SteamAPI_Init"):
        steam_api.SteamAPI_Init.restype = ctypes.c_bool
        success = steam_api.SteamAPI_Init()
    # Пробуем новый метод (для свежих DLL из Steamworks SDK 1.59+)
    elif hasattr(steam_api, "SteamAPI_InitFlat"):
        steam_api.SteamAPI_InitFlat.argtypes = [ctypes.c_char_p]
        steam_api.SteamAPI_InitFlat.restype = ctypes.c_int
        err_msg = ctypes.create_string_buffer(1024)
        # В SteamAPI_InitFlat код 0 (k_ESteamAPIInitResult_OK) означает успех
        res = steam_api.SteamAPI_InitFlat(err_msg)
        if res == 0:
            success = True
        else:
            print(f"Ошибка SteamAPI_InitFlat для {app_id}: {err_msg.value.decode('utf-8', errors='ignore')}")

    if success:
        print(f"УСПЕХ: Игра {app_id} подключена к Steam!")
        while True:
            time.sleep(10)
    else:
        print(f"Не удалось подключить игру {app_id} (проверьте, есть ли она на аккаунте и запущен ли Steam).")

except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА в worker.py: {e}")

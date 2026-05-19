import time
import requests

URL_P1 = "https://school-game-test-default-rtdb.firebaseio.com/player1_move.json"
URL_P2 = "https://school-game-test-default-rtdb.firebaseio.com/player2_move.json"

print("--- ИГРОК 1 ---")
print("Очищаем старые ходы...")
requests.put(URL_P1, json="пусто")
requests.put(URL_P2, json="пусто")

try:
    for i in range(1, 4):
        my_move = f"Ход Игрока 1 номер {i}"
        
        # Отправляем свой ход
        requests.put(URL_P1, json=my_move)
        print(f"\nВы отправили в облако: {my_move}")
        print("Ждем, пока Игрок 2 ответит...")
        
        # Ждем ход от Игрока 2
        while True:
            try:
                p2_move = requests.get(URL_P2).json()
                
                # Если вернулся словарь с ошибкой или "пусто", игнорируем и ждем дальше
                if isinstance(p2_move, dict) and "error" in p2_move:
                    time.sleep(1)
                    continue
                    
                if p2_move and p2_move != "пусто":
                    print(f"Игрок 2 прислал ответ: {p2_move}")
                    # Сбрасываем его ход для следующего раунда
                    requests.put(URL_P2, json="пусто")
                    break
            except Exception:
                pass # Если лагает интернет, просто пробуем еще раз
                
            time.sleep(1.5)
            
    print("\nИгра успешно завершена!")

except Exception as e:
    print(f"Ошибка: {e}")
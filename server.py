import asyncio
import websockets
import os        # <-- ОБЯЗАТЕЛЬНО ДОБАВЬ ЭТОТ ИМПОРТ
import requests  # Твой импорт, который мы чинили в прошлый раз

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

async def main():
    # Получаем порт от Render. Если его нет, используем 10000 по умолчанию
    port = int(os.environ.get("PORT", 10000))
    
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server started on port {port}")
        await asyncio.Future()

asyncio.run(main())

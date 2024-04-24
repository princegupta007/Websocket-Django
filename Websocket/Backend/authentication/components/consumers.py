# # components/consumers.py
# from channels.generic.websocket import WebsocketConsumer

# class MyConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         print("Connected to WebSocket")

#     def disconnect(self, close_code):
#         print("Disconnected from WebSocket")

#     def receive(self, text_data):
#         print("Received message from WebSocket:", text_data)
#         # Handle received message here










import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connected to WebSocket")
        self.send_random_number_task = asyncio.create_task(self.send_random_number())

    async def disconnect(self, close_code):
        print("Disconnected from WebSocket")
        if hasattr(self, 'send_random_number_task'):
            self.send_random_number_task.cancel()

    async def send_random_number(self):
        try:
            while True:
                number = random.randint(100, 999)
                await self.send(text_data=str(number))
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

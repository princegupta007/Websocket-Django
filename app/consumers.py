# components/consumers.py
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connected to websocket.")

    def disconnect(self, close_code):
        print("Disconnected from websocket.")

    def receive(self, text_data):
        print("Received data from websocket:", text_data)

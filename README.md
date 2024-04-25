# Basic WebSocket Connection in Django

This guide demonstrates how to create a basic WebSocket connection in Django using a `WebsocketConsumer`.

## Getting Started

### Prerequisites

- Python
- Django

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```bash
   cd <project_directory>
   ```

### Usage

1. Create a Django app (if you haven't already):

   ```bash
   python manage.py startapp <app_name>
   ```

2. Create a `consumers.py` file inside your app directory.

3. Add the following code to `consumers.py`:

   ```python
   from channels.generic.websocket import WebsocketConsumer

   class MyConsumer(WebsocketConsumer):
       def connect(self):
           self.accept()
           print("Connected to websocket.")

       def disconnect(self, close_code):
           print("Disconnected from websocket.")

       def receive(self, text_data):
           print("Received data from websocket:", text_data)
   ```

4. Configure routing in `routing.py` (if not already configured):

   ```python
   from channels.routing import ProtocolTypeRouter, URLRouter
   from django.urls import path
   from myapp.consumers import MyConsumer

   application = ProtocolTypeRouter({
       "websocket": URLRouter([
           path("ws/myapp/", MyConsumer.as_asgi()),
       ])
   })
   ```

   Replace `myapp` with the name of your Django app.

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open your browser's console and initiate a WebSocket connection to `ws://localhost:8000/ws/myapp/`.

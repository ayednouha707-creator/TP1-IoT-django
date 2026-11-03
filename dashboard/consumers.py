import json
from channels.generic.websocket import AsyncWebsocketConsumer

GROUP_NAME = 'sensor_temperature'


class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('connect....')
        self.room_group_name = GROUP_NAME
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "connected..."}))

    async def receive(self, text_data=None, bytes_data=None):
        # le navigateur n'envoie rien dans ce TP
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from group
    async def sensor_temperature(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message['payload']}))
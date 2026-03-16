from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'dashboard'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def device_update(self, event):
        # Triggered when a new device update is pushed from views
        device_data = event['message']
        await self.send(text_data=json.dumps({
            "type": "device_update",
            "data": device_data
        }))
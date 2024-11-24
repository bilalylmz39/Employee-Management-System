from channels.generic.websocket import JsonWebsocketConsumer


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def send_notification(self, event):
        self.send_json(event['message'])

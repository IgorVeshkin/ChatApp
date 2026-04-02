from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

# from channels.layers import get_channel_layer

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):

        # Getting user: self.scope["user"] --> AnonymousUser

        async_to_sync(self.channel_layer.group_add)(
           "Test_Chat_name", self.channel_name # "Test_channel_name" 
        )

        self.accept()

        # print("self.scope:", self.scope)

        print("Connected successfully....")


    def message_handler(self, event):
        print("Сообщение отправлено")
        message = event['message']
        self.send(text_data=message)

    def receive(self, text_data):
        print("The message has been received: ", text_data)

        event = {
            "type": "message_handler",
            "message": text_data,

        }

        async_to_sync(self.channel_layer.group_send)(
           "Test_Chat_name", event
        )
        


    # def message_handler(self, event):
    #     print("Сообщение отправлено")
    #     self.send(text_data=event["message"])


    def disconnect(self, close_code):
        print("One of users has been disconnected....")

        async_to_sync(self.channel_layer.group_discard)(
           "Test_Chat_name", self.channel_name # "Test_channel_name" 
        )


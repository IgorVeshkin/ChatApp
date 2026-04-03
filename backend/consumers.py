from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import urllib.parse


class ChatroomConsumer(WebsocketConsumer):

    def get_url_query_params(self):
        # Получение параметров из url-строки (парсинг)
        query_string_bytes = self.scope['query_string']

        query_string = query_string_bytes.decode('utf-8')
        query_params = urllib.parse.parse_qs(query_string)

        query_params_edited = {}

        # Убираю список, если объект всего один
        for key, value_list in query_params.items():
            if len(value_list) == 1:
                query_params_edited[key] = value_list[0]
            else:
                query_params_edited[key] = value_list

        return query_params_edited


    def connect(self):

        # Getting user: self.scope["user"] --> AnonymousUser

        self.query_params = self.get_url_query_params()

        async_to_sync(self.channel_layer.group_add)(
           self.query_params["chatroom_uuid"], self.channel_name # "Test_Chat_name" # "Test_channel_name" 
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
           self.query_params["chatroom_uuid"], event # "Test_Chat_name"
        )


    def disconnect(self, close_code):
        print("One of users has been disconnected....")

        async_to_sync(self.channel_layer.group_discard)(
           self.query_params["chatroom_uuid"], self.channel_name # "Test_Chat_name" # "Test_channel_name" 
        )


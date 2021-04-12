import json
import re

import pandas as pd

from channels.generic.websocket import AsyncWebsocketConsumer


def csv_to_dict(csv_url):
    print(csv_url)
    df = pd.read_csv(csv_url)
    return df.to_dict(orient='records')


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sets room name
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

    async def connect(self):
        """ Client gets connected """
        print('consumers.connect')
        # Joins room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Tells succeeded connection
        await self.accept()

    async def disconnect(self, close_code):
        """ Client gets disconnected """
        print('consumers.disconnect')
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """ User sends message, we receive it """
        print('consumers.receive', text_data)
        text_data_json = json.loads(text_data)
        name = text_data_json["name"]
        text = text_data_json["text"]
        createdAt = text_data_json["createdAt"]
        print('  * calling commands', text_data)
        # Send message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "name": name,
                "text": text,
                "createdAt": createdAt
            },
        )
        await self.commands(text, name, createdAt)

    async def commands(self, text, name, createdAt):
        """ Identifies if a command was sent """
        print('** consumers.commands', text)
        supported_commands = ['stock']
        command_pattern = re.match(".*/([A-z]*)=.*", text)
        valid_command = re.match("^/([a-z]+)=(([A-z]|\.)+)$", text)
        print('valid_command', valid_command)
        if valid_command:
            command, value = valid_command.groups()[:2]
            print(command, value)
            if command in supported_commands:
                url = f'https://stooq.com/q/l/?s={value}&f=sd2t2ohlcv&h&e=csv'
                parsed_data = csv_to_dict(url)
                print(parsed_data)
                data = parsed_data[0]
                data = f"{data['Symbol']} is {data['Close']}"
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "name": 'BOT',
                        "text": data,
                        "createdAt": createdAt
                    },
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "name": 'BOT',
                        "text": f"Unsupported command: {command}",
                        "createdAt": createdAt
                    },
                )

        elif command_pattern:
            command = command_pattern.groups()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "name": 'BOT',
                    "text": f"Wrong Formatted '{command}' command.",
                    "createdAt": createdAt
                },
            )
        else:
            pass

    async def chat_message(self, event):
        """ Receive room data """
        print('consumers.chat_message', event)
        name = event["name"]
        text = event["text"]
        createdAt = event["createdAt"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "name": name,
                    "text": text,
                    "createdAt": createdAt
                }
            )
        )

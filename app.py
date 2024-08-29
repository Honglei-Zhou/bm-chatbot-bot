import logging
import json
from chatbot.utils.detect_intent import detect_intent_texts
from chatbot.utils.update_db import update_message
from server.server import app
import socketio


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app.config['SECRET_KEY'] = 'secret!'


sio = socketio.Client()


@sio.on('connect')
def connect():
    print('connection established')
    sio.emit('bot_join', json.dumps({'username': 'bot'}))


@sio.on('CHAT_MESSAGE')
def handle_message(data):
    print(data)

    data = json.loads(data)
    if data['tag'] != 'bot' and data['tag'] != 'admin':
        to_room_id = data['groupId']
        message = data['message']
        new_message = detect_intent_texts(to_room_id, message)

        sio.emit('bot_message', json.dumps({
            'groupId': to_room_id,
            'message': new_message,
            'tag': 'bot',
            'unread': 1
        }))


@sio.on('MUTE_STATE')
def handle_user_leave(data):
    # [{'groupId': room, 'online': False, 'muted': False}]
    data = json.loads(data)
    if len(data) > 0:
        message = data[0]
        if message['online'] is False:
            to_room_id = data['groupId']
            message = {'data': {'text': 'CUSTOMERHASLEFT'}}
            detect_intent_texts(to_room_id, message)


@sio.on('disconnect')
def disconnect():
    print('disconnected from server')


sio.connect('http://127.0.0.1:5001')
sio.wait()



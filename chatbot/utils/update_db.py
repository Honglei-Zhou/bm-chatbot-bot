import os
from ..models import Group, Message
from datetime import datetime
import json

dirpath = os.path.dirname(os.path.realpath(__file__))


def update_group(sid, alive):

    group = Group.query.filter(Group.session_id == sid).first()

    if group is None:

        new_group = Group()
        new_group.session_id = sid

        new_group.alive = alive

        new_group.created = datetime.utcnow()

        new_group.save_to_db()

    else:
        group.alive = alive
        group.save_to_db()


def update_message(sid, message):
    message_dict = message

    in_message = Message()

    if message_dict['author'] == 'user':
        in_message.direction = 'incoming'
        in_message.message_owner = 'customer'
    else:
        in_message.direction = 'outgoing'
        in_message.message_owner = 'admin'
    # in_message.message = json.dumps({'messages': texts})
    in_message.message = json.dumps(message)
    in_message.session_id = sid
    in_message.from_bot = 0
    in_message.is_read = 0
    in_message.created_time = datetime.utcnow()

    in_message.save_to_db()
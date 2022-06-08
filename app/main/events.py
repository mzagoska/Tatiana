from flask import session

from flask_socketio import emit, join_room, leave_room
from .. import socketio
from main import to_text, talk_to_file


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    msg = message
    print(msg)
    print(room)
    emit('msg', {'msg': msg}, room=room)

@socketio.on('radio', namespace='/chat')
def voice(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    msg = to_text(message)
    #msg = "Вы сказали: " + msg
    emit('msg', {'msg': message}, room=room)
    emit('voice', message, room=room)
    #mess = talk_to_file(msg)
    print(message)
    print(msg)
    print(room)
    #emit('voice', mess, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


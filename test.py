import socketio
import json

sio = socketio.Client()

ROOM_ID = "253a8dea-48f8-410e-b539-4546cb8959f1"

@sio.event
def connect():
    print('Connected to server')
    sio.emit('join_room', {'conversation_id': ROOM_ID})
    print(f'Emitted join_room-{ROOM_ID} with id: {ROOM_ID}')

def print_response(response):
    print('Server response on connect:', response)

@sio.on('message')
def on_message(data):
    if isinstance(data, str):
        data = json.loads(data)
    print('Received:', data)
    conversation_id = data.get('new_conversation_id')
    if conversation_id:
        sio.emit('join_room', {'conversation_id': conversation_id})
        print(f'Emitted join_room-{conversation_id} with id: {conversation_id}')

# Listen on channel chat:{ROOM_ID}
@sio.on('completed')
def on_completed(data):
    print('Received completed event:', data)

@sio.event
def disconnect():
    print('Disconnected from server')

sio.connect('https://socketio-server-production-a953.up.railway.app')
sio.wait()
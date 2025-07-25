import os
import sys
import socketio
import asyncio
import json 
from redis import asyncio as aioredis

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from core.config import settings 

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('status', {'status': 'connected'}, room=sid) 

# @sio.on('join_room-{id}')
# async def join_room(sid, data):
#     conversation_id = data.get('new_conversation_id')
#     if conversation_id:
#         room_name = f"chat:{conversation_id}"
#         sio.enter_room(sid, room_name)
#         print(f"Client {sid} joined room: {room_name}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

async def redis_listener(sio_app):
    """
    Lắng nghe các kênh chat:* trên Redis và emit sự kiện tới client.
    """
    redis_conn = aioredis.from_url(settings.REDIS_URL)
    pubsub = redis_conn.pubsub()
    await pubsub.psubscribe("chat:*")
    print("Redis listener started...")

    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if not message or message['type'] != 'pmessage':
                await asyncio.sleep(0.01)
                continue

            room_name = message['channel'].decode('utf-8')
            
            try:
                event_data = json.loads(message['data'])
                event_name = event_data.get('type')
                payload = event_data.get('data', {})

                if not event_name:
                    print(f"Warning: Received message without a 'type' on {room_name}")
                    continue
                await sio_app.emit(event_name, payload)

            except json.JSONDecodeError:
                print(f"Error decoding JSON from message on {room_name}: {message['data']}")
            except Exception as e:
                print(f"Error processing message from {room_name}: {e}")

        except Exception as e:
            print(f"Redis listener main loop error: {e}")
            # Đợi một chút trước khi thử lại để tránh vòng lặp lỗi nóng
            await asyncio.sleep(1)
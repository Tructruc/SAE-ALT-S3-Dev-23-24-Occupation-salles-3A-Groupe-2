import redis

def redis_sender(channel_name, message):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.publish('sse', str(
            {
                'type': f'{channel_name}', 
                'message': f'{message}'
            }
        )
    )
import threading

def start_thread_redis_listener():
    from app.usecases.redis import redis_listener
    stop_event = threading.Event()
    thread = threading.Thread(target=redis_listener, args=(stop_event,))
    thread.daemon = True
    thread.start()

    return thread, stop_event

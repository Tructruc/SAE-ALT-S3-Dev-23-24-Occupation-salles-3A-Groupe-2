def start_thread_redis_listener() :
    import threading

    from app.usecases.redis import redis_listener

    thread = threading.Thread(target=redis_listener)
    thread.daemon = True
    thread.start()

    return thread


def transaction(lock):
    def decorator(func):
        def wrapper(*args, **kwargs):
            lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                lock.release()
                
        return wrapper
    return decorator

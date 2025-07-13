from threading import Thread


def run_in_thread(target, *args, **kwargs):
    t = Thread(target=target, args=args, kwargs=kwargs)
    t.start()
    return t

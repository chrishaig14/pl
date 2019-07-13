DEBUG = False
ACTIVE = True

def log(*args):
    if not ACTIVE:
        return

    print(*args)


def debug(*args):
    if not ACTIVE:
        return
    if DEBUG:
        print(*args)


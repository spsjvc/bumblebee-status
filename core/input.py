import uuid
import util.cli

LEFT_MOUSE = 1
MIDDLE_MOUSE = 2
RIGHT_MOUSE = 3
WHEEL_UP = 4
WHEEL_DOWN = 5

callbacks = {}

class Object(object):
    def __init__(self):
        super(Object, self).__init__()
        self._id = str(uuid.uuid4())

    def id(self):
        return self._id

def register(obj, button=None, cmd=None):
    callbacks.setdefault(obj.id(), {}).setdefault(button, []).append(cmd)

def trigger(event):
    for field in ['instance', 'name']:
        if field in event:
            cb = callbacks.get(event[field])
            _invoke(event, cb)

def _invoke(event, callback):
    if not callback: return
    if not 'button' in event: return

    for cb in callback.get(event['button']):
        if callable(cb):
            cb(event)
        else:
            util.cli.execute(cb, wait=False)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
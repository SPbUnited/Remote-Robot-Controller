from pyee import EventEmitter
from .events import load_events


def event_emitter(app):

    ee = EventEmitter(loop=app.loop)
    load_events(app, ee)

    return ee


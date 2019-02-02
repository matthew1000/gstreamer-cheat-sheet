#!/usr/bin/env python
#
# Plays any URI to screen. And shows how to handle buffering.
#
# Make sure the environment variable SRC is set to a playable file
# e.g.
#   export SRC='file:///tmp/me.mp4'
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()
pipeline = None

def on_state_change(bus, message):
    is_pipeline_state_change = isinstance(message.src, Gst.Pipeline)
    if is_pipeline_state_change:
        old_state, new_state, pending_state = message.parse_state_changed()
        print('State is now %s' % new_state.value_nick.upper())

        if new_state == Gst.State.PAUSED:
            consider_move_to_playing_if_not_buffering()

def consider_move_to_playing_if_not_buffering():
    query_buffer = Gst.Query.new_buffering(Gst.Format.PERCENT)
    result = pipeline.query(query_buffer)

    if result:
        result_parsed = query_buffer.parse_buffering_percent()
        buffering_is_busy = result_parsed.busy
        if not buffering_is_busy:
            pipeline.set_state(Gst.State.PLAYING)


def on_error(bus, message):
    print('ERROR:', message.parse_error())

def on_buffering(bus, message):
    if pipeline.get_state(0)[1] in [Gst.State.PAUSED, Gst.State.PLAYING]:
        buffering_percent = message.parse_buffering()
        print('Buffering %d%%' % buffering_percent)
        if pipeline.get_state(0)[1] == Gst.State.PAUSED and buffering_percent == 100:
            pipeline.set_state(Gst.State.PLAYING)

        # The percentage goes to 0 too soon. So setting back to PAUSED can cause a needless streamingn blip.
        # if pipeline.get_state(0)[1] == Gst.State.PLAYING and buffering_percent == 0:
        #     pipeline.set_state(Gst.State.PAUSED)

def go():
    global pipeline
    pipeline = Gst.ElementFactory.make('playbin')
    pipeline.set_property('uri', os.environ['SRC'])

    # How large a buffer would you like?
    pipeline.set_property('buffer-duration', 3 * Gst.SECOND)

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message::buffering', on_buffering)
    bus.connect('message::state-changed', on_state_change)
    bus.connect('message::error', on_error)

    pipeline.set_state(Gst.State.PAUSED)
    mainloop.run()

go()

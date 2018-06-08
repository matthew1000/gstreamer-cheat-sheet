#!/usr/bin/env python
# Shows how two pipelines can be connected, using proxysink/proxysrc
# This example uses Playbin to read a file, and send the video and audio to separate proxies.
# Unlike just using playbin directly, this will never end, as the other pipelines will continue 'listening'.
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipe1 = Gst.parse_launch("playbin uri=\"file://" + os.environ['SRC'] + "\"")
playsink = pipe1.get_by_name('playsink')

psink1 = Gst.ElementFactory.make("proxysink", "psink1")
psink2 = Gst.ElementFactory.make("proxysink", "psink2")
playsink.set_property('video-sink', psink1)
playsink.set_property('audio-sink', psink2)

pipe2 = Gst.parse_launch("proxysrc name=psrc1 ! autovideosink")
psrc1 = pipe2.get_by_name('psrc1')
psrc1.set_property('proxysink', psink1)

pipe3 = Gst.parse_launch("proxysrc name=psrc2 ! autoaudiosink")
psrc2 = pipe3.get_by_name('psrc2')
psrc2.set_property('proxysink', psink2)

clock = Gst.SystemClock.obtain()
pipe1.use_clock(clock)
pipe2.use_clock(clock)
pipe3.use_clock(clock)
clock.unref()

pipe1.set_base_time(0)
pipe2.set_base_time(0)
pipe3.set_base_time(0)

pipe1.set_state(Gst.State.PLAYING)
pipe2.set_state(Gst.State.PLAYING)
pipe3.set_state(Gst.State.PLAYING)

def on_error(bus, message):
    print(message.parse_error())

bus1 = pipe1.get_bus()
bus1.add_signal_watch()
bus1.connect('message::error', on_error)

mainloop.run()

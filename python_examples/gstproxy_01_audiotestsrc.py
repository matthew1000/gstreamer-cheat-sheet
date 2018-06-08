#!/usr/bin/env python
# Shows how two pipelines can be connected, using proxysink/proxysrc.
# It will output a test audio sound.
# Python equivalent of example at https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad-plugins/html/gst-plugins-bad-plugins-proxysrc.html
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipe1 = Gst.parse_launch("audiotestsrc is-live=1 ! proxysink name=psink")
psink = pipe1.get_by_name('psink')

pipe2 = Gst.parse_launch("proxysrc name=psrc ! autoaudiosink")
psrc = pipe2.get_by_name('psrc')

psrc.set_property('proxysink', psink)

clock = Gst.SystemClock.obtain()
pipe1.use_clock(clock)
pipe2.use_clock(clock)
clock.unref()

pipe1.set_base_time(0)
pipe2.set_base_time(0)

pipe1.set_state(Gst.State.PLAYING)
pipe2.set_state(Gst.State.PLAYING)

mainloop.run()

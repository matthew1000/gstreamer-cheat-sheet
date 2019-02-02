#!/usr/bin/env python
#
# Sends a test stream to a fake sink.
# This is utterly pointless, but allows easy testing of GStreamer
# Python on a remote box that doesn't have video.
#
# Equivalent to:
#    gst-launch-1.0 videotestsrc ! fakesink
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipeline =  Gst.Pipeline.new("pipe")

videotestsrc = Gst.ElementFactory.make("videotestsrc", "videotestsrc")
fakesink = Gst.ElementFactory.make("fakesink", "fakesink")

pipeline.add(videotestsrc)
pipeline.add(fakesink)

videotestsrc.link(fakesink)

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()

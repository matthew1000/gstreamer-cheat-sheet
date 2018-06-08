#!/usr/bin/env python
#
# Plays a test screen to screen.
#
# Equivalent to:
#    gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipeline =  Gst.Pipeline.new("pipe")

videotestsrc = Gst.ElementFactory.make("videotestsrc")
videoconvert = Gst.ElementFactory.make("videoconvert")
autovideosink = Gst.ElementFactory.make("autovideosink")

pipeline.add(videotestsrc)
pipeline.add(videoconvert)
pipeline.add(autovideosink)

videotestsrc.link(videoconvert)
videoconvert.link(autovideosink)

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()

#!/usr/bin/env python

'''
An example of how dynamic values can work for properties such as size and position.
Here an image moves across (in the first second) and then enlarges (in seconds 1-3).
'''

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstController', '1.0')
from gi.repository import GObject, Gst, GstController
import os
from time import sleep
from threading import Thread

def get_timing_controller(pad, field):
    cs = GstController.InterpolationControlSource()
    cs.set_property('mode', GstController.InterpolationMode.LINEAR)

    cb = GstController.DirectControlBinding.new_absolute(pad, field, cs)
    pad.add_control_binding(cb)
    return cs

Gst.init(None)
mainloop = GObject.MainLoop()
pipe = Gst.parse_launch(\
    "videotestsrc pattern=4 ! "
    "timeoverlay valignment=top font-desc=\"Sans, 50\" ! "
    "compositor name=compositor sink_1::width=80 sink_1::height=45 sink_1::ypos=50 ! autovideosink"
    " videotestsrc pattern=5 ! compositor.")
compositor = pipe.get_by_name('compositor')
textoverlay = pipe.get_by_name('textoverlay')

sink1 = compositor.get_static_pad('sink_1')
xpos_cs = get_timing_controller(sink1, 'xpos')
xpos_cs.set(0*Gst.SECOND, 150)
xpos_cs.set(1*Gst.SECOND, 50)

width_cs = get_timing_controller(sink1, 'width')
width_cs.set(1*Gst.SECOND, 80)
width_cs.set(3*Gst.SECOND, 160)

height_cs = get_timing_controller(sink1, 'height')
height_cs.set(1*Gst.SECOND, 45)
height_cs.set(3*Gst.SECOND, 90)

pipe.set_state(Gst.State.PLAYING)
mainloop.run()

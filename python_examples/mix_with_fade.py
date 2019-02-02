#!/usr/bin/env python

'''
An example of how fading can work into a compositor (mixer).
Similar to a Gist at https://gist.github.com/lsiden/649d8ef9e02758ffde30b2b10fbac45a

'''

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstController', '1.0')
from gi.repository import GObject, Gst, GstController
import os
from time import sleep
from threading import Thread

def get_alpha_controller(pad):
    cs = GstController.InterpolationControlSource()
    cs.set_property('mode', GstController.InterpolationMode.LINEAR)

    cb = GstController.DirectControlBinding.new(pad, 'alpha', cs)
    pad.add_control_binding(cb)
    return cs

Gst.init(None)
mainloop = GObject.MainLoop()
pipe = Gst.parse_launch("videotestsrc ! timeoverlay name=timeoverlay halignment=right font-desc=\"Sans, 50\" deltax=10 ! "      "compositor name=compositor sink_1::width=100 ! "
    "autovideosink videotestsrc pattern=1 ! compositor.")
compositor = pipe.get_by_name('compositor')

sink1 = compositor.get_static_pad('sink_1')
cs = get_alpha_controller(sink1)
is_showing = True
# cs.set(0*Gst.SECOND, 0)
# cs.set(1*Gst.SECOND, 1)
# cs.set(2*Gst.SECOND, 0)
# cs.set(3*Gst.SECOND, 0)
# cs.set(4*Gst.SECOND, 1)

pipe.set_state(Gst.State.PLAYING)

# Separate thread to provide user interaction:
def separate_thread():
    global is_showing
    while True:
        input("Press enter to fade...")
        current = 0
        dest = 1
        if is_showing:
            current = 1
            dest = 0

        pos = pipe.query_position(Gst.Format.TIME).cur
        print('Moving from %d to %d' % (current, dest))
        cs.set(pos, current)
        cs.set(pos + 1*Gst.SECOND, dest)
        is_showing = not is_showing


myThread = Thread(target=separate_thread, args=())
myThread.start()

mainloop.run()

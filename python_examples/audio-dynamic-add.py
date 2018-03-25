#!/usr/bin/python
# Shows how two test sources can be mixed together.
#
# A variation of what's on
# https://stackoverflow.com/questions/3899666/adding-and-removing-audio-sources-to-from-gstreamer-pipeline-on-the-go


import os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk

Gst.init(None)
GObject.threads_init()

# def buzzersrc1_probe_callback(a,b):
#     print("buzzersrc1_probe_callback called")

if __name__ == "__main__":
    # First create our pipeline
    pipe = Gst.Pipeline.new("mypipe")

    audiomixer = Gst.ElementFactory.make("audiomixer","audiomixer")
    pipe.add(audiomixer)

    # Gather a request sink pad on the mixer
    sinkpad1=audiomixer.get_request_pad("sink_%u")
    print("sinkpad1:" + str(sinkpad1))

    # Create the first buzzer..
    buzzer1 = Gst.ElementFactory.make("audiotestsrc","buzzer1")
    buzzer1.set_property("freq",1000)
    pipe.add(buzzer1)
    # .. and connect it's source pad to the previously gathered request pad
    buzzersrc1=buzzer1.get_static_pad("src")
    buzzersrc1.link(sinkpad1)

    # Add some output
    output = Gst.ElementFactory.make("autoaudiosink", "audio_out")
    pipe.add(output)
    audiomixer.link(output)

    # Start the playback
    pipe.set_state(Gst.State.PLAYING)

    input("1kHz test sound. Press <ENTER> to continue.")

    # Get an another request sink pad on the mixer
    sinkpad2=audiomixer.get_request_pad("sink_%u")

    # Create an another buzzer and connect it the same way
    buzzer2 = Gst.ElementFactory.make("audiotestsrc","buzzer2")
    buzzer2.set_property("freq",500)
    pipe.add(buzzer2)

    buzzersrc2=buzzer2.get_static_pad("src")
    buzzersrc2.link(sinkpad2)

    # Start the second buzzer (other ways streaming stops because of starvation)
    buzzer2.set_state(Gst.State.PLAYING)

    input("1kHz + 500Hz test sound playing simoultenously. Press <ENTER> to continue.")

    # Before removing a source, we must use pad blocking to prevent state changes
    # buzzersrc1.set_blocked(True)
    # I think this gets replaced with:
    # buzzersrc1.add_probe(Gst.PadProbeType.BLOCK_DOWNSTREAM, buzzersrc1_probe_callback)
    # but it doesn't seem to be required.

    # Stop the first buzzer
    buzzer1.set_state(Gst.State.NULL)
    # Unlink from the mixer
    buzzersrc1.unlink(sinkpad2)
    # Release the mixers first sink pad
    audiomixer.release_request_pad(sinkpad1)
    # Because here none of the audiomixer's sink pads block, streaming continues

    input("Only 500Hz test sound. Press <ENTER> to stop.")

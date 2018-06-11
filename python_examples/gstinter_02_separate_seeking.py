#!/usr/bin/env python
'''
To run this, set the environment variables $SRC and $SRC2 to full paths to two mp4 files.

This has three pipelines:

- Pipeline 1 plays the file $SRC
- Pipeline 2 plays the file $SRC2
- Pipeline 3 displays them mixed

Pipeline-1 --\
              ---> Pipeline3
Pipeline 2 --/

This demo shows how, by splitting into pipelines, each soure can be seeked independently.
And if one fails (e.g. file not found), the other continues.
'''

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os
from time import sleep
from threading import Thread

Gst.init(None)
mainloop = GObject.MainLoop()

# We make the two pipelines
pipe1 = Gst.parse_launch("playbin uri=\"file://" + os.environ['SRC'] + "\"")
pipe2 = Gst.parse_launch("playbin uri=\"file://" + os.environ['SRC2'] + "\"")

# The third pipeline is more complex as it has to accept the other two, and mix.
pipe3 = Gst.parse_launch(
    "intervideosrc name=video_src_1 ! videomix. " +
    "interaudiosrc name=audio_src_1 ! autoaudiosink "
    "intervideosrc name=video_src_2 ! videomix. " +
    "interaudiosrc name=audio_src_2 ! autoaudiosink " +
    "compositor name=videomix sink_1::xpos=800 sink_1::ypos=800  ! autovideosink "
    )

# Because 'playbin' is a bin rather than element, the bit we want within it is 'playsink':
pipe1_playsink = pipe1.get_by_name('playsink')
pipe2_playsink = pipe2.get_by_name('playsink')

audio_src_1 = pipe3.get_by_name('audio_src_1')
video_src_1 = pipe3.get_by_name('video_src_1')
audio_src_2 = pipe3.get_by_name('audio_src_2')
video_src_2 = pipe3.get_by_name('video_src_2')

# Make the sinks for the first two pipelines:
video_sink_1 = Gst.ElementFactory.make("intervideosink", "video_sink_1")
audio_sink_1 = Gst.ElementFactory.make("interaudiosink", "audio_sink_1")
video_sink_2 = Gst.ElementFactory.make("intervideosink", "video_sink_2")
audio_sink_2 = Gst.ElementFactory.make("interaudiosink", "audio_sink_2")
pipe1_playsink.set_property('video-sink', video_sink_1)
pipe1_playsink.set_property('audio-sink', audio_sink_1)
pipe2_playsink.set_property('video-sink', video_sink_2)
pipe2_playsink.set_property('audio-sink', audio_sink_2)

# We use 'channel' to name the two different connections between
video_sink_1.set_property('channel', 'video-channel-1')
audio_sink_1.set_property('channel', 'audio-channel-1')
video_src_1.set_property('channel', 'video-channel-1')
audio_src_1.set_property('channel', 'audio-channel-1')
video_sink_2.set_property('channel', 'video-channel-2')
audio_sink_2.set_property('channel', 'audio-channel-2')
video_src_2.set_property('channel', 'video-channel-2')
audio_src_2.set_property('channel', 'audio-channel-2')

# Off we go!
pipe1.set_state(Gst.State.PLAYING)
pipe2.set_state(Gst.State.PLAYING)
pipe3.set_state(Gst.State.PLAYING)

# This bit allows the user to specitfy different offsets for each video
def separate_thread():
    while True:
        seconds = input("Enter the number of seconds to jump the FIRST video to (0=start): ")
        pipe1.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, Gst.SECOND * int(seconds))
        seconds = input("Enter the number of seconds to jump the SECOND video to (0=start): ")
        pipe2.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, Gst.SECOND * int(seconds))

myThread = Thread(target=separate_thread, args=())
myThread.start()

mainloop.run()

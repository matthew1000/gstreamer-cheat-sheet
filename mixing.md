# Mixing (GStreamer command-line cheat sheet)

This page talks about mixing video (i.e. replacing or overlaying), and also mixing audio (i.e. replacing or merging audio tracks). We'll do one at a time.

## Mixing video

The element `compositor` allows video to be mixed (overlayed, put side-by-side, etc).

The older `videomixer` element can be used instead, and takes the same arguments as `compositor` so it's easy to swap between them. However, `videomixer` is apparently inferior in some situations, such as for live streams.

### Picture in picture

Here we have two source (mp4) files, which should be set as environment variables `$SRC` and `$SRC2`

```
gst-launch-1.0   \
    filesrc location="$SRC2" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    compositor name=mix sink_0::alpha=1 sink_1::alpha=1 !   \
    videoconvert ! autovideosink \
    filesrc location="$SRC" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

Put a box around the in-picture using ‘videobox’ e.g.

```
gst-launch-1.0   \
    filesrc location="$SRC2" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    compositor name=mix sink_0::alpha=1 sink_1::alpha=1 !   \
    videoconvert ! autovideosink \
    filesrc location="$SRC" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    videobox border-alpha=0 top=-10 bottom=-10 right=-10 left=-10 ! \
    mix.
```

Choose where the in-picture goes with the ‘xpos’ and ‘ypos’ attributes of videomixer, e.g.

```
gst-launch-1.0   \
    filesrc location="$SRC2" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    compositor name=mix sink_0::alpha=1 sink_1::alpha=1 sink_1::xpos=50 sink_1::ypos=50 !   \
    videoconvert ! autovideosink \
    filesrc location="$SRC" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

Add audio by demuxing the inputs so it can be handled separately. This example does so on the first source (rather than mixing the two together):

```
gst-launch-1.0   \
    filesrc location="$SRC" ! \
    qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    autoaudiosink \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    compositor name=mix sink_0::alpha=1 sink_1::alpha=1 sink_1::xpos=50 sink_1::ypos=50 !   \
    videoconvert ! autovideosink \
    filesrc location="$SRC2" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

### Compositor with just one source

It is possible for a compositor to have just one source. This example has the test source of a bouncing ball. It also has the audio test source included (muxed).

```
gst-launch-1.0   \
    videotestsrc pattern=ball ! \
    decodebin ! \
    compositor name=mix sink_0::alpha=1 ! \
    x264enc ! muxer. \
    audiotestsrc ! avenc_ac3 ! muxer. \
    mpegtsmux name=muxer ! queue ! \
    tcpserversink host=127.0.0.1 port=7001 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

## Mixing audio

Use the `audiomixer` element to mix audio. It replaces the `adder` element, which struggles under some circumstances (according to the [GStreamer 1.14 release notes](https://gstreamer.freedesktop.org/releases/1.14/)).

Mix to audio streams:

```
gst-launch-1.0 audiotestsrc freq=100 ! audiomixer name=mix ! audioconvert ! alsasink audiotestsrc freq=500 ! mix.
```

[This Python example](python_examples/audio_dynamic_add.py) shows a dynamic equivalent of this example - the second test source is only mixed when the user presses Enter.

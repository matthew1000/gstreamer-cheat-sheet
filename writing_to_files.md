# Writing to files (GStreamer command-line cheat sheet)

The [`filesink`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-filesink.html) element allows writing to a file.

Note that, when using the command-line, the `-e` parameter ensures the output file is correctly completed on exit.


### Write to an mp4 file

This example creates a test video (animated ball moving, with clock), and writes it as an MP4 file.
Also added is an audio test source - a short beep every second.

Leave it running for a few seconds, and then CTRL-C to stop it.

```
gst-launch-1.0 -e videotestsrc pattern=ball ! \
    video/x-raw,width=1280,height=720 ! \
    timeoverlay font-desc="Sans, 48" ! \
    x264enc ! mux. \
    audiotestsrc is-live=true wave=ticks ! audioconvert ! audioresample ! faac bitrate=32000 ! mux.  \
    mp4mux name=mux ! filesink location=file.mp4
```

gst-launch-1.0 -e videotestsrc pattern=ball ! \
    video/x-raw,width=640,height=320 ! \
    x264enc ! mux. \
    audiotestsrc is-live=true freq=200 ! audioconvert ! audioresample ! faac bitrate=32000 ! mux.  \
    mp4mux name=mux ! filesink location=file.mp4


### Other examples

*TODO* more descriptions here!

 ```
 gst-launch-1.0 -e videotestsrc ! video/x-raw-yuv, framerate=25/1, width=640, height=360 ! x264enc ! \
               mpegtsmux ! filesink location=test.ts
```

```
gst-launch-1.0 -e videotestsrc !\
    x264enc !\
    mpegtsmux !\
    filesink location=test.ts
```

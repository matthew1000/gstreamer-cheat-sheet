# Capturing images (GStreamer command-line cheat sheet)

The [`shmsink`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad/html/gst-plugins-bad-plugins-shmsink.html) element allows you to write video into shared memory, from which another gstreamer application can read it with [`shmsrc`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad/html/gst-plugins-bad-plugins-shmsrc.html).

### Puttingn a stream into memory

```
gst-launch-1.0 -v videotestsrc ! \
    'video/x-raw, format=(string)I420,  width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    queue !  identity ! \
    shmsink wait-for-connection=1 socket-path=/tmp/tmpsock  shm-size=20000000 sync=true  
```

Another example, this time from a file rather than test source, and keeping the audio local:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    autoaudiosink \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! videoscale ! videorate ! \
    'video/x-raw, format=(string)I420,  width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    queue !  identity ! \
    shmsink wait-for-connection=0 socket-path=/tmp/tmpsock  shm-size=20000000 sync=true  
```

### Reading a stream from memory

```
gst-launch-1.0 shmsrc socket-path=/tmp/tmpsock ! \
    'video/x-raw, format=(string)I420, width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    autovideosink
````



# RTMP (GStreamer command-line cheat sheet)

GStreamer can receive an RTMP stream from an RTMP server. It can also send an RTMP stream to an RTMP server.

If you need your own RTMP server, [the Nginx RTMP extension](https://github.com/arut/nginx-rtmp-module) works quite well though is no longer supported.

### Play an RTMP stream

To play from RTMP server, playbin can be used (as with files and HLS streams):

```
gst-launch-1.0 playbin uri=$RTMP_SRC
```

A test RTMP stream is available at `rtmp://184.72.239.149/vod/BigBuckBunny_115k.mov` which serves as a useful example:

```
gst-launch-1.0 playbin uri='rtmp://184.72.239.149/vod/BigBuckBunny_115k.mov'
```

Instead of using `playbin`, it's possible to get video only with `uridecodebin` then shown with `autovideosink`:

```
gst-launch-1.0 uridecodebin uri=$RTMP_SRC ! autovideosink
```

Or as a step further we can split out into the source and decode too. This does video:

```
gst-launch-1.0 rtmpsrc location=$RTMP_SRC ! decodebin ! autovideosink
```

and this does the audio:

```
gst-launch-1.0 rtmpsrc name=rtmpsrc location=$RTMP_SRC ! decodebin ! \
queue ! audioconvert ! autoaudiosink
```

We can vget flvdemux to pull out the audio:

```
gst-launch-1.0 rtmpsrc location=$RTMP_SRC ! \
    flvdemux name=t  t.audio ! decodebin ! autoaudiosink
```

Incidentally, all of these work with a direct flv file:

```
gst-launch-1.0 filesrc location="/Users/clarkm22/workspace/silver/assets/test.flv" ! \
    flvdemux name=t  t.audio ! decodebin ! autoaudiosink
```

If you want to use `flvdemux` to do the video, you need to capture the audio too or else it will fail. This example puts it in `fakesink` which is basically discarding it:

```
gst-launch-1.0 rtmpsrc location="$RTMP_SRC" ! \
    flvdemux name=demux \
    demux.audio ! queue ! decodebin ! fakesink \
    demux.video ! queue ! decodebin ! autovideosink
```

You could then use this to capture the RTMP as an MP4, e.g.

```
gst-launch-1.0 -e rtmpsrc location="$RTMP_SRC" ! \
    flvdemux name=demux \
    demux.audio ! queue ! decodebin ! audioconvert ! faac bitrate=32000 ! mux. \
    demux.video ! queue ! decodebin ! videoconvert ! video/x-raw,format=I420 ! x264enc speed-preset=superfast tune=zerolatency psy-tune=grain sync-lookahead=5 bitrate=480 key-int-max=50 ref=2  ! mux. \
    mp4mux name=mux ! filesink location="out.mp4"
```

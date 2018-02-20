# RTMP (GStreamer command-line cheat sheet)

GStreamer can receive an RTMP stream from an RTMP server. It can also send an RTMP stream to an RTMP server.

If you need your own RTMP server, [the Nginx RTMP extension](https://github.com/arut/nginx-rtmp-module) works quite well though is no longer supported.

### Play an RTMP stream

To play from RTMP server, at the path `/live/x`, with the server name in the environment variable `RTMP_SERVER`:

```
gst-launch-1.0 uridecodebin uri='rtmp://$RTMP_SERVER/live/x' ! \
    videoconvert ! videorate ! videoscale ! videoconvert ! \
    video/x-raw, format=BGRA, pixel-aspect-ratio=1/1, interlace-mode=progressive,framerate=24/1, width=640, height=360 ! \
    autovideosink
```

Russia Today is available over RTMP at `https://rtmp.api.rt.com/hls/rtdru360.m3u8`. So you can watch it with:

```
gst-launch-1.0 uridecodebin uri='https://rtmp.api.rt.com/hls/rtdru360.m3u8' ! \
    videoconvert ! videorate ! videoscale ! videoconvert ! \
    video/x-raw, format=BGRA, pixel-aspect-ratio=1/1, interlace-mode=progressive,framerate=24/1, width=640, height=360 ! \
    autovideosink
```

### Stream TO an RTMP server

At the path '/live/x', with the server name in the environment variable `RTMP_SERVER`:

```
gst-launch-1.0 videotestsrc \
    is-live=true ! queue ! x264enc ! flvmux name=muxer ! \
    rtmpsink location='rtmp://$RTMP_SERVER/live/x'
```

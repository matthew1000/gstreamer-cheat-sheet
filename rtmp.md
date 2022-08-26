# RTMP (GStreamer command-line cheat sheet)

GStreamer can:
* retrieve an RTMP stream from an RTMP server, and
* also send an RTMP stream to an RTMP server (including YouTube).

If you need your own RTMP server, [the Nginx RTMP extension](https://github.com/arut/nginx-rtmp-module) works quite well. [Linode has a good NGINX RTMP installation guide.](https://www.linode.com/docs/guides/set-up-a-streaming-rtmp-server/)

### Play an RTMP stream

RTMP can be live streams, or on-demand streams - playback is the same in both cases.

To play from RTMP server, [playbin](https://gstreamer.freedesktop.org/documentation/playback/playbin.html) can be used. (Playbin is magical - it can also play files, HLS streams, DASH streams, and many other sources!) Example:

```
export RTMP_SRC="rtmp://matthewc.co.uk/vod/scooter.flv"
gst-launch-1.0 playbin uri=$RTMP_SRC
```

A test RTMP VOD stream is available at `rtmp://matthewc.co.uk/vod/scooter.flv` which serves as a useful example:

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

Incidentally, all of these work with a direct *flv* file:

```
gst-launch-1.0 filesrc location="/path/to/test.flv" ! \
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

According to [this conversation](http://gstreamer-devel.966125.n4.nabble.com/flvdemux-working-sometimes-td4677796.html), the following also works, although personally I find it intermittent:

```
export QUEUE="queue max-size-time=0 max-size-bytes=0 max-size-buffers=0"

gst-launch-1.0 \
    rtmpsrc location="$RTMP_SRC live=1" ! \
    $QUEUE                          ! \
    flvdemux name=demux             ! \
    $QUEUE                          ! \
    aacparse                        ! \
    avdec_aac                       ! \
    autoaudiosink sync=0 demux.video ! \
    $QUEUE                          ! \
    h264parse                       ! \
    avdec_h264                      ! \
    $QUEUE                          ! \
    videoconvert                    ! \
    autovideosink sync=0
```

### Adding an RTMP as picture-in-Picture

This overlays an RTMP source as a picture-in-picture on top of a local filesource (set as `$SRC`)

```
export QUEUE="queue max-size-time=0 max-size-bytes=0 max-size-buffers=0"
gst-launch-1.0 \
    filesrc location="$SRC" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    compositor name=mix sink_0::alpha=1 sink_1::alpha=1 sink_1::xpos=50 sink_1::ypos=50 !   \
    videoconvert ! autovideosink \
    rtmpsrc location="$RTMP_SRC" ! \
    flvdemux name=demux \
    demux.audio ! $QUEUE ! decodebin ! autoaudiosink \
    demux.video ! $QUEUE ! decodebin ! \
    videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

## Sending a live stream to an RTMP server

The examples below use the `RTMP_DEST` environment variable. You can set it to reference your RTMP server, e.g.

```
export RTMP_DEST="rtmp://example.com/live/test"
```

If you're using [Nginx RTMP](https://github.com/arut/nginx-rtmp-module), the name configured for your application needs to be the first part of the URL path. For example, if your NGINX configuration is:

```
rtmp {
    server {
        listen 1935;
        hunk_size 4096;
        notify_method get;

        application livestream {
            live on;
        }
    }
}
```

then the application name is `livestream`, and so your URL will be `rtmp://<your-domain>/livestream/<stream-name>` (where `<stream-name> can be anything`).

### Sending a test live stream to an RTMP server

To send a video test source:

```
gst-launch-1.0 videotestsrc  is-live=true ! \
    queue ! x264enc ! flvmux name=muxer ! rtmpsink location="$RTMP_DEST live=1"
```

To send an audio test source (note: `flvmux` is still required even though there is no muxing of audio & video):

```
gst-launch-1.0 audiotestsrc is-live=true ! \
    audioconvert ! audioresample ! audio/x-raw,rate=48000 ! \
    voaacenc bitrate=96000 ! audio/mpeg ! aacparse ! audio/mpeg, mpegversion=4 ! \
    flvmux name=mux ! \
    rtmpsink location=$RTMP_DEST
```

This sends both video and audio as a test source:

```
gst-launch-1.0 videotestsrc is-live=true ! \
    videoconvert ! x264enc bitrate=1000 tune=zerolatency ! video/x-h264 ! h264parse ! \
    video/x-h264 ! queue ! flvmux name=mux ! \
    rtmpsink location=$RTMP_DEST audiotestsrc is-live=true ! \
    audioconvert ! audioresample ! audio/x-raw,rate=48000 ! \
    voaacenc bitrate=96000 ! audio/mpeg ! aacparse ! audio/mpeg, mpegversion=4 ! mux.
```

### Live streaming to YouTube via RTMP

YouTube accepts live RTMP streams. They must have both audio and video.

Set up a stream by visiting [YouTube.com](https://www.youtube.com/) on desktop, and selecting 'Create' from the top-right.

YouTube will provide a 'Stream URL' and a 'Stream key'. Combine these to create the full URL.

For example, if the URL is `rtmp://a.rtmp.youtube.com/live2` and the key is `abcd-1234-5678`, then:

```
export RTMP_DEST="rtmp://a.rtmp.youtube.com/live2/abcd-1234-5678"
```

Given the  [YouTube stream suggestions](https://support.google.com/youtube/answer/2853702)) here's a good test stream:

```
gst-launch-1.0 \
    videotestsrc is-live=1 \
    ! videoconvert \
    ! "video/x-raw, width=1280, height=720, framerate=30/1" \
    ! queue \
    ! x264enc cabac=1 bframes=2 ref=1 \
    ! "video/x-h264,profile=main" \
    ! flvmux streamable=true name=mux \
    ! rtmpsink location="${RTMP_DEST} live=1" \
    audiotestsrc is-live=1 wave=ticks \
    ! voaacenc bitrate=128000 \
    ! mux.
```

### Send a file over RTMP

Audio & video:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! x264enc bitrate=1000 tune=zerolatency ! video/x-h264 ! h264parse ! \
    video/x-h264 ! queue ! flvmux name=mux ! \
    rtmpsink location=$RTMP_DEST \
    demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    audio/x-raw,rate=48000 ! \
    voaacenc bitrate=96000 ! audio/mpeg ! aacparse ! audio/mpeg, mpegversion=4 ! mux.
```

Just video:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! x264enc bitrate=1000 tune=zerolatency ! video/x-h264 ! h264parse ! \
    video/x-h264 ! queue ! flvmux name=mux ! \
    rtmpsink location=$RTMP_DEST
```

## Misc: latency

There's a comment about reducing latency at https://lists.freedesktop.org/archives/gstreamer-devel/2018-June/068076.html

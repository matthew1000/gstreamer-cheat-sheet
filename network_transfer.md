# Transfer of audio/video via a network socket  (GStreamer command-line cheat sheet)

GStreamer can send and receive audio and video via a network socket, using either UDP or TCP.

*UDP* is faster but lossy - there is no attempt to resend lost network packets to it will fail if the network is not perfect. *TCP* acknowledges every network packet so is slower, but more reliable.

See also [SRT](srt.md) as an alternative format.

## UDP

### Audio via UDP

To send an audio test source:

```
gst-launch-1.0 audiotestsrc ! avenc_ac3 ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=7001
```

To send an audio file:

```
# Make sure $SRC is set to an audio file (e.g. an MP3 file)
gst-launch-1.0 -v filesrc location=$AUDIO_SRC ! mpegaudioparse ! udpsink port=7001
```

And to receive audio:

```
gst-launch-1.0 udpsrc port=7001 ! decodebin ! autoaudiosink
```

### Video via UDP, as h264

To send a test stream:

```
gst-launch-1.0 videotestsrc ! decodebin ! x264enc ! rtph264pay ! udpsink port=7001
```

Or to send a file (video or audio only, not both):

```
# Make sure $SRC is set to an video file (e.g. an MP4 file)
gst-launch-1.0  filesrc location=$SRC ! decodebin ! x264enc ! rtph264pay ! udpsink port=7001
```

To receive:

```
gst-launch-1.0 \
    udpsrc port=7001 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! \
    rtph264depay ! decodebin ! videoconvert ! autovideosink
```

### Video via UDP, as MPEG-2

To send a video test source:

```
gst-launch-1.0 videotestsrc ! x264enc ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=7001
```

To receive:

```
gst-launch-1.0 udpsrc port=7001 ! decodebin ! autovideosink
```

### Both video and audio

To send both a video and audio test source (mixed together):

```
gst-launch-1.0 \
    videotestsrc ! x264enc ! muxer. \
    audiotestsrc ! avenc_ac3 ! muxer. \
    mpegtsmux name=muxer ! rtpmp2tpay ! udpsink host=127.0.0.1 port=7001
```

And to receive both video and audio together:

```
gst-launch-1.0 \
    udpsrc port=7001 caps="application/x-rtp" ! \
    rtpmp2tdepay ! decodebin name=decoder ! autoaudiosink  decoder. ! autovideosink
```

### How to receive with VLC

To receive a UDP stream, an `sdp` file is required. An example can be found at https://gist.github.com/nebgnahz/26a60cd28f671a8b7f522e80e75a9aa5

## TCP

### Audio via TCP

To send a test stream:

```
gst-launch-1.0 \
    audiotestsrc ! \
    avenc_ac3 ! mpegtsmux ! \
    tcpserversink port=7001 host=0.0.0.0
```

To send a file:

```
# Make sure $SRC is set to an audio file (e.g. an MP3 file)
gst-launch-1.0 \
    filesrc location=$AUDIO_SRC ! \
    mpegaudioparse ! \
    tcpserversink port=7001 host=0.0.0.0
```

And to receive:

```
gst-launch-1.0 tcpclientsrc port=7001 host=0.0.0.0 ! decodebin ! autoaudiosink
```

### Video via TCP

Test video stream:

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! x264enc ! mpegtsmux ! queue ! \
    tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

MP4 file (video only):

```
gst-launch-1.0 \
    filesrc location=$SRC ! decodebin ! x264enc ! mpegtsmux ! queue ! \
    tcpserversink host=127.0.0.1 port=7001 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

To receive, either use VLC (`tcp://localhost:7001`) or this command:

```
gst-launch-1.0 \
    tcpclientsrc host=127.0.0.1 port=7001 ! \
    decodebin ! videoconvert ! autovideosink sync=false
```

### Stream and receive video via TCP, using Matroska

Should you wish to use the Matroska container rather than MPEG, here are some examples.
(The [Matroska FAQ](https://www.matroska.org/technical/guides/faq/index.html) nicely describes what it is, if you're interested.)

To send a test stream:

```
gst-launch-1.0 \
    videotestsrc is-live=true ! \
    queue ! videoconvert ! x264enc byte-stream=true ! \
    h264parse config-interval=1 ! queue ! matroskamux ! queue leaky=2 ! \
    tcpserversink port=7001 host=0.0.0.0 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

To send a file (video only):

```
# Make sure $SRC is set to an video file (e.g. an MP4 file)
gst-launch-1.0 \
    filesrc location=$SRC ! decodebin ! \
    queue ! videoconvert ! x264enc byte-stream=true ! \
    h264parse config-interval=1 ! queue ! matroskamux ! queue leaky=2 ! \
    tcpserversink port=7001 host=0.0.0.0 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

To receive:

```
gst-launch-1.0 \
    tcpclientsrc host=0.0.0.0 port=7001 typefind=true do-timestamp=false ! \
    matroskademux ! typefind ! avdec_h264 ! autovideosink
```

I struggle to get VLC to play this (through `tcp://localhost:7001`).

### Audio and Video via TCP

We can of course mux to send audio and video together.

To send both audio and video test:

```
gst-launch-1.0 \
    videotestsrc ! decodebin ! x264enc ! muxer. \
    audiotestsrc ! avenc_ac3 ! muxer. \
    mpegtsmux name=muxer ! \
    tcpserversink port=7001 host=0.0.0.0 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

To send audio and video of an MP4 file:
(Note, quite a few `queue2` elements are required now... there's an explanation of why [here](http://gstreamer-devel.966125.n4.nabble.com/Simple-AV-pipeline-stuck-in-prerolling-state-mp4-h264-aac-td4656970.html).)

```
gst-launch-1.0 \
    filesrc location=$SRC ! \
    qtdemux name=demux \
    demux.video_0 ! queue2 ! decodebin ! x264enc ! queue2 ! muxer. \
    demux.audio_0 ! queue2 ! decodebin ! audioconvert ! audioresample ! avenc_ac3 ! queue2 ! muxer. \
    mpegtsmux name=muxer ! \
    tcpserversink port=7001 host=0.0.0.0 recover-policy=keyframe sync-method=latest-keyframe sync=false
```

To receive, either use VLC (`tcp://localhost:7001`) or this command:

```
gst-launch-1.0 \
    tcpclientsrc host=127.0.0.1 port=7001 ! \
    decodebin name=decoder ! autoaudiosink  decoder. ! autovideosink
```


## Previewing in a web browser using TCP

I've successfully managed to send video to *Firefox*, but not *Chrome* or *Safari*.

You'll need a HTML page with a video element, like [this one](./html_examples/tcp-receive.html)

Then send video like this:

```
gst-launch-1.0 \
        videotestsrc is-live=true ! queue ! \
        videoconvert ! videoscale ! video/x-raw,width=320,height=180 ! \
        clockoverlay shaded-background=true font-desc="Sans 38" ! \
        theoraenc ! oggmux ! tcpserversink host=127.0.0.1 port=9090
```

Video and audio together:

```
gst-launch-1.0 \
        videotestsrc is-live=true ! queue ! \
        videoconvert ! videoscale ! video/x-raw,width=320,height=180 ! \
        clockoverlay shaded-background=true font-desc="Sans 38" ! \
        theoraenc ! queue2 ! mux. \
        audiotestsrc ! audioconvert ! vorbisenc ! mux. \
        oggmux name=mux ! tcpserversink host=127.0.0.1 port=9090
```

Play a source rather than test:

```
gst-launch-1.0 \
    filesrc location=$SRC ! \
    qtdemux name=demux \
    demux.audio_0 ! queue ! decodebin ! vorbisenc ! muxer. \
    demux.video_0 ! queue ! decodebin ! \
    videoconvert ! videoscale ! video/x-raw,width=320,height=180 ! \
    theoraenc ! muxer. \
    oggmux name=muxer ! \
    tcpserversink host=127.0.0.1 port=9090 recover-policy=keyframe sync-method=latest-keyframe
```

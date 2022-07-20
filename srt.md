# SRT (GStreamer command-line cheat sheet)

SRT has a client-server relationship. One side must be the server, the other the client.
The server can either be the side that is sending the audio/video (pushing) or the side that is
receiving (pulling). The server must have started exist before the client.

NOTE: THIS IS FOR GSTREAMER 1.14; IT HAS CHANGED IN 1.16.

## Server sending the AV

Create a sender server like this:

```
gst-launch-1.0 videotestsrc ! video/x-raw, height=360, width=640 ! videoconvert ! x264enc tune=zerolatency ! video/x-h264, profile=high ! mpegtsmux ! srtserversink uri=srt://127.0.0.1:8888/
```

And create a receiver client like this:

```
gst-launch-1.0 -v srtclientsrc uri="srt://127.0.0.1:8888" ! decodebin ! autovideosink
```

## Server receiving the AV

To have the server receiving, rather than sending, swap 'srtclientsrc' for 'srcserversrc'.
Likewise, to have the client sending rather than receiving, swap 'srtserversink' for 'srtclientsink'.

Create a receiver server like this:

```
gst-launch-1.0 -v srtserversrc uri="srt://127.0.0.1:8888" ! decodebin ! autovideosink
```

And a sender client like this:

```
gst-launch-1.0 videotestsrc ! video/x-raw, height=360, width=640 ! videoconvert ! x264enc tune=zerolatency ! video/x-h264, profile=high ! mpegtsmux ! srtclientsink uri="srt://127.0.0.1:8888/"
```
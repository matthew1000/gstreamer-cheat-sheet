# SRT (GStreamer command-line cheat sheet)

SRT is a means of sending AV between to servers.
SRT has a client-server relationship. One side must be the server, the other the client.
The server can either be the side that is sending the audio/video (pushing) or the side that is
receiving (pulling). The server must have started exist before the client.

## Pre-requisites

If on MacOS, ensure the SRT library is installed:

```
brew install srt
```

Then at the time of writing, the default Homebrew build does not include SRT, so build from scratch:

```
brew install --build-from-source gst-plugins-bad
```

## Client receiving from server

The most common usage is that the server has the video, and a client reads from it.

To create a sender server, use `srtsink` (or alternatively, `srtserversink`):

```
gst-launch-1.0 -v videotestsrc ! video/x-raw, height=360, width=640 ! videoconvert ! x264enc tune=zerolatency ! video/x-h264, profile=high ! mpegtsmux ! srtsink uri=srt://:8888
```

And then recieve with `srtsrc`  (or alternatively, `srtclientsrc`):

```
gst-launch-1.0 -v srtsrc uri="srt://127.0.0.1:8888" ! decodebin ! autovideosink
```

Don't forget, the amazing `playbin` can show anything - including SRT streams. This is useful for debugging:

```
gst-launch-1.0 playbin uri=srt://127.0.0.1:8888
```

By default, `srtsink` will wait for a clilent   connection before allowing the stream to start. If you'd prefer this not to happen, set `wait-for-connection=false`:

```
gst-launch-1.0 -v videotestsrc ! video/x-raw, height=360, width=640 ! \
  videoconvert ! clockoverlay font-desc="Sans, 48"  ! x264enc tune=zerolatency ! \
  video/x-h264, profile=high ! mpegtsmux ! srtsink uri=srt://:8888 wait-for-connection=false
```

## Client sending to server

The alternative way round is to have the producer sending the AV to the receiving server.

To have the server receiving, rather than sending, swap 'srtclientsrc' for 'srcserversrc'.
Likewise, to have the client sending rather than receiving, swap 'srtserversink' for 'srtclientsink'.

Create a receiver server like this:

```
gst-launch-1.0 -v srtserversrc uri="srt://127.0.0.1:8889" ! decodebin ! autovideosink
```

And a sender client like this:

```
gst-launch-1.0 -v videotestsrc ! video/x-raw, height=360, width=640 ! \
  videoconvert ! clockoverlay font-desc="Sans, 48"  ! x264enc tune=zerolatency ! \
  video/x-h264, profile=high ! mpegtsmux ! srtclientsink uri=srt://:8889
```


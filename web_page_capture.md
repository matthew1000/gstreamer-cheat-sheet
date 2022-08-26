# Web page capture (WPE)

The [wpesrc](https://gstreamer.freedesktop.org/documentation/wpe/wpesrc.html?gi-language=python) plugin can take a web page, and offer it as a GStreamer source. This allows you to:

* Show web pages on screen, and
* Use web pages as a means of doing graphics.

The `wpesrc` plugin isn't frequently used. To see if you have it installed:

```
gst-inspect-1.0  | grep wpe
```

## Installing

MacOS: The `wpesrc` plugin isn't part of the Homebrew build, unortunately.

Ubuntu: `wpesrc` has a separate package called `gstreamer1.0-wpe`. So to install:

```
sudo apt-get install gstreamer1.0-wpe
```

## Using

TODO

### Streaming to SRT

```
LIBGL_ALWAYS_SOFTWARE=true gst-launch-1.0 -v wpevideosrc location="https://www.bbc.co.uk" ! videoconvert ! x264enc tune=zerolatency ! \
  video/x-h264, profile=high ! mpegtsmux ! srtsink uri=srt://:8889 wait-for-connection=false
```

### Without GPU

Setting `LIBGL_ALWAYS_SOFTWARE=true` allows the `wpserc` element to work without GPU. This can lead to issues if the format is not set to `BGRA`. An example, sending a web page as a live stream to an RTMP server:

```
LIBGL_ALWAYS_SOFTWARE=true gst-launch-1.0 \
    wpevideosrc location="https://en.wikipedia.org/wiki/Main_Page"     \
    ! videoconvert ! videoscale ! videorate \
    ! "video/x-raw, format=BGRA, width=854, height=480, framerate=30/1"  \
    ! videoconvert ! queue ! x264enc speed-preset=1 ! flvmux name=muxer \
    ! rtmpsink location="$RTMP_DEST live=1"
```

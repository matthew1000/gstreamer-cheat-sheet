# Capturing images (GStreamer command-line cheat sheet)

### Capture an image as PNG

The `pngenc` element can create a single PNG:

```
gst-launch-1.0 videotestsrc ! pngenc ! filesink location=foo.png
```

### Capture an image as JPEG

The `jpegenc` element can create a single JPEG:

```
gst-launch-1.0 videotestsrc ! jpegenc ! filesink location=foo.jpg
```

### Capturing images every X seconds

This example captures one frame every 3 seconds, and places it in files with the format `img00001.jpg`.
It also displays the video (as the `tee` command sends the video to both `multifilesink` and `autovideosink`).
To change the frequency, change the `framerate=1/3`.
e.g. `framerate=2/1` would capture a frame twice a second.

```
gst-launch-1.0 videotestsrc ! \
    videoscale ! videoconvert ! video/x-raw,width=640,height=480 ! \
    queue ! decodebin ! tee name=t ! queue ! videoconvert ! videoscale ! \
    videorate ! video/x-raw,width=640,height=480,framerate=1/3  ! \
    jpegenc ! multifilesink location=img%05d.jpg t. ! queue ! autovideosink
```

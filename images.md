# Images (GStreamer command-line cheat sheet)

Images can be added to video.
In addition, video can be converted into images.
This page looks at both types.

## Including images in video

Gstreamer can show images on video using the `imagefreeze` element.


### Create a video from an image

![Example imagefreeze single image](images/imagefreeze_single.png "Example imagefreeze single image")


```
export PIC="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/263px-Wikipedia-logo-v2.svg.png"

gst-launch-1.0 \
    uridecodebin uri=$PIC ! \
    imagefreeze ! \
    autovideosink
```

### Create a video from multiple images

Here's the same image four times, done with the help of `compsitor` (a mixer):

```
gst-launch-1.0 \
    compositor name=m sink_1::xpos=263 sink_2::ypos=240 sink_3::xpos=263 sink_3::ypos=240 ! autovideosink \
    uridecodebin uri=$PIC ! videoscale ! video/x-raw, width=263, height=240 ! imagefreeze ! m. \
    uridecodebin uri=$PIC ! videoscale ! video/x-raw, width=263, height=240 ! imagefreeze ! m. \
    uridecodebin uri=$PIC ! videoscale ! video/x-raw, width=263, height=240 ! imagefreeze ! m. \
    uridecodebin uri=$PIC ! videoscale ! video/x-raw, width=263, height=240 ! imagefreeze ! m.
```

## Capturing video output as images

### Capture an image as PNG

The `pngenc` element can create a single PNG:

```
gst-launch-1.0 videotestsrc ! pngenc ! filesink location=foo.png
```

### Capture an image as JPEG

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
gst-launch-1.0 -v videotestsrc is-live=true ! clockoverlay font-desc=\"Sans, 48\" ! videoconvert ! videorate ! video/x-raw,framerate=1/3 ! jpegenc ! multifilesink location=file-%02d.jpg
```

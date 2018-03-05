# Images (GStreamer command-line cheat sheet)

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


# Basics (GStreamer command-line cheat sheet)

## Playing content

For these,set `SRC` to be e.g. an mp4 file., e.g.

```
export SRC=/home/me/videos/test.mp4
```

### Play a video (with audio)

```
gst-launch-1.0 -v playbin uri=file://$SRC
```

or, if you'd rather have more control of the pipeline:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    autoaudiosink \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! videoscale ! autovideosink
```

### Play a video (no audio)

```
gst-launch-1.0 -v uridecodebin uri="file://$SRC" ! autovideosink
```

which could also have been done as:

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! autovideosink
```

### Play just the audio from a video

```
gst-launch-1.0 -v uridecodebin uri="file://$SRC" ! autoaudiosink
```

### Visualise the audio:

```
gst-launch-1.0 filesrc location=$SRC ! qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! wavescope ! autovideosink
```

(or replace `‘wavescope` with `spectrascope` or `synaescope` or `spacescope`)

Or even better visualisation:

```
gst-launch-1.0 filesrc location=$SRC ! decodebin ! tee name=t ! queue ! audioconvert ! wavescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! videomixer name=m background=black ! videoconvert ! vertigotv ! autovideosink t. ! queue ! audioconvert ! spacescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! m. t. ! queue ! autoaudiosink
```

### Add filters

Go slightly mad:

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! videoconvert ! vertigotv ! autovideosink
```

Try also ‘rippletv’, ‘streaktv’, ‘radioactv’, ‘optv’, ‘quarktv’, ‘revtv’, ‘shagadelictv’, ‘warptv’ (I like), ‘dicetv’, ‘agingtv’ (great), ‘edgetv’ (could be great on real stuff)

### Resize video

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! videoconvert ! videoscale ! video/x-raw,width=100 ! autovideosink
```

### Change framerate

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! videoconvert !  videorate ! video/x-raw,framerate=5/1  ! autovideosink
```

And of course you can resize the video and change the framerate:

```
gst-launch-1.0 -v \
    filesrc location="$SRC” ! \
    decodebin ! videoconvert ! videoscale ! video/x-raw,width=100 ! videorate ! video/x-raw,framerate=5/1  ! \
    autovideosink
```

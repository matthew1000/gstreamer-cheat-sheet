# Basics (GStreamer command-line cheat sheet)

## Playing content

These examples assume that bash variable `SRC` to be set to a video file (e.g. an mp4 file). You can do this by, e.g.

```
export SRC=/home/me/videos/test.mp4
```

### Play a video (with audio)

The magical element `playbin` can play anything:

```
gst-launch-1.0 playbin uri=file://$SRC
```

This works with video, audio, RTMP streams, and so much more.

The 'bin' in 'playbin' means that under-the-hood, it's a collection of elements. We could split it down into the individual components:

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

### Play just the audio from a video

```
gst-launch-1.0 -v uridecodebin uri="file://$SRC" ! autoaudiosink
```

### Visualise the audio:

```
gst-launch-1.0 filesrc location=$SRC ! qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! wavescope ! autovideosink
```

(or replace `‘wavescope` with `spectrascope` or `synaescope` or `spacescope`)

Or even better visualisation:

```
gst-launch-1.0 filesrc location=$SRC ! decodebin ! tee name=t ! queue ! audioconvert ! wavescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! videomixer name=m background=black ! videoconvert ! vertigotv ! autovideosink t. ! queue ! audioconvert ! spacescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! m. t. ! queue ! autoaudiosink
```

### Add filters

Here's the 'vertigo' filter:

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! videoconvert ! vertigotv ! autovideosink
```

Try also ‘rippletv’, ‘streaktv’, ‘radioactv’, ‘optv’, ‘quarktv’, ‘revtv’, ‘shagadelictv’, ‘warptv’ (I like), ‘dicetv’, ‘agingtv’ (great), ‘edgetv’ (could be great on real stuff)

### Add a clock

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! clockoverlay font-desc="Sans, 48" ! videoconvert ! autovideosink
```

### Resize video

```
gst-launch-1.0 -v filesrc location="$SRC" ! decodebin ! videoconvert ! videoscale ! video/x-raw,width=100 ! autovideosink
```

### Change framerate

Changing framerate is quiet common, as the world does not have a consistent standard. Facebook Live wants 30fps, for example. 

Change framerate:

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

Here's a more complete example, that keeps the audio, and changes the size and framerate:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    autoaudiosink \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! videoscale ! videorate ! \
    'video/x-raw, format=(string)I420,  width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    autovideosink
```

### Play an MP3 audio file

Set the environment variable `$AUDIO_SRC` to be the location of the MP3 file. Then:

```
# All three of these do the same thing:
gst-launch-1.0 playbin uri=file://$AUDIO_SRC
gst-launch-1.0 -v uridecodebin uri="file://$AUDIO_SRC" ! autoaudiosink
gst-launch-1.0 -v filesrc location=$AUDIO_SRC ! mpegaudioparse ! decodebin ! autoaudiosink
```

### Play files back to back

See (https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-with-gstreamer/)[https://coaxion.net/blog/2014/08/concatenate-multiple-streams-gaplessly-with-gstreamer/]


### Jumping to a certain point in a video/audio (seek/rewind/restart)

As far as I know, this isn't possible on the command-line. But it is possible as code. Here is a simple Python example:

[/python_examples/seeking.py](/python_examples/seeking.py)

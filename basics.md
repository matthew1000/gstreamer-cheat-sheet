# Basics (GStreamer command-line cheat sheet)

## Playing content

### Play a video (with audio)

```
gst-launch-1.0 -v playbin uri=file:///Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4
```

or another way

```
gst-launch-1.0 filesrc location=/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4 ! qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! autoaudiosink   demux.video_0 ! queue ! decodebin ! videoconvert ! videoscale ! autovideosink
```

# Play a video (no audio)

```
gst-launch-1.0 -v uridecodebin uri="file:///Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! autovideosink
```

which could also have been done as:

```
gst-launch-1.0 -v filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! decodebin ! autovideosink
```

To play a video (just audio, no video):

```
gst-launch-1.0 -v uridecodebin uri="file:///Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! autoaudiosink
```

Audio visualisation:

```
gst-launch-1.0 filesrc location=/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4 ! qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! wavescope ! autovideosink
```

(or replace ‘wavescope’ with ‘spectrascope’ or ‘synaescope’ or ‘spacescope’)

Or even better visualisation:

```
gst-launch-1.0 filesrc location=/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4 ! decodebin ! tee name=t ! queue ! audioconvert ! wavescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! videomixer name=m background=black ! videoconvert ! vertigotv ! autovideosink t. ! queue ! audioconvert ! spacescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! m. t. ! queue ! autoaudiosink
```

Go slightly mad:


```
gst-launch-1.0 -v filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! decodebin ! videoconvert ! vertigotv ! autovideosink
```

Try also ‘rippletv’, ‘streaktv’, ‘radioactv’, ‘optv’, ‘quarktv’, ‘revtv’, ‘shagadelictv’, ‘warptv’ (I like), ‘dicetv’, ‘agingtv’ (great), ‘edgetv’ (could be great on real stuff)

## Resize video

```
gst-launch-1.0 -v filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! decodebin ! videoconvert ! videoscale ! video/x-raw,width=100 ! autovideosink
```

Change framerate

```
gst-launch-1.0 -v filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! decodebin ! videoconvert !  videorate ! video/x-raw,framerate=5/1  ! autovideosink
```

And of course you can resize the video and change the framerate:

```
gst-launch-1.0 -v \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4” ! \
    decodebin ! videoconvert ! videoscale ! video/x-raw,width=100 ! videorate ! video/x-raw,framerate=5/1  ! \
    autovideosink
```

## Picture in picture

```
gst-launch-1.0   \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20161017-224500-match-of-the-day-2-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    videomixer name=mix sink_0::alpha=1 sink_1::alpha=1 !   \
    videoconvert ! autovideosink \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

Put a box around the in-picture using ‘videobox’ e.g.

```
gst-launch-1.0   \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20161017-224500-match-of-the-day-2-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    videomixer name=mix sink_0::alpha=1 sink_1::alpha=1 !   \
    videoconvert ! autovideosink \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    videobox border-alpha=0 top=-10 bottom=-10 right=-10 left=-10 ! \
    mix.
```

Choose where the in-picture goes with the ‘xpos’ and ‘ypos’ attributes of videomixer, e.g.

```
gst-launch-1.0   \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20161017-224500-match-of-the-day-2-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=640,height=360 ! \
    videomixer name=mix sink_0::alpha=1 sink_1::alpha=1 sink_1::xpos=50 sink_1::ypos=50 !   \
    videoconvert ! autovideosink \
    filesrc location="/Users/clarkm22/workspace/silver/assets/20160920-184500-danger-mouse-h264lg.mp4" ! \
    decodebin ! videoconvert ! \
    videoscale ! video/x-raw,width=320,height=180! \
    mix.
```

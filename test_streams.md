# Test streams (GStreamer command-line cheat sheet)

Display a test pattern:

```
gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink
```

Listen to a test audio (beep):

```
gst-launch-1.0 audiotestsrc ! audioconvert ! autoaudiosink
```

Combine both the test pattern and test audio:

```
gst-launch-1.0 audiotestsrc ! autoaudiosink videotestsrc ! autovideosink
```

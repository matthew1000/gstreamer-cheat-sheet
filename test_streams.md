# Test streams (GStreamer command-line cheat sheet)

### Display a test pattern

```
gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink
```

This should display the test pattern in a window, that looks a 
bit like this:

![Test pattern window](images/test-pattern.png "Test pattern window")

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

There are multiple test patterns available, such as

| Pattern        | Example           |
| ------------- |:-------------:|
| `videotestsrc pattern=snow`  | ![](images/test_snow.png) |
| `videotestsrc pattern=red` (and blue and green) | !(images/test_red.png) |
| `videotestsrc pattern=red` (and blue and green) | !(images/test_red.png) |
| `videotestsrc pattern=pinwheel` | !(images/test_pinwheel.png) |
| `videotestsrc pattern=smpte100` (color test bars) | !(images/test_smpte100.png) |
| `videotestsrc pattern=colors` | !(images/test_colors.png) |

For the full list of patterns, see https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-videotestsrc.html

### Listen to a test audio (beep)

```
gst-launch-1.0 audiotestsrc ! audioconvert ! autoaudiosink
```

Combine both the test pattern and test audio:

```
gst-launch-1.0 audiotestsrc ! autoaudiosink videotestsrc ! autovideosink
```

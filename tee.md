# Multiple outputs (tee)

The `tee` command allows audio & video streams to be sent to more than one place.

Here's a simple example that sends shows video test source twice (using `autovideosink`)

```
# The two windows may overlay on top of each other
gst-launch-1.0 \
    videotestsrc ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink \
    t. ! queue ! videoconvert ! autovideosink
```

Here's an example that sends video to both `autovideosink` and a TCP server (`tcpserversink`).
Note how `async=false` is required on both sinks.

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink async=false \
    t. ! queue ! x264enc ! mpegtsmux ! tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe async=false
```

However, as discussed [here](http://gstreamer-devel.966125.n4.nabble.com/tee-won-t-go-in-playing-state-td4680128.html), `async=false` can cause issues. Adding `tune=zerolatency` to the `x264enc` also resolves the issue.

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink \
    t. ! queue ! x264enc tune=zerolatency ! mpegtsmux ! tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe
```

You can also use `tee` in order to do multiple things with inputs. This example combines two audio visualisations:

```
gst-launch-1.0 filesrc location=$SRC ! decodebin ! tee name=t ! \
    queue ! audioconvert ! wavescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! \
    videomixer name=m background=black ! videoconvert ! vertigotv ! autovideosink \
    t. ! queue ! audioconvert ! spacescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! m. \
    t. ! queue ! autoaudiosink
```

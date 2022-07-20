# Multiple outputs (tee)

This page describes the `tee` element, which allows audio & video streams to be sent to more than one place.

## Tee to two local video outputs

Here's a simple example that sends shows video test source twice (using `autovideosink`)

```
# The two windows may overlay on top of each other
gst-launch-1.0 \
    videotestsrc ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink \
    t. ! queue ! videoconvert ! autovideosink
```

## Tee to two different video outputs

Here's an example that sends video to both `autovideosink` and a TCP server (`tcpserversink`).
Note how `async=false` is required on both sinks, because the encoding step on the TCP branch takes longer, and so the timing will be different.

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink async=false \
    t. ! queue ! x264enc ! mpegtsmux ! tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe async=false
```

However, as discussed [here](http://gstreamer-devel.966125.n4.nabble.com/tee-won-t-go-in-playing-state-td4680128.html), `async=false` can cause issues. Adding `tune=zerolatency` to the `x264enc` also resolves the issue, by telling the encoding step not to add a delay, and thus making its branch as quick as the `autovideosink` one.

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! tee name=t \
    t. ! queue ! videoconvert ! autovideosink \
    t. ! queue ! x264enc tune=zerolatency ! mpegtsmux ! tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe
```

Or, if you'd rather not reduce the quality of x264 encoding, you can increase the queue size:

```
gst-launch-1.0 videotestsrc ! \
    decodebin ! tee name=t \
    t. ! queue max-size-time=3000000000 ! videoconvert ! autovideosink \
    t. ! queue ! x264enc ! mpegtsmux ! tcpserversink port=7001 host=127.0.0.1 recover-policy=keyframe sync-method=latest-keyframe
```

## Tee on inputs

You can also use `tee` in order to do multiple things with inputs. This example combines two audio visualisations:

```
gst-launch-1.0 filesrc location=$SRC ! decodebin ! tee name=t ! \
    queue ! audioconvert ! wavescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! \
    videomixer name=m background=black ! videoconvert ! vertigotv ! autovideosink \
    t. ! queue ! audioconvert ! spacescope style=color-lines shade-amount=0x00080402 ! alpha alpha=0.5 ! m. \
    t. ! queue ! autoaudiosink
```

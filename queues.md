# Queues

A `queue` can appear almost anywhere in a GStreamer pipeline. Like most elements, it has an input (sink) and output (src). It has two uses:

* As a thread boundary - i.e. The elements after a queue will run in a different thread to those before it
* As a buffer, for when different parts of the pipeline may move at different speeds.

Queues can generally be added anywhere in a pipeline. For example, a test stream:

```
gst-launch-1.0 videotestsrc ! autovideosink
```

This works just as well with a queue in the middle:

```
gst-launch-1.0 videotestsrc ! queue ! autovideosink
```

(If you [count the number of threads on the process](https://stackoverflow.com/questions/28047653/osx-how-can-i-see-the-tid-of-all-threads-from-my-process), you will see that this second example, with a queue, has one more.)

Queues add latency, so the general advice is not to add them unless you need them.


## Queue2

Confusingly, `queue2` is not a replacement for `queue`. It's not obvious when to use one or the other.

Most of the time, `queue2` appears to replace `queue` without issue. For example:

```
# Same as above, but with queue2 instead of queue:
gst-launch-1.0 videotestsrc ! queue2 ! autovideosink
```

According to the [GStreamer tutorial](https://gstreamer.freedesktop.org/documentation/tutorials/basic/handy-elements.html), _as a rule of thumb, prefer queue2 over queue whenever network buffering is a concern to you._


## Multiqueue

The `multiqueue` can provide multiple queues. If, for example, you have a video and an audio queue, it can handle them both, and do a better job of allowing one to grow if the other is delayed.

As a simple (pointless) example, it can be used to replace `queue` or `queue2`

```
# Same as above, but with multiqueue instead of queue/queue2:
gst-launch-1.0 videotestsrc ! multiqueue ! autovideosink
```

A more realistic example is where there are two queues, such as here, for video and audio:

```
gst-launch-1.0 \
    videotestsrc ! queue ! autovideosink \
    audiotestsrc ! queue ! autoaudiosink
```

The two queues could be replaced with one multiqueue. Naming it (in this case, `q`) allows it to be referenced later.

```
gst-launch-1.0 \
    videotestsrc ! multiqueue name=q ! autovideosink \
    audiotestsrc ! q. q. ! autoaudiosink
```

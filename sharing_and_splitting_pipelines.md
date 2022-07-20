# Sharing and splitting pipelines (GStreamer command-line cheat sheet)

There are various reasons why you might want your video (or audio) to leave the pipeline, such as:

* To enter a separate application, such as [Snowmix](http://snowmix.sourceforge.net/)
* To use multiple processes (perhaps for security reasons)
* To split into multiple pipelines, so that a failure in one part does not alter another
* To split into multiple pipelines, so that you can 'seek' (jump to a certain point) in one without affecting another

To quote from http://blog.nirbheek.in/2018/02/decoupling-gstreamer-pipelines.html:

> In some applications, you want even greater decoupling of parts of your pipeline.
> For instance, if you're reading data from the network, you don't want a network error
> to bring down our entire pipeline, or if you're working with a hotpluggable device,
> device removal should be recoverable without needing to restart the pipeline.

There are many elements that can achieve this, each with their own pros and cons.

## Summary of methods to share and split pipelines

_As with the rest of this site, this is a rough guide, and is probably not complete or accurate!_

| Name | Description | Points to note | Further reading |
| ---- | ----------- | -------------- | --------------- |
| *shmsink and shmsrc* | Allows video to be read/written from shared memory | Used to send/receive from Snowmix | See below |
| *appsrc/appsink* | Allows video data to leave/enter the pipeline from your own application | n/a | [Docs](https://thiblahute.github.io/GStreamer-doc/app-1.0/index.html?gi-language=c) |
| *fdsrc/fdsink* | Allows communication via a file descriptor | n/a | [Docs](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-fdsrc.html) |
| *interpipe* | Allows simple communication between two or more independent pipelines. Very powerful. | * Not part of GStreamer (though it is open-source... I'm not sure why it's not been included) | [Great RidgeRun docs](https://developer.ridgerun.com/wiki/index.php?title=GstInterpipe) [Presentation](https://gstreamer.freedesktop.org/data/events/gstreamer-conference/2015/Melissa%20Montero%20-%20GST%20Daemon%20and%20Interpipes:%20A%20simpler%20way%20to%20get%20your%20applications%20done%20.pdf) |
| *inter* (intervideosink, etc) | Send/receive AV between two pipelines in the same process | Only support raw audio or video, and drop events and queries at the boundary (source: [Nirbheek's blog](http://blog.nirbheek.in/2018/02/decoupling-gstreamer-pipelines.html)) | See below |
| *ipcpipeline* | Allows communication between pipelines *in different processes*. | Arrived with GStreamer 1.14 (Spring 2018) |  [Collabora post](https://www.collabora.com/news-and-blog/blog/2017/11/17/ipcpipeline-splitting-a-gstreamer-pipeline-into-multiple-processes/) |
| *gstproxy (proxysink and proxysrc)* | Send/receive AV between two pipelines in the same process. | Arrived with GStreamer 1.14 (Spring 2018) | See below |


## Sharing via memory - shmsink and shmsrc

The [`shmsink`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad/html/gst-plugins-bad-plugins-shmsink.html) element allows you to write video into shared memory, from which another gstreamer application can read it with [`shmsrc`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad/html/gst-plugins-bad-plugins-shmsrc.html).


### Putting a stream into memory

Put a test video source into memory:

```
gst-launch-1.0 -v videotestsrc ! \
    'video/x-raw, format=(string)I420,  width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    queue !  identity ! \
    shmsink wait-for-connection=1 socket-path=/tmp/tmpsock  shm-size=20000000 sync=true  
```

Another example, this time from a file rather than test source, and keeping the audio local:

```
gst-launch-1.0 filesrc location=$SRC ! \
    qtdemux name=demux  demux.audio_0 ! queue ! decodebin ! audioconvert ! audioresample ! \
    autoaudiosink \
    demux.video_0 ! queue ! \
    decodebin ! videoconvert ! videoscale ! videorate ! \
    'video/x-raw, format=(string)I420,  width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    queue !  identity ! \
    shmsink wait-for-connection=0 socket-path=/tmp/tmpsock  shm-size=20000000 sync=true  
```

### Reading a stream from memory

This will display the video of a stream locally:

```
gst-launch-1.0 shmsrc socket-path=/tmp/tmpsock ! \
    'video/x-raw, format=(string)I420, width=(int)320, height=(int)240, framerate=(fraction)30/1' ! \
    autovideosink
````

## gstproxy (proxysink and proxysrc)

I've used `proxysink` and `proxysrc` to split larger pipelines into smaller ones. That way, if a part fails, the rest can continue.

Unlike _inter_ below, _proxy_ will keep timing in sync. This is great if it's what you want... but if you want pipelines to have their own timing, it might not be right for your needs..


### gstproxy documentation

* Introduced by the blog mentioned above (http://blog.nirbheek.in/2018/02/decoupling-gstreamer-pipelines.html)
* Example code on proxysrc here: https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad-plugins/html/gst-plugins-bad-plugins-proxysrc.html
* Equivalent proxysink: https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad-plugins/html/gst-plugins-bad-plugins-proxysink.html


### gstproxy examples

It's not possible to use them via the command-line, because you connect them by having the receiver (`proxysrc`) reference the sender (`proxysink`).

A very simple example would be:

```
1st pipeline:   audiotestsrc is-live=1 ! proxysink
2nd pipeline:   proxysrc ! autoaudiosink
```

This would achieve the same as `audiotestsrc | autoaudiosink`, but in two pipelines.

An Python example of this can be found at [/python_examples/gstproxy_01_audiotestsrc.py](/python_examples/gstproxy_01_audiotestsrc.py).

A slightly more interesting example can be found at

[/python_examples/gstproxy_02_playbin.py](/python_examples/gstproxy_02_playbin.py). This plays a video file (e.g. mp4). It shows:

* that `proxysink` can work with [`playbin`](https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-playbin.html)
* separate proxies for audio and video
* that when the video ends, the other pipelines continue.


## inter (intervideosink/intervideosrc and their audio & subtitle counterparts)

The 'inter' versions of 'proxy' are dumber. They don't attempt to sync timings. But this can be useful if you want pipelines to be more independent. (Pros and cons on this discussed [here](http://gstreamer-devel.966125.n4.nabble.com/How-to-connect-intervideosink-and-intervideosrc-for-IPC-pipelines-td4684567.html).)

* `interaudiosink` and `intervideosink` allow a pipeline to send audio/video to another pipeline.
* `interaudiosrc` and `intervideosrc` are the corresponding elements for receiving the audio/video.
* subtitle versions are available too.

They are documented here: https://thiblahute.github.io/GStreamer-doc/inter-1.0/index.html?gi-language=c<

An example can't be done via the command-line, but here is a simple example using Python:

[/python_examples/gstinter_01_audiotestsrc.py](/python_examples/gstinter_01_audiotestsrc.py)

Here's a more complex example, showing how two files can have separate seeking by being in different pipelines:

[/python_examples/gstinter_02_separate_seeking.py](/python_examples/gstinter_02_separate_seeking.py)

 gst-launch-1.0 -e videotestsrc ! video/x-raw-yuv, framerate=25/1, width=640, height=360 ! x264enc ! \
               mpegtsmux ! filesink location=test.ts

gst-launch-1.0 -e videotestsrc !\
    x264enc !\
    mpegtsmux !\
    filesink location=test.ts

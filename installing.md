# Installing (GStreamer command-line cheat sheet)

## Packages

Installing GStreamer is not enough. GStreamer is built on a large number of plugins, which are split into four packages:

* *Base*: Reliable, commonly used, high-quality plug-ins
* *Good*: Additional plug-ins that are also reliable and high-quality
* *Bad*: Plugins that are potentially unreliable
* *Ugly*: Plugins that may bring concerns, often around licensing

(Full definition of these packages [in this readme](https://gitlab.freedesktop.org/gstreamer/gstreamer/-/blob/main/subprojects/gst-plugins-bad/README.md).)

You can choose which you install - you'll almost certainly need base, and potentially the others.

You can see which package a plugin belongs in the [Plugins API reference](https://gstreamer.freedesktop.org/documentation/plugins_doc.html?gi-language=c).

You can get a list of all installed plugins with:

```
gst-inspect-1.0
```

## Installing on MacOS

The easiest way to install on MacOS is using Homebrew. There is a [GStreamer](https://formulae.brew.sh/formula/gstreamer) package, and additional packages for the base/good/bad/ugly plugins.

Example:

```
brew install gstreamer gst-plugins-base gst-plugins-good
```

There are many dependencies so this can take time to run!

You can also compile and install yourself - see (https://gstreamer.freedesktop.org/documentation/installing/on-mac-osx.html).


## Installing on Ubuntu Linux

The GStreamer APT packages are excellent. 

For a good install command, see (https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c).



## Installing on other platfoms

See (https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c)


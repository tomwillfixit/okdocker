# How to train your Docker (using voice recognition)

This is a work in progress but just wanted to get this code pushed incase someone else finds it useful.

Before you start there is one file that is greater than 100mb and I couldn't push it to github :

http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Language%20Model/cmusphinx-5.0-en-us.lm.gz/download

If you want to build the image locally you will need to download that file and gunzip it.  You should end up with this extracted file : cmusphinx-5.0-en-us.lm

The Build and Usage commands are in the Dockerfile. 

The blog post associated with this can be found here :

http://thshaw.blogspot.com/2016/01/how-to-train-your-docker-using-voice.html

The docker image can be pulled from : thshaw/okdocker

I'll be updating this code regularly as it is only partially working.  More details in the blog.

Here is what currently works :

```
Recording 3 second clip
Playback clip
Decoding clip to text
```

This was built and tested on Ubuntu 15.10 and you may need to tweak the audio on the host to get this to work.

This is still a work in progress and the accuracy is very low.  If you want to train Sphinx to use your own voice then then instructions can be found here : http://cmusphinx.sourceforge.net/wiki/tutorialadapt

The next version of the code will use pocketsphinx_continuous and gstreamer : http://cmusphinx.sourceforge.net/wiki/gstreamer

Rgds,
@tomwillfixit




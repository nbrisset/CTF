# Just open it (Forensics, 15 points)
>I'm almost positive we put a flag in [this](https://mega.nz/#!q8FBHAqD!D2-GX_5pi5rb1cfjNGTV-NDWTahZiJlFfDl5PlUY8z8) file.
Can you find it for me?

We are given a link to an image.

![Find the flag in this image](just-open-it.jpg)

Just in order to be sure, let's use the "file" command. It might be totally something else than expected.

```
root@blinils:~/ABCTF# mv 676F6F645F6A6F625F6275745F746869735F69736E745F7468655F666C6167.jpg just-open-it.jpg
root@blinils:~/ABCTF# file just-open-it.jpg
676F6F645F6A6F625F6275745F746869735F69736E745F7468655F666C6167.jpg: JPEG image data,
JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 1024x768, frames 3
```
 
Well, it's really a JPG file. As for the previous challenge,
[Elemental](https://github.com/nbrisset/CTF/tree/master/abctf-2016/elemental-10),
it seems that we have to dive deeper... in the code.

Either with a text editor (at line 88 with Notepad++), or with a "strings / grep" command, the flag appears!

``` 
root@blinils:~/ABCTF# strings just-open-it.jpg | grep ABCTF
P ABCTF{forensics_1_tooo_easy?}
```

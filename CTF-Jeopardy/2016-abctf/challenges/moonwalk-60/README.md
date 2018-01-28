_[<<< Return to ABCTF 2016 tasks and writeups](/CTF-Jeopardy/2016-abctf)_
# MoonWalk (Forensics, 60 points)

>There is something a little off about [this picture](PurpleThing.png).

>If you could help us we could give you some points! Just find us a flag!

We are given a link to an image.

Just in order to be sure, let's use the "file" command. It might be totally something else than expected.

```console
root@blinils:~/ABCTF# file PurpleThing.png
PurpleThing.png: PNG image data, 3200 x 2953, 8-bit/color RGBA, non-interlaced
```

Then, I am used to launching ExifTool, in order to check the metadata of the picture.

Sometimes, the flag is hidden in metadata fields, such as "Author", "Profile Copyright", "Camera Model"...

```console
root@blinils:~/ABCTF# exiftool PurpleThing.png
ExifTool Version Number        : 10.23
File Name                      : PurpleThing.png
Directory                      : .
File Size                      : 2.2 MB
File Modification Date/Time    : 2016:07:16 08:51:53+02:00
File Access Date/Time          : 2016:08:24 22:36:38+02:00
File Inode Change Date/Time    : 2016:07:16 08:52:26+02:00
File Permissions               : rwxrwx---
File Type                      : PNG
File Type Extension            : png
MIME Type                      : image/png
Image Width                    : 3200
Image Height                   : 2953
Bit Depth                      : 8
Color Type                     : RGB with Alpha
Compression                    : Deflate/Inflate
Filter                         : Adaptive
Interlace                      : Noninterlaced
[...]
Red Tone Reproduction Curve    : (Binary data 2060 bytes, use -b option to extract)
Green Tone Reproduction Curve  : (Binary data 2060 bytes, use -b option to extract)
Blue Tone Reproduction Curve   : (Binary data 2060 bytes, use -b option to extract)
[...]
Warning                        : Truncated PNG IEND chunk
Image Size                     : 3200x2953
Megapixels                     : 9.4
```

This file is quite heavy, it might have hidden data in it,
as for the [Banana Boy challenge](/CTF-Jeopardy/2016-sctf-q1/challenges/banana-boy-20)
from the [sCTF event](/CTF-Jeopardy/2016-sctf-q1).

Let's use [binwalk](http://tools.kali.org/forensics/binwalk) and
[hachoir-subfile](https://pypi.python.org/pypi/hachoir-subfile/0.5.3),
which are tools designed to analyze and extract data contained in a file.

```console
root@blinils:~/ABCTF# hachoir-subfile PurpleThing.png
[+] Start search on 2354256 bytes (2.2 MB)

[+] File at 0: PNG picture: 3200x2953x32 (alpha layer)
[+] File at 765455 size=1588789 (1.5 MB): JPEG picture
 
[+] End of search -- offset=2354256 (2.2 MB)
Total time: 187 ms -- global rate: 12.0 MB/sec
```

Yeah, there is a JPEG picture inside our PNG purple thing, which we have to extract with binwalk.

```console
root@blinils:~/ABCTF# binwalk -e PurpleThing.png
DECIMAL      HEXADECIMAL    DESCRIPTION
--------------------------------------------------------------------------------
0            0x0            PNG image, 3200 x 2953, 8-bit/color RGBA, non-interlaced
85           0x55           Zlib compressed data, best compression
2757         0xAC5          Zlib compressed data, best compression
765455       0xBAE0F        JPEG image data, JFIF standard 1.01
765485       0xBAE2D        TIFF image data, big-endian, offset of first image directory: 8
 
WARNING: Extractor.execute failed to run external extractor 'unstuff '%e'': [Errno 2] No such file or directory: 'unstuff'
1809691      0x1B9D1B       StuffIt Deluxe Segment (data): f
```

Unluckily, the expected JPEG file is not in the extracted data.
But we have a large toolbox, let's use [foremost](https://doc.ubuntu-fr.org/foremost) instead!

```console
root@blinils:~/ABCTF# foremost -v Purple.png
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File
 
Foremost started at Thu Aug 25 08:09:10 2016
Invocation: foremost -v Purple.png
Output directory: /root/ABCTF/output
Configuration file: /etc/foremost.conf
Processing: Purple.png
|------------------------------------------------------------------
File: Purple.png
Start: Thu Aug 25 08:09:10 2016
Length: 2 MB (2354256 bytes)
 
Num    Name (bs=512)          Size    File Offset    Comment
 
0:    00001495.jpg            1 MB          765455
*|
Finish: Thu Aug 25 08:09:10 2016
 
1 FILES EXTRACTED
   
jpg:= 1
------------------------------------------------------------------
 
Foremost finished at Thu Aug 25 08:09:10 2016
```

We eventually find the extracted file in the "output" folder: [/root/ABCTF/output/jpg/00001495.jpg](00001495.jpg).

Solution: ABCTF{PNG_S0_C00l}

Or kind of, there was a little controversy about the letter case... png or PNG? cOOl C00l cOO1...?

# Banana Boy (Forensics, 20 points)
>Carter loves bananas, but I heard a rumor that he's hiding something! [Can you find it?](carter.jpg)

Yeah, I love steganography. Let's see who really is Carter with the "file" command.

```
root@blinils:~/SCTF2016# file carter.jpg

carter.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16,
Exif Standard: [TIFF image data, big-endian, direntries=5, orientation=upper-left, xresolution=74,
yresolution=82, resolutionunit=2], baseline, precision 8, 600x450, frames 3
```

This is a real JPG image. But is there hidden data in it?

Let's use "binwalk", a tool designed to analyze and extract data contained in a file.

```
root@blinils:~/SCTF2016# binwalk carter.jpg

DECIMAL     HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0           0x0             JPEG image data, JFIF standard 1.01
382         0x17E           Copyright string: "Copyright (c) 1998 Hewlett-Packard Company"
3192        0xC78           TIFF image data, big-endian, offset of first image directory: 8
140147      0x22373         JPEG image data, JFIF standard 1.01
140177      0x22391         TIFF image data, big-endian, offset of first image directory: 8
```
 
Wow! There is another JPEG image in the original JPEG!

Let's extract this new file from the offset 140147, with the "dd" command.

```
root@blinils:~/SCTF2016# dd skip=140147 if=./carter.jpg of=./carter1.jpg bs=1

54041+0 records in
54041+0 records out
54041 bytes (54 kB, 53 KiB) copied, 0,124007 s, 436 kB/s

root@blinils:~/SCTF2016# file carter1.jpg

carter1.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, 
segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=1, orientation=upper-left],
baseline, precision 8, 610x337, frames 3
```

Gotcha! Banana! [This file embedded in carter.jpg](carter1.jpg) gives us the flag.

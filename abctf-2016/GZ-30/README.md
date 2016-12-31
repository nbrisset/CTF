_[<<< Return to ABCTF 2016 tasks and writeups](/abctf-2016)_
# GZ

>We shot a flag into [this](https://mega.nz/#%21z4dlBSTb%215A2R5e6O9xYFYLhAcYUL8vRio4MW6dSfOWdEMaYuE80)
file but some things got messed up on the way...

[This file](flag) seems to be a [gzip archive](https://en.wikipedia.org/wiki/Gzip)
which can be restored using [GNU Gzip](http://www.gnu.org/software/gzip/manual/gzip.html).

```console
root@blinils:~/abctf-2016# cat flag
^pWflagstrq�N*��N͋��,(H-����%�
 
root@blinils:~/abctf-2016# file flag
flag: gzip compressed data, was "flag", last modified: Sun Jun 26 17:22:38 2016, from Unix

root@blinils:~/abctf-2016# mv flag flag.gz && gzip -d flag.gz

root@blinils:~/abctf-2016# cat flag
ABCTF{broken_zipper}
```


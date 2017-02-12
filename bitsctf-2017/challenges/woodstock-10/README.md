_[<<< Return to BitsCTF 2017 tasks and writeups](/bitsctf-2017)_
# Woodstock-1 (Forensics, 10 points)

>Someone intercepted a chat between illustris and codelec

This challenge consists in [a pcapng file](ws1_2.pcapng) (a network traffic capture).

The first way to solve the challenge: using strings.

```console
root@blinils:~/bitsctf-2017# strings ws1_2.pcapng | grep BITSCTF
$MyPass BITSCTF{such_s3cure_much_w0w}|
```

The second way to solve the challenge: using Wireshark.

![Wireshark on Woodstock](wireshark-woodstock.png)

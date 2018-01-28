_[<<< Return to GreHack CTF 2016 tasks and writeups](/2016-grehack-ctf)_
# My first reverse (Reverse, 50 points)

> Find the flag!

This was the first out of four reverse challenges: we had to find a flag in [this program](my_first_reverse.exe).

My first reflex as a reverse newbie: let's use "strings", maybe the flag will magically appear.

```console
root@blinils:~/GH16# file reverse.exe
reverse.exe: MS-DOS executable

root@blinils:~/GH16# strings reverse.exe
.text
.imp
Pj2hz
<ru{F
<sutF
<1umF
<nufF
<gu_F
<_uXF
<1uQF
<suJF
<_uCF
<cu<F
<0u5F
<0u.F
<lu'F
<!u F
Password? 
Try again!
Correct!
KERNEL32.dll
GetStdHandle
ReadFile
WriteFile
ExitProcess
```

We are given the end of a sentence: rs1ng_1s_c00l!

It is definitely a program which asks for a password (Password?), and indicates if the password is (Correct!) or not.

Now if we only want the printable characters from the file:

```console
root@blinils:~/GH16# tr -dc '[:print:]' < reverse.exe | sed 's/F<//g'
MZPEL@0~   }.text .imp  Uj @Ej @EjEPjh[@u @jEPj2hz@u @Ez@<GH16{r3v3ru{sut1umnufgu__uX1uQsuJ_uCcu<0u50u.lu'!u }uFjEPjhq@u @jEPjhf@u @j @Password? Try again!Correct!U d o { H  KERNEL32.dllGetStdHandleReadFileWriteFileExitProcess
```

We now have the beginning of the flag: GH16{r3v3r, but also the end of the flag,
truncated with extra characters... which gives GH16{r3v3rs1ng_1s_c00l!} ... Correct!
My teammates solved this challenge in other ways,
by working with [radare2](https://github.com/radare/radare2) or [using an online decompiler](DECOMPILE.md).


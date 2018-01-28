_[<<< Return to IceCTF 2016 tasks and writeups](/CTF-Jeopardy/2016-icectf)_
# IRC I (Misc, 35 points)

>There is someone sharing flags on our IRC server, can you find him and stop him? glitch.is:6667

Sharing flags or giving major hints to other teams is not
well perceived by CTF organizers, and it can lead to an outright ban.

Well it seems that someone shares flags on IRC, so we have
to [log on their IRC server](https://chat.icec.tf/) glitch.is:6667 in order to investigate!

There are quite a few players on it, and three ops (admins) :
finalC, hkr and Glitch, the latter being the creator of the challenge.

If we run a [whois query](https://tools.ietf.org/html/rfc1459#section-4.5.2) on Glitch:

```
Glitch (~Glitch@localhost): Hlynur
Glitch is on the following channels: @#78a99bb_flagshare @#IceCTF @#Glitch
Glitch is connected to irc.glitch.is
```

... we learn that he is also an op on the channel #78a99bb_flagshare. 
Let's [join it](https://tools.ietf.org/html/rfc1459#section-4.2.1) and see what happens.

```
10:10 Blinils (~Blinils@-censored IP-.bc.googleusercontent.com) has joined the channel 
10:10 The topic is:  Want flags? We got 'em! IceCTF{pL3AsE_D0n7_5h4re_fL495_JUsT_doNT}
```

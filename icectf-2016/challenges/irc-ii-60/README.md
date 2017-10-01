_[<<< Return to IceCTF 2016 tasks and writeups](/icectf-2016)_
# IRC II (Misc, 60 points)

>Can you trick our IRC bot into giving you his flag? Talk to IceBot on glitch.is:6667.
>Please only send him private messages, you do this by writing /msg IceBot !command.
>The "help" command has been removed so here is the output from !help.
>Please consider that he may be slow to respond or the command you're trying may not work.

Here it is, the last challenge of the CTF about IRC.
The first write-up is here: [IRC I (Misc)](/icectf-2016/challenges/irc-i-35)

Once again, we have to return to their IRC server, in order to ~~trick~~ politely ask the bot to give us the flag.

The "help" command has been removed because of a known bug,
where too many requests to the bot make it quiet a long time.
Instead, we are given the output from !help. In a split second,
the right command to use is quite obvious: `00:22 <IceBot> FLAG flag`

Using the !flag command in the main channel is unconclusive because IceBot only replies to private messages.

```
20:20 Blinils (~Blinils@-censoredIP-.bc.googleusercontent.com) has joined the channel
20:20 Blinils !flag
20:20 +IceBot I'm sorry, you're not a channel operator
```

Unfortunately, if we send a private message to the bot, it will return an error.

I used https://chat.icec.tf and clicked on "IceBot" in order to send it private messages.

In this way, I can send `!flag` instead of `/msg IceBot !flag`

```
21:21  Blinils  !flag 
21:21  IceBot   KeyError: Identifier('Blinils') 
                (file "/usr/local/lib/python2.7/dist-packages/sopel/module.py", line 321, in guarded)  
```

A quick search of "sopel/module.py" provides us
[a Github repository](https://github.com/sopel-irc/sopel/blob/master/sopel/module.py),
dedicated to Sopel IRC Bot.

According to the code near line 321, the error above means that we don't have sufficient permissions to ask for the flag.

```
314    def require_privilege(level, message=None):
315         """Decorate a function to require at least the given channel permission.
316        
317         `level` can be one of the privilege levels defined in this module. If the
318         user does not have the privilege, `message` will be said if given. If it is
319         a private message, no checking will be done."""
```

Since the organizers won't let each player become an op
on the main channel (even for a few seconds) we have to do it differently.
Two things: 1# when a user creates and joins a channel,
he automatically becomes op and 2# a user
[can invite another user](https://tools.ietf.org/html/rfc1459#section-4.2.7)
to an arbitrary channel.

So the solution is to create a channel, ecome op on it,
then invite IceBot and ~~politely ask it~~ trick it into giving us the flag.

```
[/join #omeca]
23:23    Blinils (~Blinils@-censoredIP-.bc.googleusercontent.com) has joined the channel
23:23    #omeca sets mode +nt
[/invite IceBot #omeca]
23:23    IceBot (~IceBot@-censoredIP-.bc.googleusercontent.com) has joined the channel
23:23    @Blinils !flag
23:23    IceBot IceCTF{H3Re_y0U_9O_M4s7Er_m4kE_5uR3_yOU_K33P_iT_54F3}
```

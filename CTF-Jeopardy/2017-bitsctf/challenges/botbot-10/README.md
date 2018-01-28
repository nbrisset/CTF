_[<<< Return to BitsCTF 2017 tasks and writeups](/2017-bitsctf)_
# BotBot (Web, 10 points)

>Should not ask for the description of a 5 marker. botbot.bitsctf.bits-quark.org

```html
<!DOCTYPE HTML>
<!--
	Nothing to see here. Maybe try looking up seo .txt
-->
<html>
	<head>
		<title>Photon by HTML5 UP</title>
		...
	</head>
```

Looking at the source code of the given website, I saw a clue about
[search engine optimization](https://en.wikipedia.org/wiki/Search_engine_optimization) (SEO).
One of these SEO techniques involves the use of robots.txt, a file which denies search engines access to certain resources. Let's look at it!

```console
root@blinils:~/bitsctf-2017# curl http://botbot.bitsctf.bits-quark.org/robots.txt
Useragent *
Disallow: /fl4g
```

Great! The flag must be in this directory.

```console
root@blinils:~/bitsctf-2017# curl http://botbot.bitsctf.bits-quark.org/fl4g/
BITCTF{take_a_look_at_googles_robots_txt}
```

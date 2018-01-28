_[<<< Return to ABCTF 2016 tasks and writeups](/CTF-Jeopardy/2016-abctf)_
# Elemental (Web Exploitation, 10 points)

>Just put in the password for the flag! [Link](http://yrmyzscnvh.abctf.xyz/web1/)

We are given a link to a website, which only contains a password field and a "submit" button.

![Screenshot from the website yrmyzscnvh.abctf.xyz/web1](elemental.png)

Within the source code of the page, the expected password can be seen as a comment. How dreadful!

```html
<div class="row">
<div class="col l4 push-l4" id="response-wrong">
</div>
</div>

</body>

<!-- 7xfsnj65gsklsjsdkj -->

<script type="text/javascript" src="fade.js"></script>

</html>
```

With the good password 7xfsnj65gsklsjsdkj, we got the solution: ABCTF{insp3ct3d_dat_3l3m3nt}


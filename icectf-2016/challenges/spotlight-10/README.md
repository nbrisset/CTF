_[<<< Return to IceCTF 2016 tasks and writeups](/icectf-2016)_
# Spotlight (Web, 10 points)

>Someone turned out the lights and now we can't find anything.
Send halp! [spotlight](http://spotlight.vuln.icec.tf/)

This challenge consists in a totally dark website (with a black background), in which you can move the cursor, a white circle acting as a "spotlight". After searching around, there was no evidence of the flag, but some encouraging words such as "Almost there!" or "Look closer!".

![Affichage de l'image spotlight.png](spotlight.png)

This is the source code of the challenge:

```html
<!DOCTYPE html>
<html>
    <head>
        <title>IceCTF 2016 - Spotlight</title>
        <link rel="stylesheet" type="text/css" href="spotlight.css">
    </head>
    <body>
        <!-- Hmmm... not here either? -->

        <canvas id="myCanvas" style="background-color:#222;">
            Your browser does not support the HTML5 canvas tag.
        </canvas>
        <script src="spotlight.js"></script>
    </body>
</html>
```

Looking very thoroughly [the source code for the JS](spotlight.js), we finally find the flag, which was hidden in the debug log.

```javascript
53	console.log("DEBUG: IceCTF{5tup1d_d3v5_w1th_th31r_l095}");
54
55	console.log("DEBUG: Loading up helper functions...");
56	console.log("DEBUG:     * getMousePos(canvas, evt)");
57	function getMousePos(canvas, evt) {
58	    var rect = canvas.getBoundingClientRect();
59	    return {
60	        x:  evt.clientX - rect.left,
61	        y:  evt.clientY - rect.top
62	    };
63	}
```

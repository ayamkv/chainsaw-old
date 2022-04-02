# Chainsaw
<img src="https://img.shields.io/badge/deprecated-discontinued-inactive"/>

it's a python program that posts a frame (images) from 
chainsaw man pv in order every 6-7 hours

## Storage

the image files are huge, so i decided to upload them on **dropbox** 
> since they have an easier api to implement , i think

using dropbox api we can download the image and delete the image when we're done
so it will _bypass_ **heroku** storage limit.
 
## Banner
there's another feature which is to change the twitter banner
everytime it posts, it would have a background of the current frame blurred
and the logo of chainsaw man. I'm using PIL for the blurred frame and overlay the logo 
on top.


## Keep On Track

to keep on track/in order i use `current.dat` to count every single time
after it uploads, the file is in dropbox so it needs to download `current.dat`
<br>
```
1208
```
read and edit(update) it with incremental +1 and upload it to **dropbox**.
<br>
`current.dat` +1
```
1209
```

it's used to know we're we are at the moment too.






### Notes
> the only main files are `app.py` other .py app is just me practicing before i implement it.

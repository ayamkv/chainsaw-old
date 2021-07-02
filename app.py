from pathlib import Path
from PIL import Image
from keys import *
from dropbox import Dropbox
import dropbox
import numpy as np
import os, tweepy, time, math, sys, io, glob


sleep = time.sleep

if production == 'true':
    print(status_project + '\n ')
    dbx = dropbox.Dropbox(TOKEN)
    auth = tweepy.OAuthHandler(apikey, apikey_secret)
    auth_url = auth.get_authorization_url()
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    print('Auth success\n\n')
    print ("Authenticated as: %s" % api.me().screen_name)   
else:
    print(10 * '\n')
    print(status_project + '\n')




def job():
    
    def get_var_value(filename="current.dat"):
        with open(filename, "a+") as f:
            f.seek(0)
            val = int(f.read() or 0) + 3
            f.seek(0)
            f.truncate()
            #if production , write the next value on dat else, write value - 1 (current)
            # if production == 'true':
            f.write(str(val))
            # else:
            #     f.write(str(val - 1))
            return val

    #####################

    #TOTAL IMAGE
    out_of = '1640'
    #NUMBER IMAGE
    n_counter = get_var_value() 
    #CURRENT COUNTER
    current_counter = n_counter - 3
    #NEXT COUNTER
    next_counter = n_counter + 3
    #IMAGE PATH DOWNLOADED
    image_path = Path('./images/{}.png'.format(n_counter))
    #NUMBER?
    the = Path('./images/{}.png'.format(n_counter)).stem
    #PATH STRING FOR PRINT
    path_string = './images/' + the + '.png' 
    #TWITTER TEXT , TWEET
    tweet = (":: Frame {} out of {} from Chainsaw Man PV.\n\n::\n#ChainsawMan #ChainsawManFrames #CSM{}\n".format(the, out_of, the))
    #DROPBOX DOWNLOAD
    # file = f"{n_counter}.png"
    file_from = f"/csm/images/{n_counter}.png"
    file_to = f'images/{n_counter}.png'

    print('[=JOB STARTED=]')
    print('\n[::] now on frame : ' + the)
    print(file_from)
    print('\nDownloading FIles................')   
    dbx.files_download_to_file(file_to, file_from)     
    time.sleep(1)
    #IMAGE COMPRESSED
    image_c = Image.open(image_path)
    x, y = image_c.size
    x2, y2 = math.floor(x-70), math.floor(y-40)
    rzd = x2, y2
    print('Original Resolution')
    print(image_c.size)
    print('Compressed to (for banner) ' )
    print(rzd)
    image_cpath = Path('./images/{}r.jpg'.format(n_counter))
    

    def compress_image(im, filename, target):
        """Save the image as JPEG with the given name at best quality that makes less than "target" bytes"""
        # Min and Max quality
        Qmin, Qmax = 25, 96
        # Highest acceptable quality found
        Qacc = -1
        while Qmin <= Qmax:
            m = math.floor((Qmin + Qmax) / 2)

            # Encode into memory and get size
            buffer = io.BytesIO()
            im.save(buffer, format="JPEG", quality=m)
            s = buffer.getbuffer().nbytes

            if s <= target:
                Qacc = m
                Qmin = m + 1
            elif s > target:
                Qmax = m - 1
        # Write to disk at the defined quality
        if Qacc > -1:
            im.save(filename, format="JPEG", quality=Qacc)
        else:
            print("ERROR: No acceptble quality factor found", file=sys.stderr)
            image_cpath = image_path
            print(image_cpath)
            print('Using original image since its not working')
    im = Image.open(image_path)
    compress_image(im, "./images/{}r.jpg".format(n_counter), 100000)    
    print('[~] Compress done')
    

    if production == 'true':
        print('\n\n_________Posting__Tweet________________\n')
        print('\n[::] Youre now on frame : ' + the)
        print('[<<] Frame Before : {}'.format(current_counter))
        print('This is the image path : ' + path_string)
        print('tweeting...')
        api.update_with_media(image_path, tweet)
        # os.startfile(image_path)
        print('\n[<>] its tweeted')
        print('This is your tweet :\n\n' + tweet) 
        print('\n[>>] Next Frame : {}'.format(next_counter))
        time.sleep(1)
        api.update_profile_banner(image_cpath)
        print('[<>] Image Banner Updated')
        # os.startfile(image_cpath)
        
        time.sleep(6)
        
    else:
        print('\nNot tweeting Because ' + status_project)
        print('Your next frame: ' + the)
        print('This is the next image path : ' + path_string)

def delete_files():
    sleep(3)
    pngfiles = glob.glob('./images/*.png')
    jpgfiles = glob.glob('./images/*.jpg')
    for f in pngfiles:
        os.remove(f)
    sleep(2)
    for j in jpgfiles:
        os.remove(j)
     
    print(' All Png and Jpg .Deleted. ')


print('---- Running Job ----- ')

def looping():
    print('-- Looping range 3 / im inside looping -- ')
    for _ in range(5):
        # get_var_value() 
        sleep(2)
        print ("Authenticated as: %s" % api.me().screen_name) 
        job()
        

while True:
    print('im running...')
    print('im inside while true\n')
    sleep(1)
    looping()
    print('[=JOB DONE=]')
    print('wait for delete image')
    sleep(5)
    delete_files() 
    print(3 * '\n')
    print(10 * '-')
    print('\n[[]-[]] Im sleeping  :D Waiting for the next time im runnin\n')
    sleep(25200) # 5.5 Hours
    print(20 * '=')
    print('\n[[]=[]] Im Awake!!!! Lets get started :D \n')
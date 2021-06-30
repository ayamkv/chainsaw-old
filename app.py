from pathlib import Path
from PIL import Image
from keys import *
from dropbox import Dropbox
import dropbox
import numpy as np
import os, tweepy, time, math, sys, io


while True:

    if production == 'true':
            
            print(status_project + '\n ')
            dbx = dropbox.Dropbox(TOKEN)
            auth = tweepy.OAuthHandler(apikey, apikey_secret)
            auth.set_access_token(token, token_secret)
            api = tweepy.API(auth)
            print('Auth success\n\n')
            for _ in range(2):
                def get_var_value(filename="current.dat"):
                    with open(filename, "a+") as f:
                        f.seek(0)
                        val = int(f.read() or 0) + 3
                        f.seek(0)
                        f.truncate()
                        #if production , write the next value on dat else, write value - 1 (current)
                        if production == 'true':
                            f.write(str(val))
                        else:
                            f.write(str(val - 1))
                        
                        return val

                        #####################

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
                desc = (":: Frame {} out of {} from Chainsaw Man PV.\n\n:: Skipping\n#ChainsawMan #ChainsawManFrames #CSM{}\n".format(the, out_of, the))
                #DROPBOX DOWNLOAD
                print('[::] Youre now on frame : ' + the)
                file = f"{n_counter}.png"
                file_from = f"/csm/images/{n_counter}.png"
                file_to = f'images/{n_counter}.png'
                print(file_from)
                print('\nDownloading FIles................')   
                
                dbx.files_download_to_file(file_to, file_from)     
                time.sleep(2)
                #IMAGE COMPRESSED
                image_c = Image.open(image_path)
                x, y = image_c.size
                totalsize = x*y
                x2, y2 = math.floor(x-70), math.floor(y-40)
                rzd = x2, y2
                print('Original Resolution')
                print(image_c.size)
                print('Compressed to (for banner) ' )
                print(rzd)
                image_cpath = Path('./images/{}r.jpg'.format(n_counter))
                def JPEGSaveWithTargetSize(im, filename, target):
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

                
                JPEGSaveWithTargetSize(im, "./images/{}r.jpg".format(n_counter), 100000)
                
                print('[~] Compress done')
                
                
                if production == 'true':
                    print('\n\n___________________________\n')
                    
                    print('[<<] Frame Before : {}'.format(current_counter))
                    print('This is the image path : ' + path_string)
                    print('tweeting...')
                    tweet = api.update_with_media(image_path, desc)
                    # os.startfile(image_path)
                    print('\n[<>] its tweeted')
                    print('This is your tweet :\n\n' + desc) 
                    print('\n[>>] Next Frame : {}'.format(next_counter))
                    time.sleep(1)
                    api.update_profile_banner(image_cpath)
                    print('[<>] Image Banner Updated')
                    # os.startfile(image_cpath)
                    time.sleep(6)
                    try:
                        if totalsize < 2073600:
                            os.remove(image_path)
                        else:
                            None
                    except WindowsError:
                        time.sleep(3)
                    print(' .. ')
                else:
                    print('\nNot tweeting Because ' + status_project)
                    print('Your next frame: ' + the)
                    print('This is the next image path : ' + path_string)


    else:
        print(status_project + '\n')

print('Waiting.......')

time.sleep(51840)
exec(open("delete.py").read())
time.sleep(1)


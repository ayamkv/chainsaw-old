from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
from keys import *
from dropbox import Dropbox
import dropbox
import numpy as np
from datetime import datetime, time, timedelta
from time import sleep
import os, tweepy, time, math, sys, io, glob, signal
import pytz

wib_tz = pytz.timezone('Asia/Jakarta')
file_from_v = 'current.dat'
file_to_v = '/csm/current.dat'

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
    
    file_from_v = 'current.dat'
    file_to_v = '/csm/current.dat'

    def upload_file(file_from_v, file_to_v):
        f = open(file_from_v, 'rb')
        # percentage = f.content
        # percentage = percentage.decode('utf-8')
        # print(percentage)
        dbx.files_upload(f.read(), file_to_v, mode=dropbox.files.WriteMode.overwrite)

    def download_file(file_from_v, file_to_v):
        dbx.files_download_to_file(file_to_v, file_from_v)

        


    def get_var_value(filename=file_from_v):
        download_file(file_to_v, file_from_v)
        print('wait for sync')
        time.sleep(3)
        print('dat Downloaded')
        with open(filename, "a+") as f:
            f.seek(0)
            val = int(f.read() or 0) + 2
            f.seek(0)
            f.truncate()
            #if production , write the next value on dat else, write value - 1 (current)
            # if production == 'true':
            f.write(str(val))
            print('dat write : %s' % val)
            # else:
            #     f.write(str(val - 1))
            return val

    def value_read(filename=file_from_v):
        # This opens a handle to your file, in 'r' read mode
        fh = open('current.dat', 'r')
        fh.seek(0)
        val = int(fh.read())
        fh.seek(0)
        return val
            
    def print_acc():
        account = dbx.users_get_current_account()
        print('[dbx] ' + account.name.given_name, account.name.surname)
        print('[dbx] ' + account.email)
        print( 2 * '\n')


    def value_func():
        get_var_value()
        upload_file(file_from_v,file_to_v)
        print('dat Uploaded\n')
        print( 5 * '_' )
        
    
    print_acc() 
    value_func()

    #####################

    #TOTAL IMAGE
    out_of = '1640'
    #NUMBER IMAGE
    n_counter = value_read()
    #CURRENT COUNTER
    current_counter = n_counter - 1
    #NEXT COUNTER
    next_counter = n_counter + 1
    #IMAGE PATH DOWNLOADED
    image_path = Path('./images/{}.png'.format(n_counter))
    #NUMBER?
    the = Path('./images/{}.png'.format(n_counter)).stem
    #PATH STRING FOR PRINT
    path_string = './images/' + the + '.png' 
    #TWITTER TEXT , TWEET
    tweet = (":: Frame {} out of {} from Chainsaw Man PV.\n\n#ChainsawMan #ChainsawManFrames #CSM{}\n".format(the, out_of, the))
    #DROPBOX DOWNLOAD
    # file = f"{n_counter}.png"
    file_from = f"/csm/images/{n_counter}.png"
    file_to = f'images/{n_counter}.png'
    
    print(10 * '_' + '[=JOB STARTED=]' + 10 * '_' )
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
    
    outputpath = ('./images/{}r.jpg'.format(n_counter))
    def BlurrBanner():
        imBlur = image_c.filter(ImageFilter.GaussianBlur(7))
        imBlur.save(outputpath)
        print('Blurred', end='\r')


    def textBanner():
        sleep(3)
        image_ppath = Image.open(image_cpath)
        overlay = Image.open(r'./images/overlay/overlay.png')
        image_ppath.paste(overlay, (0, 0), overlay)
        image_ppath.save(outputpath)
        # imBright.enhance(factorBright).save(outputpath,'PNG')
        print('Texted', end='\r')
    sleep(3)
    BlurrBanner()
    textBanner()
    
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
    im = Image.open(image_cpath)
    compress_image(im, "./images/{}rr.jpg".format(n_counter), 100000)
    img_banner = Path('./images/{}rr.jpg'.format(n_counter))
    print('[~] Compress done')
    

    if production == 'true':
        print('\n\n___Posting__Tweet____\n')
        print('\n[::] Youre now on frame : ' + the)
        print('[<<] Frame Before : {}'.format(current_counter))
        print('This is the image path : ' + path_string)
        print('tweeting...')
        api.update_with_media(image_path, tweet)
        # os.startfile(image_path)
        print('\n[<>] Its Tweeted! YAY')
        print('This is your tweet :\n\n' + tweet) 
        print('\n[>>] Next Frame : {}'.format(next_counter))
        time.sleep(1)
        api.update_profile_banner(img_banner)
        print('[<>] Image Banner Updated')
        # os.startfile(image_cpath)
        
        time.sleep(3)
        
    else:
        print('\nNot tweeting Because ' + status_project)
        print('Your next frame: ' + the)
        print('This is the next image path : ' + path_string)

def delete_files():
    sleep(3)
    pngfiles = glob.glob('./images/*.png')
    # jpgfiles = glob.glob('./images/*.jpg')
    for f in pngfiles:
        # os.remove(f)
        print(f)
        os.system('rm images/*.png')
        os.system('rm images/*.jpg')
    sleep(2)
    # for j in jpgfiles:
    #     os.remove(j)
     
    print(' All Png and Jpg .Deleted. ')


print('---- Running Job ----- ')

def looping():
    print('-- Looping range 3 / im inside looping -- ')
    for _ in range(3):
        # get_var_value() 
        sleep(2)
        print ("Authenticated as: %s" % api.me().screen_name) 
        job()
        
def everything():
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

def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return (hours, minutes, seconds)

current_date = datetime.now(wib_tz)
hours = 6
hours_added = timedelta(hours = hours)
future_date = str(current_date + hours_added)
ftur = current_date + hours_added
fturs = ftur.strftime("%H:%M:%S || %d %B, %Y")
fturjson = ftur.strftime("%B %d, %Y %H:%M:%S")
print('Today : ', current_date.strftime("%d %B, %Y '-' %H:%M:%S"))
req = datetime.strptime(future_date, '%Y-%m-%d %H:%M:%S.%f%z')
now = datetime.now(wib_tz)

def countdown_sleep(t):
    print('\n' + fturs)
    while t:
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        timeformat = '{:d} Hour :{:02d} Minute :{:02d} Sec'.format(h, m, s)
        print(timeformat, end='\r')
        time.sleep(5)
        t -= 5
        
    print('Timer Doneeee!\n\n\n\n\n')


  

    
    # while req>now:
    #     sleep(1)
    #     cdp = " %d Hours %d Minutes %d Seconds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, req))
    #     sleep(1)
    #     now = datetime.now(wib_tz)
    #     cds = str(cdp)   # print('\n ' + ftur.strftime, end="\r", flush=True)
    #     print( '>  ' + cds, end="\r", flush=True)

    #     sleep(1)
    
def convert_sec(hour):
   hour = hour * 3600

   return hour
 
sleep_value = convert_sec(6)
print(sleep_value)
# @app.route('/id')
# def tweet():
#     id = {'id':id_tweet}
#     return jsonify(id)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    while True:
        everything()
        print('\n[[]-[]] Im sleeping  :D Waiting for the next time im runnin : \n')
        
        countdown_sleep(sleep_value)
        print('\n')
        # 7 Hours
        print(20 * '=')
        print('\n[[]=[]] Im Awake!!!! Lets get started :D \n')

    #time.sleep(3)

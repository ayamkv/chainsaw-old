import os, time
import glob

time.sleep(2)

files = glob.glob('./images/*.png')
for f in files:
    os.remove(f)
    
time.sleep(2)

from PIL import Image, ImageEnhance, ImageFilter
from time import sleep
overlay = Image.open(r'./images/overlay/overlay.png')
imagepath = Image.open(r'./images/968r.jpg')
outputpath = './images/968rr.jpg'

# factorBright = 0.9
# imBright = ImageEnhance.Brightness(imagedimpath)
def BlurrBanner():
    imBlur = imagepath.filter(ImageFilter.GaussianBlur(7))
    imBlur.save(outputpath)
    print('Blurred', end='\r')


def textBanner():
    sleep(3)
    imagedimpath = Image.open(r'./images/968rr.jpg')
    imagedimpath.paste(overlay, (0, 0), overlay)
    imagedimpath.save(outputpath)
    # imBright.enhance(factorBright).save(outputpath,'PNG')
    print('Texted', end='\r')


textBanner()

# imf.save('./images/968rr.jpg')





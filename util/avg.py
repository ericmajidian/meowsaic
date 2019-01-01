import sys
import os
from PIL import Image

def avg_it(img_path):
    print(img_path)
    img = Image.open(img_path)
    w, h = img.size
    pix = img.load()
    r, g, b = 0, 0, 0
    numpixels = 0
    for y in range(0, h):
        for x in range(0, w):
            numpixels += 1
            rgb = pix[x, y]
            r += rgb[0]
            g += rgb[1]
            b += rgb[2]
    r = int(r / numpixels)
    g = int(g / numpixels)
    b = int(b / numpixels)

    savepath = "hqcats/%d_%d_%d" % (r, g, b)
    img.save(savepath, 'JPEG')
    img = img.resize((64,64), Image.ANTIALIAS)
    savepath = "cats/%d_%d_%d" % (r, g, b)
    img.save(savepath, 'JPEG')
    os.remove(img_path)
    return (r, g, b)

if __name__ == '__main__':
    for filename in os.listdir('tmp'):
        filepath='tmp/'+filename
        r, g, b = avg_it(filepath)
        print(r, g, b)

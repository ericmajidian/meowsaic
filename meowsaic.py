from PIL import Image
import matplotlib.pyplot as plt
import sys
import os
import math
from progress.bar import Bar

def Usage():
    print("Usage:")
    print("\tpython3 meowsaic.py <inputImagePath> <outputImagePath> [quality]")
    print("\n\tQuality determines the number of pixels per cat picture.\n"
          "\tMust be 1 (16x16), 2 (32x32), or 3 (64x64).\n"
          "\tDefaults to 3 if not provided.\n")

def parseArguments(argv):
    args = sys.argv[1:]
    if len(args) < 2 or len(args) > 3:
        Usage()
        exit(1)

    inputPath = args[0] 
    outputPath = args[1]
    quality = 64
    if len(args) == 3:
        q = int(args[2])
        if q == 1:
            quality = 16
        elif q == 2:
            quality = 32
        elif q == 3:
            quality = 64
        else:
            Usage()
            exit(1)

    return inputPath, outputPath, quality

def resizeInputImage(inputPath):
    """
    Resizes the input image to have a width and height
    that are factors of 64.
    """
    img = Image.open(inputPath)
    width, height = img.size

    while width % 64 != 0:
        width += 1
    while height % 64 != 0:
        height += 1

    img = img.resize((width,height), Image.ANTIALIAS)
    return img

def calculateTileWidth(width, height):
    """
    Currently sets tileWidth to 4. May update later 
    to dynamically determine an appropriate tileWidth.
    """
    return 4

def getCatInfo():
    """
    Gets the average RGB value and file path for each
    image in the cats/ directory.
    """
    catColors = []
    catFiles = []
    for filename in os.listdir('cats'):
        catFiles.append(filename)
        r, g, b = filename.split('_')
        catColors.append((int(r), int(g), int(b)))
    return (catColors, catFiles)

def getTileAvgs(inputImg, tileWidth):
    """
    Calculates the average RGB value of a tile
    from the input image.
    """
    width, height = inputImg.size
    pix = inputImg.load()
    tileAvgs = []

    for y in range(0, height, tileWidth):
        for x in range(0, width, tileWidth):
            r, g, b = pix[x, y]
            for i in range(0, tileWidth):
                r += pix[x + i, y + i][0]
                g += pix[x + i, y + i][1]
                b += pix[x + i, y + i][2]
            r = int(r / tileWidth)
            g = int(g / tileWidth)
            b = int(b / tileWidth)
            tileAvgs.append((r,g,b))

    return tileAvgs

def getMatchingCats(tileAvgs, catColors, catFiles):
    """
    Returns a list of indices into catFiles which match
    each tile in tileAvgs to the best fit cat photo.
    """
    matchingCats = []
    for i in range(0, len(tileAvgs)):
        r1, g1, b1 = tileAvgs[i]
        diff=[0]*len(catFiles)
        for c in range(0, len(catFiles)):
            r2, g2, b2 = catColors[c]
            diff[c] = (((r2-r1)*0.3)**2 +
                       ((g2-g1)*0.59)**2 +
                       ((b2-b1)*0.11)**2)
            # 0.3 0.59 0.11
        minValue = sys.maxsize
        minIndex = len(catFiles) + 1
        for d in range(0, len(diff)):
            if diff[d] < minValue:
                minValue = diff[d]
                minIndex = d
        matchingCats.append(minIndex)
    return matchingCats

def createMosaic(inputImg, outputPath, quality):
    """
    Creates the mosaic using the average RGB value of each tile from the
    original image.
    """
    catColors, catFiles = getCatInfo()
    tileWidth = calculateTileWidth(inputImg.size[0], inputImg.size[1])
    tileAvgs = getTileAvgs(inputImg, tileWidth)
    matchingCats = getMatchingCats(tileAvgs, catColors, catFiles)
    width, height = inputImg.size

    bar = Bar('Cats:', max=((width/tileWidth)*(height/tileWidth)))

    # CON helps determine the size of the mosaic based on the quality of
    # each cat picture and the tileWidth.
    CON = int(quality / tileWidth)   

    # Cat pictures are pasted onto bg.
    bg = Image.new('RGBA', (width*CON, height*CON), (255, 255, 255, 255))

    count = 0
    for y in range(0, height*CON, tileWidth*CON):
        for x in range(0, width*CON, tileWidth*CON):
            catPath = 'cats/'+catFiles[matchingCats[count]]
            catImg = Image.open(catPath)
            catImg = catImg.resize((tileWidth*CON, tileWidth*CON), Image.ANTIALIAS)
            bg.paste(catImg, (x, y))
            count += 1
            bar.next()
    bg.save(outputPath)
    bar.finish()

if __name__ == '__main__': 

    inputPath, outputPath, quality = parseArguments(sys.argv)
    inputImg = resizeInputImage(inputPath)
    createMosaic(inputImg, outputPath, quality)

import os
from PIL import Image
from tqdm import tqdm

def cornerLeftFill(xStart, xEnd, y):
    fillColor = pix[(xEnd + 1), y]
    for x in range(xEnd - xStart):
        try:
            pix[(xStart+x), y] = fillColor
        except Exception:
            pass

def cornerRightFill(xStart, xEnd, y):
    fillColor = pix[(xEnd - 1), y]
    for x in range(xStart - xEnd):
        try:
            pix[(xStart-x), y] = fillColor
        except Exception:
            pass

def CornerFill():
    TopCornerList = [35, 28, 23, 22, 19, 19, 15, 15, 13, 13, 11, 11, 9, 9, 7, 7, 7, 7, 5, 5, 5, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2] #Gross, but works
    y = 0
    for x in TopCornerList:
        cornerLeftFill(0, x, y)
        y +=1

    y = 0
    for x in TopCornerList:
        newX = 750-x
        cornerRightFill(750, newX, y)
        y +=1

    y = 1000
    for x in range(46):
        cornerLeftFill(0, 32, y)
        y +=1

    y = 1000
    for x in range(46):
        newX = 750-33
        cornerRightFill(750, newX, y)
        y +=1

def boarderFill(): #Creation of extra boarder
    for y in range(1046):
        for x in range(750):
            fillColor = pix[x, y]
            newPix[x+33, y+32] = fillColor
            if y == 0:
                for b in range(32):
                    newY = y+31-b
                    newPix[x+33, newY] = fillColor
            elif y == 1045:
                for b in range(32):
                    newY = y+33+b
                    newPix[x+33, newY] = fillColor
            elif x == 0:
                for b in range(33):
                    newX = x+32-b
                    newPix[newX, y+32] = fillColor
            elif x == 749:
                for b in range(33):
                    newX = x+34+b
                    newPix[newX, y+32] = fillColor

    for y in range(33):
        for x in range(34):
            fillColor = newPix[34, y]
            newPix[x, y] = fillColor

    for y in range(33):
        for x in range(34):
            fillColor = newPix[781, y]
            newPix[815-x, y] = fillColor

    for y in range(33):
        for x in range(34):
            fillColor = newPix[34, 1109-y]
            newPix[x, 1109-y] = fillColor

    for y in range(33):
        for x in range(34):
            fillColor = newPix[782, 1109-y]
            newPix[815-x, 1109-y] = fillColor

def main(filename):
    global im, pix
    im = Image.open('images/'+filename)
    pix = im.load()

    CornerFill()

    global newImage, newPix
    newImage = Image.new('RGB', (816, 1110))
    newPix = newImage.load()

    boarderFill()

    newImage.save('images/' + filename)

def BSM(): #integration for main
    toFolder = os.listdir('images')
    for num in tqdm(range(len(toFolder)), desc='Creating boarders...'):
        main(toFolder[num])
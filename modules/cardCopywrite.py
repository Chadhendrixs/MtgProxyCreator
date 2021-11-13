import os
import cv2
from pytesseract import pytesseract
from PIL import Image
import numpy
import shutil
from tqdm import tqdm
from copy import copy
from autocorrect import Speller
import concurrent.futures

def cut(filename, pixRange): #Cropping image for tesseract
    im = Image.open('images/'+filename)
    pix = im.load()
    cropImage = Image.new('RGB', ((pixRange[2] - pixRange[0]), (pixRange[3] - pixRange[1])))
    cropPix = cropImage.load()
    for y in range(pixRange[3] - pixRange[1]):
        for x in range(pixRange[2] - pixRange[0]):
            fillColor = pix[(x+pixRange[0]), (y+pixRange[1])]
            cropPix[x, y] = fillColor
    open_cv_image = numpy.array(cropImage)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    return gray

def fill(filename, pixRange): #Filling in determined area
    try:
        im = Image.open('images/' + filename)
        pix = im.load()
        fillColor = pix[pixRange[0], pixRange[1]]
        for x in range(pixRange[2] - pixRange[0]):
            for y in range(pixRange[3] - pixRange[1]):
                pix[pixRange[0]+x, pixRange[1]+y] = fillColor
        im.save('__temp__/' + filename)
        return True
    except:
        return False

def main(argGroup): #Trying to detect text, slowly increasing the black threshhold until tesseract can read it.
    fileName = argGroup[0]
    location = argGroup[1]
    if location[2] == 570:
        location[2] = location[2]-135
        cropped = cut(fileName, location)
        location[2] = location[2]+135
    else:
        cropped = cut(fileName, location)
    for num in range(50):
        edited = copy(cropped)
        edited[edited >= num] = 255
        value = pytesseract.image_to_string(edited)
        value = str(Spell(value))
        if '©' in value.lower():
            if fill(fileName, location):
                return True
            else:
                return False
        elif 'wizards' in value.lower():
            if fill(fileName, location):
                return True
            else:
                return False
    return False

def mainInv(argGroup): #Inverse of main. Trying to detect text, slowly decreasing the black threshhold until tesseract can read it.
    fileName = argGroup[0]
    location = argGroup[1]
    if location[2] == 570:
        location[2] = location[2]-135
        cropped = cut(fileName, location)
        location[2] = location[2]+135
    else:
        cropped = cut(fileName, location)
    for num in range(50):
        edited = copy(cropped)
        edited[edited <= 100-num] = 0
        value = pytesseract.image_to_string(edited)
        value = str(Spell(value))
        if '©' in value.lower():
            if fill(fileName, location):
                return True
            else:
                return False
        elif 'wizards' in value.lower():
            if fill(fileName, location):
                return True
            else:
                return False
    return False

def copywriteRemoval():
    pytesseract.tesseract_cmd = 'Tesseract/tesseract.exe' #Tesseract location
    global Spell
    Spell = Speller(lang='en')

    m15Fill = [443, 973, 702, 998]
    m15cFill = [442, 994, 702, 1013]
    oldFill = [56, 991, 502, 1009]
    midFill = [180, 970, 570, 990]
    ninetyFill = [70, 970, 480, 990]
    locations = [m15Fill, m15cFill, oldFill, midFill, ninetyFill] #location of copywrite on all(?) mtg boarders

    path = os.listdir('images')
    for fileName in tqdm(range(len(path)), desc='Removing Copywrite...'):
        argGroup = []
        for location in locations:
            argGroup.append([path[fileName], location])

        with concurrent.futures.ThreadPoolExecutor() as executor: #Multi-threading, to not take a million years
            futures = [executor.submit(main, param) for param in argGroup]
            results = [f.result() for f in futures]
        
        if True in results:
            pass
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor: #Multi-threading the inverse if main failed.
                futures = [executor.submit(mainInv, param) for param in argGroup]
                results = [f.result() for f in futures]
                if True in results:
                    pass
                else:
                    shutil.move('images/' + path[fileName], 'failed')
import os
from numpy.lib.function_base import _place_dispatcher
from modules.cardDownload import downloadMain
from modules.cardResize import resize
from modules.cardCopywrite import copywriteRemoval
from modules.cardBSM import BSM
from tqdm import tqdm
import shutil

def confirmation():
    while True:
        confirm = input('"Yes" or "No": ').lower()
        if confirm == 'yes' or confirm == 'y':
            break
        else:
            print('Understood! Please type "Yes" when you are ready.')
            print('---')

#Download
print('')
print('')
print('')
print('---')
print('Hello! Please make sure you have pasted the decklist into "list.txt".')
print('Please remove any basic lands, or any duplicate cards.')
print('---')
print('Ready to download?')
print('')
confirmation()
downloadMain('list.txt')
#----------

#Copywrite Removal
print('')
print('Alright! The download process is complete, please')
print('make sure all images have been downloaded; and')
print('all images are correct. When you are happy, please')
print('type "Yes" to prep the cards, and remove the copywrite!')
print('')
confirmation()
path = os.listdir('images')
for fileName in tqdm(range(len(path)), desc='Resizing...'):
    resize('images/' + path[fileName])
copywriteRemoval()
tempPath = os.listdir('__temp__')
for x in tempPath:
    os.remove('images/' + x)
    shutil.move('__temp__/' + x, 'images')
#----------

#Boarder Safe Maker
print('')
print('Alright! All of the copywrites should be removed.')
print('Please check the file "failed" to see if any of')
print('the images couldn\'t be scanned. If this is the case,')
print('please manually remove the copywrite from them')
print('(or if there isn\'t a copywrite to remove), then')
print('place them back into the "images" folder.')
print('If everything is ready, then please confirm to')
print('make the images print safe!')
print('')
confirmation()
path = os.listdir('images')
for fileName in tqdm(range(len(path)), desc='Resizing...'):
    resize('images/' + path[fileName])
BSM()
#----------

print('All done!')
os.system('pause')
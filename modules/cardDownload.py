import requests
import shutil
from tqdm import tqdm

def download(url, filename):
    image_url = url
    r = requests.get(image_url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open("images/" + filename + ".png",'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print('Image Couldn\'t be retreived')

def downloadMain(listFile):
    with open(listFile) as f: #opening .txt file, cleaning it.
        uglyList = [line.rstrip() for line in f]
        downloadList = []
        for x in uglyList:
            downloadList.append(x.replace('1 ', ''))

    bulkList = requests.get('https://api.scryfall.com/bulk-data').json() #json data of all scryfall dbs  types
    for num in range(0, len(bulkList)):
        if bulkList['data'][num]['type'] == 'default_cards': #identify default_card db
            masterList = requests.get(bulkList['data'][num]['download_uri']).json() #download and use most current default_card db as master list

    try:
        masterList #making sure it exists
    except NameError:
        raise SystemError("List unable to download! Check internet connection and try again.")

    for num in tqdm(range(0, len(masterList)-1), desc='Downloading Images...'): #itterating through each item in masterlist to see if we want to download it, faster this way than reversed.
        for cName in downloadList:
            if '/' in cName:
                cName = cName.replace('/', '//')
            if masterList[num]['name'] == cName:
                if masterList[num]['promo']: #making sure card art isn't a promo
                    pass
                elif masterList[num]['set_type'] == 'memorabilia': #or a gold boarder
                    pass
                else:
                    if '//' in cName: #if a split card, download both halves
                        splitNames = masterList[num]['name'].split(' // ')
                        download(masterList[num]['card_faces'][0]['image_uris']['png'], splitNames[0])
                        download(masterList[num]['card_faces'][1]['image_uris']['png'], splitNames[1])
                        cName = cName.replace('//', '/')
                        downloadList.remove(cName)
                    else:
                        download(masterList[num]['image_uris']['png'], masterList[num]['name'])
                        downloadList.remove(cName)
            else:
                pass
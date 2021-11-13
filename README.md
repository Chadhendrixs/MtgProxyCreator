# MtgProxyCreator

This project makes it extremely easy to create proxy-ready files. By providing a decklist, it will download all of the card images, remove the WOTC copywrite, then enlarge the boarders to make the cards print safe for a service like [MakePlayingCards](https://www.makeplayingcards.com/).

If you wish, you can insert custom cards into the process by placing them into the images folder after downloading the rest of the list (Or by not providing a decklist at all).


# Known Issues

Due to the nature of the project and the variations within cards, some known issues can appear.

### Weird card images:
[Scryfall](https://scryfall.com/) is being used to download all of the card images. Due to how scryfall has their API set up, it is difficult to always get the best image for a card. While the program is filtering out all of the weird promos and foils, it will sometimes download an odd alternate art. Newer card images can also be blurry, since high quality scans of those cards are not yet avalible.

### "Failed" cards:
Some card images will fail to scan, and be moved to the "Failed" image folder. While this could be an issue due to the card frame being weird, is it often an issue of the background color and the text color being too similar, or too blurry. It ultimately becomes easier just to do these few by hand, instead of finding a new card frame and trying again.

### Misread / incorrect covers:
In the case of a card being misread and only a part or none of the copywrite is covered, it is sadly better to download the card art from [Scryfall](https://scryfall.com/) and do it by hand. While I wish the detection would work 100% of the time, the nature of PyTesseract and AI means it will be inconsistent and wrong occasionally. The tool will cover the bulk of the images, but some images just can't be scanned properly. Better methods for detection will be updated when found.
# Installation

Either extract the current [Release](https://github.com/Chadhendrixs/MtgProxyCreator/releases), or download the project and install the required packages:

```bash
cd MtgProxyCreator
pip install -r requirements.txt
```

The most important part of building it yourself, is making sure to install Tesseract. Download the newest version of Tesseract from [here](https://digi.bib.uni-mannheim.de/tesseract/), and install it into the file named "Tesseract" within the project. Otherwise, the module `cardCopywrite.py` will error when trying to initialize pyTesseract.

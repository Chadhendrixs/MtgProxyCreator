import cv2

def resize(filename): #Resizes to MagicSetEditor 200% viewport export size, really coulda been anything but this was easier.
    img = cv2.imread(filename, 1)
    size = img.shape
    if size[1] == 750:
        if size[0] == 1046:
            pass
        else:
            cv2.imwrite(filename, cv2.resize(img, (0, 0), fx=750/size[1], fy=1046/size[0]))
    else:
        cv2.imwrite(filename, cv2.resize(img, (0, 0), fx=750/size[1], fy=1046/size[0]))
'''
Created on 14. lip 2018.

@author: Filip
'''

import cv2
from LSB import LSB



secretMsg = input("What is the message you want to hide? ")
key = input("Which key should be used? ")
imageName = input("What is the name of  image you want to use? ")
stegoName = input("How shall we name image with hidden message? ")




print("Hiding message in image " + imageName + "." )
im=cv2.imread(str(imageName))
cv2.imshow('preSteganoImage',im)


stego=LSB.LSB_sakrij(im, secretMsg, key = int(key))


cv2.imwrite(stegoName, stego)

print("Stegano image saved as " + stegoName + " .") 

cv2.imshow('postSteganoImage', stego)

cv2.waitKey(0)
cv2.destroyAllWindows()   
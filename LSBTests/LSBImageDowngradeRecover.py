'''
Created on 15. lip 2018.

@author: Filip
'''

import cv2
from LSB import ImageLSB
print()
stego = input("From which image would you like to recover hidden image? ")
key = input("Which key should be used? ")
file = input("What is the name of file in which you would like to recover image from " + stego + "?")


image = cv2.imread(stego)
print("Opened image " + stego +".")
print("Recovering image from " + stego + ".")
im4 = ImageLSB.ImageLSB_get(image, key = int(key))

cv2.imwrite(file, im4)
cv2.imshow('recovered', im4)
cv2.waitKey(0)
cv2.destroyAllWindows()   
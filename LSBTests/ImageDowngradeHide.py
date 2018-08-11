'''
Created on 15. lip 2018.

@author: Filip
'''

from LSB import ImageLSB
import cv2

print()
secretImage = input("Which image do you wish to hide? ")
carrierImage = input("In which image would you like to hide " +secretImage +"? ")
key = input("Which key should be used for hiding? ")
carrierOut = input("What will be the name of image containing " + secretImage +"? ")
    
    
im=cv2.imread(secretImage)
cv2.imshow('secret image',im)
print("Opened image" + secretImage +".")

im2 = cv2.imread(carrierImage)
cv2.imshow("carrier", im2)
print("Opened image " + carrierImage + ".")


print("Hiding image " + secretImage + " in image " + carrierImage +".")
im3 = ImageLSB.ImageLSB_hide(im, im2, key = int(key))
cv2.imwrite(carrierOut, im3)

cv2.imshow('post stegano', im3)     
     
cv2.waitKey(0)
cv2.destroyAllWindows()   
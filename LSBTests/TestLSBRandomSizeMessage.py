'''
Created on 14. lip 2018.

@author: Filip
'''
from LSB import  LSB
import cv2
messageSize = input("What will be the size of random message? ")

string = ''

print("Generating message consisting of letter \'a\' only, with size of " + messageSize + ".")

while len(string) < int(messageSize):
    string +="a"
    
    
print("Generated message with size " + str(len(string)) + ".")


key = 5
imageName = 'test.bmp'
secretMsg = string
stegoName = 'bigDataTest.png'

print("Dummy data for testing big message: key = " + str(key) + " , image for hiding =  " + imageName + " , image carrier name =  " + stegoName + "." )



im=cv2.imread(str(imageName))
cv2.imshow('preSteganoImage',im)

print("Size of image " + imageName +" (considering (width, height, depth) tuple): " + str(im.shape))

print("Hiding message in image " + imageName + "." )
stego=LSB.LSB_sakrij(im, secretMsg, key = int(key))


cv2.imwrite(stegoName, stego)

print("Stegano image saved as " + stegoName + " .") 

cv2.imshow('postSteganoImage', stego)

cv2.waitKey(0)
cv2.destroyAllWindows()   
'''
Created on 14. lip 2018.

@author: Filip
'''

import cv2
from LSB import LSB

print()
stego = input("From what image do you like to retrieve message? ")
key = input("Which key should be used? " )

nova=cv2.imread(stego)
print("Opened image named " + stego +".")
poruka=LSB.LSB_dohvati(nova, key = int(key))


print("Retrieved message: ", end='')
print(poruka)
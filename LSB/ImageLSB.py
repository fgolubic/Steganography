'''
Created on 11. svi 2018.

@author: Filip
'''

import numpy as np
import random

def PRNG(noOfPositions, width, height, depth, key):
    
    positions=list()
    
    random.seed(key)
    
    positionCounter=0
    
    while positionCounter < noOfPositions:
        
        x=random.randint(0,width - 1)
        y=random.randint(0,height - 1)
        z=random.randint(0,depth - 1)
        
        randomPosition=(x, y, z)
        
        if randomPosition in positions:
            continue
        
     
        
        positions.append(randomPosition)
        
        positionCounter+=1
        
    print("Random positions successfully generated!")  
    return positions
    
    
def IsStegoPossible(image, carrier):
    
    w1, h1, d1 = image.shape
    w2, h2, d2 = carrier.shape
    
    if((w1 * h1 * d1) + 8) > (w2 * h2 * d2):
        return False
    
    return True

def ImageDowngrade(image, key = 4):

    downgradedImage = list()
    width, height, depth = image.shape
    
    
    for i in range(0,width):
        
                    for j in range(0,height):
                        
                        for k in range(0,depth):
                                
                                temp=bin(image[i,j,k])[2:]
                                
                                while(len(temp)<8):
                                    temp='0' + temp
                                
                                mostSignBits = temp[:key]
                                
                                
                                
                                downgradedImage.append(mostSignBits)
                                
                                
    return downgradedImage
                               
       
    

def ImageLSB_hide(image, carrier, key = -1):
    
    if not IsStegoPossible(image, carrier):
        exit('Image must be SMALLER than carrier.')
        
    
    width, height, depth = carrier.shape
    
    w, h, d = image.shape
    
    dataSize = w * h * d
    
    widthBits = bin(w)[2:]
    
    
    while len(widthBits) < 15:
        widthBits = '0' + widthBits
    
    heightBits = bin(h)[2:]
    
    while len(heightBits) < 15:
        heightBits = '0' + heightBits
        
    depthBits = bin(d)[2:]
    
    while len(depthBits) < 2:
        depthBits = '0' + depthBits
    
    
    """
    Size is represented by 15 bits for width , 15 bits for height and 2 bits for depth,
     summing up to total of 32 bits that represent the shape of the image.
    """
    size_bits = str(widthBits) + str(heightBits) + str(depthBits)
    
     
    """
     Get list of 4 most significant bits for every element of the image.
    """
    imageBits = ImageDowngrade(image)
    
    
    stego = carrier
    
    #counter for no. of elements written into stego object
    dataProcessed = 0
    
    
    #counter for tracking how many size bits were written
    sizeCounter = 0
    
    print("Hiding image using key " + str(key) + ".")
    
    if key == -1:
        
        """
        Size is being hidden 4 bits per image element.
        """ 
        for i in range(0,width):
            
            for j in range(0, height):
                
                for k in range(0, depth):
                    
                    temp=bin(stego[i,j,k])[2:]
                    
                    while(len(temp)<8):
                        temp='0' + temp
                        
                    temp2=temp[0:4]+size_bits[sizeCounter:sizeCounter + 4]
                    
                    
                    
                    stego[i,j,k]=int(temp2,2)
                    sizeCounter+=4
                    
                    if sizeCounter == 32: break
                    
                if sizeCounter == 32: break
                
            if sizeCounter == 32: break
                    
                    
        i+=1
        j+=1
        k+=1
        
        #continue from the last position where last 4 bits of size were written
        
        while i < width:
            
            while j < height:
                
                while k < depth:
                    
                    temp=bin(stego[i,j,k])[2:]
                    
                    while len(temp) < 8:
                        
                        temp = '0' + temp
                        
                    temp2 = temp[:4] + imageBits[dataProcessed]
                    
                    stego[i,j,k] = int(temp2, 2)
                    
                    dataProcessed += 1
                    
                    k += 1
                    if dataProcessed == dataSize: break
                k=0        
                j+=1 
                if dataProcessed == dataSize: break
            j=0            
            i+=1 
            if dataProcessed == dataSize: break
                    
    
    
    
    else:
        
        noOfPositions = dataSize + 8
        
        positions = PRNG(noOfPositions, width, height, depth, key)
        
        i=0
        
        dataList = list()
        
        while i<32:
                        
            dataList.append(size_bits[i:i+4])
            
            i+=4
            
        
        dataList.extend(imageBits)
        
        positionsDone=0
        
        for bits in dataList:
            i, j, k = positions[positionsDone]
            
            temp=bin(stego[i,j,k])[2:]
                            
            while(len(temp)<8):
                temp='0' + temp
                        
            temp2=temp[0:4] + bits
            stego[i,j,k]=int(temp2,2)
    
            positionsDone+=1 
            
        
        
    print("Image successfully hidden!")
    return stego


def ImageLSB_get(carrier,  key = -1):
    
    stego = carrier
    
    random.seed(key)
    
    carrierWidth, carrierHeight, carrierDepth = stego.shape
    
    size_counter = 0
    
    sizeBits = ""
    
    print("Recovering image using key " + str(key) + ".")
    if key == -1:
        
        """
        Get size of hidden  image. Get its width, height and depth
        """
        for i in range(0, carrierWidth):
            
            for j in range(0, carrierHeight):
                
                for k in range(0, carrierDepth):
                    
                    temp=bin(stego[i,j,k])[2:]
                        
                    while(len(temp)<8):
                        temp='0' + temp
                            
                    temp_size=len(temp)
                    sizeBits+=str(temp[4:temp_size])    
                    size_counter+=4
                    
                    if size_counter == 32: break
                        
                if size_counter == 32: break
                    
            if size_counter == 32: break
                    
        
              
        imageWidth = int(sizeBits[0:15],2)
        
        imageHeight = int(sizeBits[15:30],2)
        
        imageDepth = int(sizeBits[30:32],2)
        
        imageSize = imageWidth * imageHeight * imageDepth  
        
        image=np.zeros((imageWidth, imageHeight, imageDepth), np.uint8)
        
        """
        Take image data from carrier and store it in a container.
        
        """
        
        i+=1
        j+=1
        k+=1
        
        imageInfo=list()
        
        infoCounter=0
        
        while i < carrierWidth:
            
            while j < carrierHeight:
                
                while k < carrierDepth:
                    
                    temp=bin(stego[i,j,k])[2:]
                            
                    while(len(temp)<8):
                        temp='0' + temp
                                
                    temp_size=len(temp)
                    imageInfo.append(temp[4:temp_size])    
                    infoCounter+=1
                    
                    k+=1   
                    if infoCounter == imageSize: break
                k=0
                j+=1            
                if infoCounter == imageSize: break
            j=0
            i+=1           
            if infoCounter == imageSize: break
        
        
        
        """
        Reconstruct hidden image from info list
        """
        
        infoCounter = 0
        
        for i in range (0, imageWidth):
            
            for j in range(0, imageHeight):
                
                for k in range(0, imageDepth):
                    
                    temp = imageInfo[infoCounter] + '0000'
                    
                    image[i,j,k] = int(temp,2)
                    
                    

                    infoCounter+=1
                       
    
    
    else:
        sizePositions = PRNG(8, carrierWidth, carrierHeight, carrierDepth, key)
        
        sizeBits = ''
        
        for position in sizePositions:
            
            temp = bin(stego[position])[2:]
            
            while len(temp)<8:
                temp = '0' + temp
                
            sizeBits += temp[4:]
            
            
        imageWidth = int(sizeBits[:15], 2)
        
    
        
        imageHeight = int(sizeBits[15:30], 2)
        
        imageDepth = int(sizeBits[30:], 2)
        
        imageSize = imageWidth * imageHeight * imageDepth
        
        image=np.zeros((imageWidth, imageHeight, imageDepth), np.uint8)
        
        positions = PRNG(imageSize + 8, carrierWidth, carrierHeight, carrierDepth, key)[8:]
        
        positionsDone = 0
        
        for i in range(0, imageWidth):
            
            for j in range(0, imageHeight):
                
                for k in range(0, imageDepth):
                    
                    position = positions[positionsDone]
                    temp = bin(stego[position])[2:]
                    
                    while  len(temp) < 8:
                        temp = '0' + temp
                    
                    image[i,j,k] = int((temp[4:] + '0000'), 2)
                    
                    positionsDone += 1
        
                
    print("Image recovered!")
    return image

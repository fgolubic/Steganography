'''
Created on 23. tra 2018.

@author: Filip
'''
import random

def IsStegoPossible(width, height, depth, messageLen):
    
    if (messageLen + 32) >( width * height * depth ):
        return False
    
    
    return True
    
    
    
def strToBin(msg):
    binMsg=str()
    
    for i in msg:
        charAscii=ord(i)
        
        tempBin=bin(charAscii)[2:]
        
        while len(tempBin)<8:
            tempBin='0'+tempBin
            
        binMsg+=tempBin
        
    return binMsg
        
    
def PRNG(noOfPositions, width, height, depth, key):
    
    positions=list()
    
    random.seed(key)
    
    positionCounter=0
    
    while positionCounter<noOfPositions:
        
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
    
    

def LSB_sakrij(image, message, key=-1):
    
    strPor=str(message)
    vel_por=bin(len(strPor))[2:]
    
    byteList=strToBin(strPor)
    
    stego=image
    w,h,d=image.shape
    size_counter=0
    msg_counter=0
   
    if not IsStegoPossible(w, h, d, len(byteList)):
        exit("Message is too big to hide in this image!")
    
    while(len(vel_por)<32):
        vel_por='0'+vel_por
    
    print("Hiding message using key " + str(key) + "." )

    
    if key==-1: 
        #Umetni velicinu poruke od 32 bita i zapamti pozicije na kojima si stao 
        for i in range(0,h):
            for j in range(0,w):
                for k in range(0,d):
                    temp=bin(stego[i,j,k])[2:]
                    
                    while(len(temp)<8):
                        temp='0' + temp
                        
                    temp2=temp[0:7]+vel_por[size_counter]
                    stego[i,j,k]=int(temp2,2)
                    size_counter+=1
                    
                    if size_counter == len(vel_por): break
                    
                if size_counter == len(vel_por): break
                
            if size_counter == len(vel_por): break
                  
        
        x=i+1
        y=j+1
        z=k+1
        
        i=x
        j=y
        k=z
        
        while i < h:
                    
            while j < w:
                        
                while k < d:
                            
                    temp=bin(stego[i,j,k])[2:]
                            
                    while(len(temp)<8):
                        temp='0' + temp
                        
                    temp2=temp[0:7] + byteList[msg_counter]
                    stego[i,j,k]=int(temp2,2)
    
                    msg_counter+=1
                            
                    k+=1
                    if msg_counter == len(byteList): break
                k=0        
                j+=1 
                if msg_counter == len(byteList): break
            j=0            
            i+=1 
            if msg_counter == len(byteList): break
                   
       
    else:
        
        noOfPositions = len(byteList)+32
        
        positions = PRNG(noOfPositions, w, h, d, key)
        
        dataToHide = vel_por+byteList
        
        positionsDone=0
        
        for bit in dataToHide:
         
            i, j, k = positions[positionsDone]
            
            temp=bin(stego[i,j,k])[2:]
                            
            while(len(temp)<8):
                temp='0' + temp
                        
            temp2=temp[0:7] + bit
            stego[i,j,k]=int(temp2,2)
    
            positionsDone+=1
                       
       
    print("Message hidden!")
    return stego




def LSB_dohvati(stego, key=-1):
    poruka='0b'
    vel_por='0b'
    w,h,d=stego.shape
    size_counter=0
    msg_counter=0
    realMsg=''
    
    print("Getting message using key " + str(key) + "." )
    if key==-1:
        
        #Procitaj velicinu poruke od 32 bita i zapamti pozicije na kojima si stao 
        for i in range(0,h):
            for j in range(0,w):
                for k in range(0,d):
                    temp=bin(stego[i,j,k])[2:]
                    
                    while(len(temp)<8):
                        temp='0' + temp
                        
                    temp_size=len(temp)
                    vel_por+=str(temp[temp_size-1])    
                    size_counter+=1
                    if size_counter == 32: break
                    
                if size_counter == 32: break
                
            if size_counter == 32: break
              
        x=i+1
        y=j+1
        z=k+1
        msg_size=int(vel_por,2)*8
        
        
        i=x
        j=y
        k=z
      
        #Procitaj poruku krenuvsi od zapamcenih pozicija
        while i < h:
            while j < w:
                while k < d:
                    temp=bin(stego[i,j,k])[2:]
                    
                    while(len(temp)<8):
                        temp='0' + temp
                        
                    temp_size=len(temp)
                    poruka+=str(temp[temp_size-1])
                    
                    msg_counter+=1
                    
                    if msg_counter%8==0:
                       
                        realMsg+=str(chr(int(poruka,2)))
                        
                        poruka='0b'
                    
                    k+=1
                    if msg_counter == msg_size: break
                k=0
                j+=1    
                if msg_counter == msg_size: break
            j=0
            i+=1    
            if msg_counter == msg_size: break
        
    
    else:
        
        sizePositions = PRNG(32, w, h, d, key)
        
        positionsDone = 0
        
        while positionsDone < 32 :
            
            i, j, k = sizePositions[positionsDone]
            
            temp=bin(stego[i,j,k])[2:]
                    
            while(len(temp)<8):
                temp='0' + temp
                        
            temp_size=len(temp)
            vel_por+=str(temp[temp_size-1])    
            
            positionsDone += 1
            
        msg_size=int(vel_por,2)*8
        
        messagePositions = PRNG(msg_size + 32 , w, h, d, key)[32:]
        
        
        positionsDone = 0
        
        while positionsDone <  len(messagePositions) :
            
            i, j, k = messagePositions[positionsDone]
            
            temp=bin(stego[i,j,k])[2:]
                    
            while(len(temp)<8):
                temp='0' + temp
                        
            temp_size=len(temp)
            poruka+=str(temp[temp_size-1])
                
            positionsDone += 1
             
            if positionsDone%8==0:
                       
                realMsg+=str(chr(int(poruka,2)))
                  
                poruka='0b'
            
             
    
    print("Message  recovered!")
    return realMsg

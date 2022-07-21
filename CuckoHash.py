# "I hereby certify that this program is solely the result of my own work and is 
# in compliance with the Academic Integrity policy of the course syllabus and 
# the academic integrity policy of the CS department.”

import time
import random
from BitHash import *
import pytest
import random

class CuckoHash(object):
    def __init__(self, size):
        self.__size = size
        self.__leftHashArray = [None] * size
        self.__rightHashArray = [None] * size
        self.__numKeys = 0
    
    # return current number of keys in table  - 
    # obtain manually to ensure accuracy in testing  
    def __len__(self): 
        ans = 0
        for i in self.__leftHashArray:
            if i:
                ans+=1
        for i in self.__rightHashArray:
            if i:
                ans+=1
        return ans  
    
    def getNumKeys(self):
        return self.__numKeys
            
    # insert key/data if the key isn't already in the table
    # return False if the key is already in the table, True otherwise
    def insert(self, k, d): 
        # make sure the key isn't already there
        if self.find(k): return False
        
        # keep track of the pair you are trying to insert
        pair = k,d

        #If the table is already too full, grow the table 
        # (.5 was chosen based on testing)       
        if self.__numKeys >= len(self.__leftHashArray)*.5:
            self.__growHash()                  
                
        # while __insert has not completed without displacing anyone and  
        # has not returned None
        while pair:
            
            # store what self.__insert returns so you know when to stop looping
            # if __insert return None you stop
            # if it returns another pair you loop again
            pair = self.__insert(pair)
                        
            # __insert looped 50 times so if your are not done you should reHash
            if pair: self.__reHash()            
        
        
        # if you reached this point:  not pair == True
        return not pair
                                     
    
    # This method tries to insert a pair 50 time. When this method is called by 
    # insert it is guaranteed to succeed beacuse it is called from a while loop
    # when it is called by __grow and __reHash there is a risk that it will 
    # fail and a pair will not make back it in to the tab.
    # This risk is very slight due to the completly new conditions and is
    # checked by the AllThere tests which ensure that each pair 
    # inserted actually can be found in the tab and Length tests which
    # ensure the length of the tab matches the number of inserts.    
    def __insert(self, pair):
        
        for i in range(50):
            
            leftLocation = BitHash(pair[0],1) % len(self.__leftHashArray)
            
            # "pick up" the contents of the left Location you are trying to place the 
            # pair in your "left hand". You very well may be holding nothing.
            leftHand = self.__leftHashArray[leftLocation] 
            # now place the pair into the left Location
            self.__leftHashArray[leftLocation] = pair
            
            # if you left hand is empty - nothing was displaced. 
            # return leftHand, which is None, and fall out of the while loop
            if not leftHand: 
                # increment numKeys here to ensure length is mantained when
                # __insert is called from __grow and __reHash                
                self.__numKeys += 1
                return leftHand
    
            # otherwise there was content in the the location before you put the pair there
            # and you need to relocate it
            else:
                rightlocation = BitHash(leftHand[0],2) % len(self.__rightHashArray)
                # "pick up" the contents of the left Location you are trying to place the 
                # displaced pair in your "right hand". You very well may be holding nothing.                
                rightHand = self.__rightHashArray[rightlocation]
                # now place the pair in your left hand into the right location
                self.__rightHashArray[rightlocation] = leftHand
                
                 # if you right hand is empty - nothing was displaced. 
                 # return rightHand, which is None, and fall out of the while loop        
                if not rightHand:
                    # increment numKeys here to ensure length is mantained when
                    # __insert is called from __grow and __reHash
                    self.__numKeys += 1
                    return rightHand
                
                
                # otherwise there was content in the the location before you put the pair there
                # and you need to relocate it by relooping - you will return pair
                # which is not None so the while loop will continue.
                else:
                    # loop again with the initial pair being the contents of right hand 
                    pair = rightHand 
        
        return pair
    
    
    def __growHash(self):
        
        ResetBitHash()
        
        # hold on to old arrays        
        temp1 = self.__leftHashArray
        temp2 = self.__rightHashArray
        
        # double size
        self.__size = self.__size*2
        
        # create future new underlying storage list using new size
        self.__leftHashArray = [None] * (self.__size)
        self.__rightHashArray = [None] * (self.__size)
        
        # reset numKeys here. each __insert will increment when it succeeds 
        self.__numKeys = 0 
        
        # for each item in the old list insert using insert helper     
        for i in range(len(temp1)):
            if temp1[i]: self.__insert((temp1[i][0], temp1[i][1]))
        for i in range(len(temp2)):   
            if temp2[i]: self.__insert((temp2[i][0], temp2[i][1]))
        
        # account for a hashArray of zero length    
        if len(self.__leftHashArray) == 0:
            self.__leftHashArray = [None]
            self.__rightHashArray = [None]  
            self.__size = 1
            
    
    def __reHash(self):
                
        ResetBitHash()
        
        # hold on to old arrays
        temp1 = self.__leftHashArray
        temp2 = self.__rightHashArray
        
        # create future new underlying storage list
        self.__leftHashArray = [None] * (len(self.__leftHashArray) )
        self.__rightHashArray = [None] * (len(self.__rightHashArray))
        
        # reset numKeys here. each __insert will increment when it succeeds 
        self.__numKeys = 0         
        
        # for each item in the old list insert using insert helper          
        for i in range(len(temp1)):
            if temp1[i]: self.__insert((temp1[i][0], temp1[i][1]))
        for i in range(len(temp2)):   
            if temp2[i]: self.__insert((temp2[i][0], temp2[i][1]))
            
   
    def find(self,k):
        if not len(self.__leftHashArray): return False
        # look in the left location and return what you find if found
        leftLocation = BitHash(k,1) % len(self.__leftHashArray)
        if self.__leftHashArray[leftLocation] and self.__leftHashArray[leftLocation][0] == (k): 
            return(k, self.__leftHashArray[leftLocation][1])
        
        # look in the right location and return what you find if found
        rightLocation = BitHash(k,2) % len(self.__leftHashArray)
        if self.__rightHashArray[rightLocation] and self.__rightHashArray[rightLocation][0] == (k): 
            return(k, self.__rightHashArray[rightLocation][1])
    
        # otherwise
        return False
    
        
    def delete(self,k):
        # look in the left location and delete return True if found        
        leftLocation = BitHash(k,1) % len(self.__leftHashArray)
        if self.__leftHashArray[leftLocation] and self.__leftHashArray[leftLocation][0] == (k): 
            self.__leftHashArray[leftLocation] = None
            self.__numKeys -= 1 
            return True
        
        # look in the right location and delete return True if found        
        rightLocation = BitHash(k,2) % len(self.__leftHashArray)
        if self.__rightHashArray[rightLocation] and self.__rightHashArray[rightLocation][0] == (k): 
            self.__rightHashArray[rightLocation] = None
            self.__numKeys -= 1 
            return True
    
        # otherwise        
        return False
        

# funtions to help with testing

def randomString(size):
    ans = ""
    for i in range(size):
        c = chr(random.randint(0,25) + ord('A'))
        ans += c
      
    return ans

def ListOfUniqueStrings(length, size=20):
    s = set()
    while len(s)<length:
        s.add(randomString(size))
    return [*s, ]

##############    
##  PYTESTS ##              
##############

# assures that insert succeeds
def test_simpleInsert():
    h = CuckoHash(1)
    assert h.insert("hello",1)
    assert h.insert("world",2)
    assert h.insert("foo",7)
    
# makes sure words inserted are found and words not inserted are not found 
def test_simpleFind():
    h = CuckoHash(1)
    h.insert("hello",1)
    h.insert("world",2)
    h.insert("foo",2)
    h.insert("bar",2)
    h.insert("baz",2)
    assert h.find("world")
    assert not h.find("blazbat")

# inserts words into tab and asserts that they all made it 
def test_simpleInsertAllThere(): 
    h = CuckoHash(1)
    u = ListOfUniqueStrings(10, 20)
    for i in range(10):
        a = u[i], i    
        h.insert(a[0],a[1])

    for i in u: 
        assert h.find(i)

# makes sure words deleted are not found  
def test_simpleDelete():
    h = CuckoHash(1)
    h.insert("hello",1)
    h.insert("world",2)
    h.insert("foo",2)
    h.insert("bar",2)
    h.insert("baz",2)
    h.delete("world")
    assert not h.find("world")
    
# makes sure the number of inserts matches the number of items in the tab
def test_simpleLength():
    h = CuckoHash(1)
    numInserts = 10
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], i    
        h.insert(a[0],a[1])
        
    assert(len(h) == numInserts == h.getNumKeys()) 


# make the tab big enought that it wont grow and assure insert succeeds
def testLargeTabManyInserts():
    h = CuckoHash(1000000)
    numInserts = 100000
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], random.randint(1,1000)   
        assert h.insert(a[0],a[1])
        
# make the tab small enought must grow and assure insert succeeds
def testSmallTabManyInserts():
    h = CuckoHash(0)
    numInserts = 100000
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], i    
        assert h.insert(a[0],a[1])  

# inserts many words into a small tab and list and asserts that they all made it 
def test_largeAllThere(): 
    numInserts = 100000
    h = CuckoHash(1)
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], random.randint(1,1000)    
        h.insert(a[0],a[1])

    for i in u: 
        assert h.find(i)

# makes sure the large number of inserts matches the number of items in the tab        
def test_largeLength():
    h = CuckoHash(1)
    numInserts = 10
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], i    
        h.insert(a[0],a[1])

    assert(len(h) == numInserts == h.getNumKeys()) 

# makes sure words deleted are not found on a large scale
def test_largeDelete():
    h = CuckoHash(1)
    numInserts = 100000
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], i    
        h.insert(a[0],a[1])
    for i in range(numInserts):
        a = u[i], i    
        h.delete(a[0])
        assert not h.find(a[0])

# makes length is zero after eveything is deleted
def test_zeroDelete():
    h = CuckoHash(1)
    numInserts = 100000
    u = ListOfUniqueStrings(numInserts, 20)
    for i in range(numInserts):
        a = u[i], i    
        h.insert(a[0],a[1])
    for i in range(numInserts):
        a = u[i], i    
        h.delete(a[0])
    assert len(h) == 0

pytest.main(["-v", "-s", "CuckoFinal.py"])
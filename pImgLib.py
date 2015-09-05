import inspect
import pdb
import numpy as np

def usage():
   helpMsg="""
   Available functions with parameters that require
   a file path to be specified via -f or --file:
   rot90, rot180, rot270:
      Rotates an image CCW by the specified angle
   flipv, fliph:
      Flips an image either vertically or horizontally.
   brightness: amount
      Alters an image's brightness. "amount" should be
      an integer between -255 (black) and 255 (white). 
   """ 
   print(helpMsg)

def nArgs(funName):
   #No problems with eval, given that this is a
   #personal use program not running as root
   return len(inspect.getargspec(eval(funName))[0])
   
def rot90(img):
   return np.rot90(img)

def rot180(img):
   return np.rot90(img, 2)

def rot270(img):
   return np.rot270(img, 3)

def flipv(img):
   return np.flipud(img)

def fliph(img):
   return np.fliplr(img)

def brightness(img, amount):
   amount=int(amount)
   upperFilter=(255-img)<amount 
   lowerFilter=img<-amount
   
   img+=amount
   img[upperFilter]=255
   img[lowerFilter]=0
   return img







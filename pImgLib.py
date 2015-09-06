import inspect
import pdb
import numpy as np

eps=0.00000001

def usage():
   helpMsg="""
   Available functions with parameters that require
   a file path to be specified via -f or --file:
   size:
      Returns the dimensions of the image
   rot90, rot180, rot270:
      Rotates the image CCW by the specified angle
   flipv, fliph:
      Flips an image either vertically or horizontally
   crop: x1 y1 x2 y2
      Crops an image with a bounding box from location
      (x1, y1) to location (x2, y2). Uses one indexing.
   cropRel: x1 y1 x2 y2
      Crops an amount off each edge of the image given by:
      left: x1
      right: x2
      top: y1
      bottom: y2
   brightness: amount
      Alters an image's brightness. "amount" should be
      an integer between -255 (black) and 255 (white). 
   contrast: multiplier
      Alters an image's contrast. "multiplier" should be
      a non-negative real number.
   contrastAndBrightness: amount multiplier
      Calls "contrast" and "brightness" with "multiplier"
      and "amount" respectively, in that order such that
      the final transformation is given by cx+b where "c"
      is contrast, "b" is brightness, and "x" is the
      original image.
   brightnessAndContrast: amount multiplier
      Calls "brightness" and "contrast" with "amount"
      and "multiplier" respectively, in that order such
      that the final transformation is given by c(x+b)
      where "c" is contrast, "b" is brightness, and "x"
      is the original image.
   grayscale: useLuminosity
      Converts an image to grayscale. Uses the luminosity
      algorithm by default, and the parameter is optional.
      Specify "False" to calculate grayscale as average
      rgb intensity.
   sepia:
      Applies the classic sepia filter to an image.
   invert:
      Inverts the colors of an image via 255-img.
   rgbTransform: r g b
      Scales the rgb components of an image, using
      "r", "g", and "b" as multipliers.
   fade: direction color mMin mMax aMin aMax addFirst
      Applies a linear gradient to the image starting
      from "direction" using "color". All other parameters
      are optional. "mMin" and 'mMax" specify the bounds
      of the multiplicative filter, "aMin" and "aMax"
      specify the bounds of the additive filter, and 
      addFirst is a boolean (True/False or 1/0) that
      specifies whether to apply the additive filter
      first and then the multiplicative filter or
      to use the opposite ordering (default).

      Valid directions: left l right r top t bottom b
      Valid colors: red green blue cyan magenta yellow
         black white grey gray OR define a custom rgb
         color with [r,g,b] with each entry between 
         0 and 255 inclusive.

   ---Generators---
   black: width height
      Solid black
   white: width height
      Solid white
   gray: width, height
      Solid gray
   solid: width height r g b
      Solid of any rgb color. "r", "g", and "b" must
      be between 0 and 255, inclusive.
   grayNoise: width height
      Random grayscale noise
   rgbNoise: width height
      Random rgb noise
    
   """ 
   print(helpMsg)

def nArgs(funName):
   #No problems with eval, given that this is a
   #personal use program not running as root
   return len(inspect.getargspec(eval(funName))[0])

def size(img):
   s=img.shape
   print("width = "+str(s[1])+", height = "+str(s[0]))
  
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

def crop(img, x1, y1, x2, y2):
   try:
      img=img[y1-1:y2, x1-1:x2, :]
   except:
      print('Error: check your crop boundaries.')
      sys.exit(2)
   return img

def cropRel(img, x1, y1, x2, y2):
   try:
      img=img[y1:-y2, x1:-x2, :]
   except:
      print('Error: check your relative crop offsets.')
      sys.exit(2)
   return img

def brightness(img, amount):
   amount=int(amount)
   upperFilter=(255-img)<amount 
   lowerFilter=img<-amount
   
   img+=amount
   img[upperFilter]=255
   img[lowerFilter]=0
   return img

def contrast(img, multiplier):
   if multiplier<0:
      print('Error: parameter "multiplier" must be non-negative')
      sys.exit(2) 
   upperFilter=img>(255.0/multiplier)
   img*=multiplier
   img[upperFilter]=255
   return img

#These two functions are not really needed, as it is
#easy to chain two operations together, but they
#are common and convenient
def contrastAndBrightness(img, amount, multiplier):
   return brightness(contrast(img,multiplier),amount)

def brightnessAndContrast(img, amount, multiplier):
   return contrast(brightness(img,amount),multiplier)

def grayscale(img, useLuminosity=True):
   if useLuminosity:
      return 0.21*img[:,:,0]+0.72*img[:,:,1]+0.07*img[:,:,2]
   else:
      return 0.33*img[:,:,0]+0.33*img[:,:,1]+0.33*img[:,:,2]

def sepia(img):
   sepMat=np.asarray([[0.393, 0.796, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
   img = img.dot(sepMat.T) 
   img[img>255]=255
   return img

def invert(img):
   return 255-img

def rgbTransform(img, r, g, b):
   if r<0 or g<0 or b<0:
      print('Error: parameters "r", "g", and "b" must be non-negative')
      sys.exit(2)
   #Unfortunately, this is not very readable,
   #but efficiency was a problem. Multiplies
   #rgb over the image and then applies a 3d
   #matrix filter to values that have rolled
   #over 255.
   params=np.asarray([r,g,b]);
   params=params[np.newaxis,np.newaxis,:]
   img=img*params
   img[img>(255/(params+eps))]=255
   return img

def fade(img, direction, color, mMin=0, mMax=1, aMin=0, aMax=0, addFirst=False):
   s=img.shape
   if color=='red':
      rgb=[255,0,0]
   elif color=='green':
      rgb=[0,255,0]
   elif color=='blue':
      rgb=[0,0,255]
   elif color=='cyan':
      rgb=[0,255,255]
   elif color=='magenta':
      rgb=[255,0,255]
   elif color=='yellow':
      rgb=[255,255,0]
   elif color=='black' or color=='white':
      print("""
      Warning: common stumbling block.
      Black and white use the same color value,
      but black is controlled by the multiplicative
      factor whereas white is controlled by the
      additive factor.""")
      rgb=[255,255,255]
   elif color=='grey' or color=='gray':
      rgb=[128,128,128]
   else:
      #User input an RGB array
      rgb=color
   rgb=np.asarray(rgb)/255.0

   #Compute fade lines
   if direction in ('left', 'l'):
      aLine=np.linspace(aMin, aMax, s[1])
      mLine=np.linspace(mMin, mMax, s[1])
   elif direction in ('right', 'r'):
      aLine=np.linspace(aMax, aMin, s[1])
      mLine=np.linspace(mMax, mMin, s[1])
   elif direction in ('top', 't'):
      aLine=np.linspace(aMin, aMax, s[0])
      mLine=np.linspace(mMin, mMax, s[0])
   elif direction in ('bottom', 'b'):
      aLine=np.linspace(aMax, aMin, s[0])
      mLine=np.linspace(mMax, mMin, s[0])
   else:
      print("""
      Error: acceptable directions are:
      left (or l)
      right (or r)
      top (or t)
      bottom (or b)
      """)
      sys.exit(2);

   #Store rgb scaled fLine filters in fMat
   aMat=np.asarray(rgb[:, np.newaxis]*aLine)
   mMat=np.asarray(rgb[:, np.newaxis]*mLine)
   #Apply filters across image layers
   if direction in ('left', 'l', 'right', 'r'):
      if addFirst:
         img=aMat.T[np.newaxis,:,:]+img
         img=mMat.T[np.newaxis,:,:]*img
      else:
         img=mMat.T[np.newaxis,:,:]*img
         img=aMat.T[np.newaxis,:,:]+img
   else:
      if addFirst:
         img=aMat.T[:,np.newaxis,:]+img
         img=mMat.T[:,np.newaxis,:]*img
      else:
         img=mMat.T[:,np.newaxis,:]*img
         img=aMat.T[:,np.newaxis,:]+img
 
   img[img>255]=255
   img[img<0]=0
   img=img.astype(np.uint8)

   return img


#Image Generators
def black(w, h):
   return np.zeros((h,w), dtype=np.uint8)

def white(w, h):
   return np.zeros((h,w), dtype=np.uint8)+255

def gray(w, h):
   return np.zeros((h,w), dtype=np.uint8)+128

def solid(w, h, r, g, b):
   img=np.zeros((h,w,3), dtype=np.uint8)
   img[:,:,0]=r
   img[:,:,1]=g
   img[:,:,2]=b
   return img

def grayNoise(w, h):
   return (np.random.rand(h,w)*256).astype(np.uint8)

def rgbNoise(w, h):
   return (np.random.rand(h,w,3)*256).astype(np.uint8)






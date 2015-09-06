import sys
import getopt
import inspect
from scipy import misc
import pImgLib
import pdb

def usage():
   #Half of this info belongs here
   #The other half is in the lib file
   helpMsg="""
   Usage: pImg libraryCall -flag arg
   Flags:
   -f or --file: Specify file path
   -p or --params: Specify function parameters
      If specifying multiple parameters, you MUST surround them with quotes
   -h or --help: Display this help

   For information about specific library functions:
   pImg usage
   """
   print(helpMsg)

def exitGracefully():
   usage()
   sys.exit(2)
   
if __name__=="__main__":
   argv=sys.argv[1:]
   if len(argv)<2 or not argv[0][0]=='-':
      exitGracefully() 
     
   img=None
   fPath=''

   #Custom flag and argument parsing
   cmds=[]
   flags=[]
   for i in range(len(argv)-1):
      if argv[i] in ('-c', '--command', '--cmd'):
         #Search through arguments for params until hit a flag.
         cmds+=[[argv[i]]]
         for p in argv[i+1:]:
            if p in ('-h', '--help', '-c', '--command', '-f', '--file'):
               break;
            cmds[-1]+=[p] 
            i+=1
      elif argv[i] in ('-f', '--file'):
         fPath=argv[i+1]
         i+=1
         try:
            img=misc.imread(fPath)
         except FileNotFoundError:
            print("File not found: "+fPath+". Is the path properly specified?")
            sys.exit(2)
         flags+=[['-f',img]] 
      elif argv[i] in ('-h', '--help'):
         exitGracefully()   
   #Use the cmd and flag lists built above to assemble a command string
   cmdStr=''
   firstIter=1
   for c in cmds: 
      c=c[1:] #strip -c
      oldCmd=cmdStr
      cmdStr='pImgLib.'+c[0]+'('  
      needImg=pImgLib.nArgs(c[0])>len(c[1:])
      if needImg and firstIter: 
         #Use user supplied image for base function cal;
         cmdStr+='img, '
      elif needImg and not firstIter:
         cmdStr+=oldCmd + ', '
      firstIter=0
      for p in c[1:]:
         #Handle string quotes
         if not(p[0]=='[' or p=='True' or p=='False'):
            try:
               float(p)
            except:
               p='"'+p+'"'
         cmdStr+=p+', ' 
      if len(c[1:])>0 or needImg:
         cmdStr=cmdStr[:-2] #strip comma
      cmdStr+=')'
   
   #This is IN NO WAY SAFE. It should not matter, as
   #this is a personal use program not running as root
   #try:
   print(cmdStr)
   retImg = eval(cmdStr)
   '''except:
      print("Tried to evaluate: "+callStr)
      print("""
      Does this look correct? If the call is not
      as you desired, check your flags/args.
      If this looks correct, check the function usage,
      or specify -h if you are confused.
      """)
      #sys.exit(2)
   '''
   try: 
      if not(retImg is None):
         misc.imsave("outputImg.png", retImg);
   except:
      print("""
      An error occured while trying to save the image.
      This usually means that the parameters you supplied
      do not make sense. Do not submit a bug report unless
      you are sure that your input is correct, as this is
      a personal use library, and I do not have time to
      ensure commercial quality robustness. However, if
      you want to fix it, feel free to submit a patch.
      """)
      sys.exit(2)





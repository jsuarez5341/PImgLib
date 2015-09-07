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
   Usage: pImg -flag arg (example: pImg -f imgPath -c rgbShift 20 20 50
   Note: you can chain multiple commands with multiple -c
   Flags:
   -f or --file: Specify file path
   -p or --params: Specify function parameters
      If specifying multiple parameters, you MUST surround them with quotes
   --jpg: Save as a .jpg
   -o or --output: Set save file name. Leave off the file extension.
   -d of --debug: Show internal command parsing
   -h or --help: Display this help

   For information about specific library functions:
   pImg -c usage
   """
   print(helpMsg)

def exitGracefully():
   usage()
   sys.exit(2)
   
if __name__=="__main__":
   argv=sys.argv[1:]
   if len(argv)<2 or not argv[0][0]=='-':
      exitGracefully() 
     
   #Custom flag and argument parsing
   cmds=[]
   flags={}
   for i in range(len(argv)):
      if argv[i] in ('-c', '--command', '--cmd'):
         #Search through arguments for params until hit a flag.
         cmds+=[[argv[i]]]
         for p in argv[i+1:]:
            if p in ('-h', '--help', '-c', '--command', '-f', '--file', '-d', '--debug', '--jpg', '-o', '--output'):
               break;
            cmds[-1]+=[p] 
            i+=1
      elif argv[i] in ('-f', '--file'):
         try:
            img=misc.imread(argv[i+1])
         except FileNotFoundError:
            print("File not found: "+argv[i+1]+". Is the path properly specified?")
            sys.exit(2)
         flags['f']=img 
      elif argv[i] == '--jpg':
         flags['jpg']=True
      elif argv[i] in ('-o', '--output'):
         flags['o']=argv[i+1]
      elif argv[i] in ('-h', '--help'):
         exitGracefully()   
      elif argv[i] in ('-d', '--debug'):
         flags['d']=True
      
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
   if 'd' in flags:
      print("Debug: command parsed as:")
      print(cmdStr)
   try:
      retImg = eval(cmdStr)
   except:
      print("Tried to evaluate: "+cmdStr)
      print("""
      Does this look correct? If the call is not
      as you desired, check your flags/args.
      If this looks correct, check the function usage,
      or specify -h if you are confused.
      """)
      #sys.exit(2)
   
   try: 
      ext='.png'
      if 'jpg' in flags:
         ext='.jpg'
      if not(retImg is None):
         fName='outputImg'
         if 'o' in flags:
            fName=flags['o']
         misc.imsave(fName+ext, retImg);
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


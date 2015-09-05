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

   if len(argv)==0 or not argv[1][0]=='-':
      exitGracefully() 
   if not (argv[0] in ('-h', '--help')):
      #Assume argument is a library function call
      funName=argv[0]
      argv=argv[1:]
     
   #Don't forget the colons for options that take arguments! 
   options='f:p:h'
   longOptions=['file=','params=', 'help']

   params=''
   fPath=''
   try:
      print(argv)
      opts, args = getopt.getopt(argv, options, longOptions) 
      print(opts)
      print(args)
      print('---')
   except getopt.GetoptError:
      exitGracefully()

   for opt,arg in opts:
      opt=opt.strip('-=')
      print('opt: '+opt+'   arg: '+arg)
      if opt in ('f', 'file'):
         fPath=arg
      elif opt in ('p', 'params'):
         params=arg
      elif opt in ('h', 'help'):
         exitGracefully()
   
   if not fPath=='': 
      #Read in file
      try:
         img=misc.imread(fPath)
      except FileNotFoundError:
         print("File not found: "+fPath+". Is the path properly specified?")
         sys.exit(2)
   nArgs=pImgLib.nArgs(funName)
   callStr=funName+'('
   params=params.split()
   if nArgs>len(params):
      #File param needed
      callStr+='img, '
   for p in params:
      callStr+=p+', '
   callStr=callStr[:-2]+')'

   #This is IN NO WAY SAFE. It should not matter, as
   #this is a personal use program not running as root
   #try:
   retImg = eval('pImgLib.'+callStr)
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
   misc.imsave("outputImg.png", retImg);




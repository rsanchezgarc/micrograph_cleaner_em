from __future__ import absolute_import, division, print_function
import sys, os
import matplotlib.pyplot as plt
import glob
from joblib import Parallel, delayed

DOWNLOAD_MODEL_URL="https://github.com/rsanchezgarc/carbonCleaner/blob/master/carbonCleaner/models/defaultModel.keras"
def main(inputMicsPath, inputCoordsDir, outputCoordsDir, deepLearningModel, boxSize, downFactor, deepThr,
         sizeThr, predictedMaskDir):


  micsFnames=getFilesInPath(inputMicsPath, ["mrc", "tif"])
  inputCoordsFnames=getFilesInPath(inputCoordsDir, ["txt", "tab", "pos"])
  coordsExtension= inputCoordsFnames[0].split(".")[-1]
  matchingFnames= getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension)
  assert len(matchingFnames)>0, "Error, there are no matching coordinate-micrograph files"
  from .cleanOneMic import cleanOneMic
  Parallel(n_jobs=1)( delayed(cleanOneMic)( * multipleNames+( deepLearningModel, 
                                              boxSize, downFactor, deepThr,sizeThr) )
                                          for multipleNames in matchingFnames.values() )
                                          
def getFilesInPath(pathsList, extensions):

  if isinstance(pathsList, str) or len(pathsList)==1:
    if not isinstance(pathsList, str) and len(pathsList)==1:
      pathsList= pathsList[0]
    if os.path.isdir(pathsList):
      pathsList= os.path.join(pathsList, "*")
    fnames=glob.glob(pathsList)
    assert len(fnames)>=1 and not os.path.isdir(pathsList), "Error, %s path not found or incorrect"%(pathsList)
    errorPath= pathsList
  else:
    fnames= pathsList
    errorPath= os.path.split(pathsList[0])[0]
  extensions= set(extensions)
  fnames= [ fname for fname in fnames if fname.split(".")[-1] in extensions ]
  assert len(fnames)>0, "Error, there are no < %s > files in path %s"%(" - ".join(extensions), errorPath)
  return fnames

def getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension):
  def getMicName(fname):
    return ".".join( os.path.basename( fname).split(".")[:-1]  )
    
  matchingFnames={}
  for fname in micsFnames:
    micName= getMicName(fname)
    print(micName)
    inCoordsFname= os.path.join(inputCoordsDir, micName+"."+coordsExtension)
    if os.path.isfile(inCoordsFname):
      outCoordsFname= os.path.join(outputCoordsDir, micName+"."+coordsExtension)
      if predictedMaskDir is not None:
        predictedMaskFname= os.path.join(predictedMaskDir, micName+".mrc")
      else:
        predictedMaskFname=None      
      matchingFnames[micName]= (fname, inCoordsFname, outCoordsFname, predictedMaskFname)  
    else:
      print("Warning, no coordinates for micrograph %s"%(fname))

  return matchingFnames
    
def parseArgs():
  import argparse
  parser = argparse.ArgumentParser(description='Rule out coordiantes that were selected in carbon/contaminated regions')
  def getRestricetedFloat(minVal=0, maxVal=1):
    def restricted_float(x):
      x = float(x)
      if x < minVal or x > maxVal:
        raise argparse.ArgumentTypeError("%r not in range [%f, %f]"%(x,minVal, maxVal))
      return x
    return restricted_float
  def file_choices(choices,fname):
    '''
    str
    '''
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
       parser.error("file %s extension not allowed: %s"%( (fname,)+(" ".join(choices),) ))
    return os.path.abspath(os.path.expanduser(fname))
    
  parser.add_argument('-i', '--inputMicsPath', type=str,  nargs='+', required=True,
                      help='path to input micrograph(s) were coordinates were picked (.mrc or .tif)')

  parser.add_argument('-c', '--inputCoordsDir', type=str, required=True,
                      help='input coordinates directory (.pos or tab separated x y). Filenames '+
                           'must agree with input micrographs except for extension')

  parser.add_argument('-o', '--outputCoordsDir', type=str,  required=True,
                      help='output coordinates directory')

  parser.add_argument('-d', '--deepLearningModel', type=str,  nargs='?', required=False,
                      help='deep learning model filename')
                                                             
  parser.add_argument('-b', '--boxSize', metavar='PXLs', type=int,  required=True,
                      help='particles box size in pixels')
                      
  parser.add_argument('-s', '--downFactor', type=float, nargs='?', required=False, default=1,
                      help='micrograph downsampling factor to scale coordinates')
                      
  parser.add_argument('--deepThr', type=getRestricetedFloat(), nargs='?', default=None, required=False,
                      help='deep learning threshold to rule out a coordinate. The bigger the more coordiantes'+
                           'will be rule out. Ranges 0..1. Recommended 0.5')
                           
  parser.add_argument('--sizeThr', type=getRestricetedFloat(0,1e5), nargs='?', default=0.8, required=False,
                      help='Failure threshold. Fraction of the micrograph predicted as contamination to ignore predictions. '+
                           '. Ranges 0..1. Default 0.8')
                           
  parser.add_argument('--predictedMaskDir', type=str, nargs='?', required=False,
                      help='directory to store the predicted masks. If a given mask already existed, it will be used instead'+
                           ' of a new prediction')
  args = vars(parser.parse_args())
  deepLearningModelPath=args["deepLearningModel"]
  if deepLearningModelPath is None:
    deepLearningModelPath= os.path.abspath(os.path.join(__file__, "..", "models", "defaultModel.keras"))
  args["deepLearningModel"]= deepLearningModelPath
  if not  os.path.isfile(deepLearningModelPath):
    print("Deep learning model not found. Downloading default model. If you want to use other model "+
          " use --deepLearningModel.")
    import requests
    r = requests.get(DOWNLOAD_MODEL_URL)
    if r.status_code!==200:
      raise Exception("It was not possible to download model")
    with open(deepLearningModelPath , 'wb') as f:
    write(r.content)
  return args

def commanLineFun():
  main( ** parseArgs() )
if __name__=="__main__":
  '''
LD_LIBRARY_PATH=/home/rsanchez/app/cuda-9.0/lib64:$LD_LIBRARY_PATH
python ruleOutCoords.py  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbonCleaner/coordsCleaned/ -d defaultModel.keras -b 180 -s 1.5   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0021_2x_SumCorr.mrc 

  '''
  commanLineFun()
  

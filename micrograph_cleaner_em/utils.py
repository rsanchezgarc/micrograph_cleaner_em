import sys, os
import glob

def getFilesInPaths(pathsList, extensions):
  if pathsList is None:
    return None
  if isinstance(pathsList, str) or 1 == len(pathsList):
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
    if inputCoordsDir is not None:
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
    else:
        predictedMaskFname= os.path.join(predictedMaskDir, micName+".mrc")
        matchingFnames[micName]= (fname, None, None, predictedMaskFname)
  return matchingFnames

def selectGpus(gpusStr):
  print("updating environ to select gpus %s" % (gpusStr))
  if gpusStr.startswith("all"):
    if 'CUDA_VISIBLE_DEVICES' in os.environ:
      gpus= [ elem.strip() for elem in os.environ['CUDA_VISIBLE_DEVICES'].split(",") ]
      return gpus, len(gpus)
    else:
      return [None], 1

  if gpusStr == '' or gpusStr is None or gpusStr=='-1':
      os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
      return [None], 1
  else:
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpusStr).replace(" ", "")
    gpus= [ int(num.strip()) for num in gpusStr.split(",") ]
    return gpus, len(gpus)
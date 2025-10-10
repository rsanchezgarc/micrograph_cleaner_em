import os
import glob
from subprocess import check_output, CalledProcessError


def getFilesInPaths(pathsList, extensions, abortIfEmpty=True):
  """
  Accepts:
    - single path string
      * file
      * directory (expands to *)
      * glob pattern
      * .txt list file: one absolute path (or glob) per line; '#' comments allowed
    - list of paths
  Filters by provided extensions (case-insensitive).
  """
  def _filter_and_norm(paths, exts):
    exts = {e.lower().lstrip(".") for e in set(exts)}
    out = []
    for p in paths:
      if not os.path.isfile(p):
        continue
      ext = p.lower().rsplit(".", 1)[-1] if "." in p else ""
      if ext in exts:
        out.append(p)
    # de-duplicate & sort for stability
    return sorted(set(out))

  if pathsList is None or len(pathsList) < 1:
    fnames = []
    errorPath = pathsList

  elif isinstance(pathsList, str) or len(pathsList) == 1:
    if not isinstance(pathsList, str) and len(pathsList) == 1:
      pathsList = pathsList[0]

    path_in = os.path.expanduser(pathsList)

    # NEW: support a .txt file with one path/glob per line
    if os.path.isfile(path_in) and path_in.lower().endswith(".txt"):
      candidates = []
      with open(path_in, "r", encoding="utf-8") as f:
        for line in f:
          s = line.strip()
          if not s or s.startswith("#"):
            continue
          s = os.path.expanduser(s)
          if os.path.isdir(s):
            candidates.extend(glob.glob(os.path.join(s, "*")))
          else:
            # allow globs inside the list file too
            candidates.extend(glob.glob(s))
      fnames = candidates
      errorPath = path_in

    else:
      if os.path.isdir(path_in):
        path_in = os.path.join(path_in, "*")
      fnames = glob.glob(path_in)
      assert len(fnames) >= 1 and not os.path.isdir(path_in), "Error, %s path not found or incorrect" % (path_in)
      errorPath = path_in

  else:
    # list of paths provided
    fnames = []
    for p in pathsList:
      p = os.path.expanduser(p)
      if os.path.isdir(p):
        fnames.extend(glob.glob(os.path.join(p, "*")))
      else:
        fnames.extend(glob.glob(p))
    try:
      errorPath = os.path.split(pathsList[0])[0]
    except IndexError:
      raise Exception("Error, pathList contains erroneous paths " + str(pathsList))

  # extension filter (case-insensitive), dedup, sort
  fnames = _filter_and_norm(fnames, extensions)

  if abortIfEmpty:
    assert len(fnames) > 0, "Error, there are no < %s > files in path %s" % (" - ".join(extensions), errorPath)

  return fnames

def getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension):
  def getMicName(fname):
    return ".".join( os.path.basename( fname).split(".")[:-1]  )

  matchingFnames={}
  for fname in micsFnames:
    micName= getMicName(fname)
#    print(micName)
    if inputCoordsDir is not None:
      coordsFname= micName+"."+coordsExtension
      inCoordsFname= os.path.join(inputCoordsDir, coordsFname)
      if not os.path.isfile((inCoordsFname)) and coordsExtension.endswith("star"):
        coordsFname = micName + "_autopick." + coordsExtension
        inCoordsFname = os.path.join(inputCoordsDir, coordsFname)
      if os.path.isfile(inCoordsFname):
        outCoordsFname= os.path.join(outputCoordsDir, coordsFname)
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
    mask_CUDA_VISIBLE_DEVICES(gpusStr)
    gpus= [ int(num.strip()) for num in gpusStr.split(",") ]
    return gpus, len(gpus)


def resolveDesiredGpus(gpusStr):
  if gpusStr == '' or gpusStr is None or gpusStr.startswith("-"):
      return [None], 1
  elif gpusStr.startswith("all"):
    if 'CUDA_VISIBLE_DEVICES' in os.environ: #this is for slurm
      gpus_str = os.environ['CUDA_VISIBLE_DEVICES']
      if gpus_str:
          gpus = [elem.strip() for elem in gpus_str.split(",")]
          return gpus, len(gpus)
      else:
          return [None], 1
    else:
      try:
        nGpus= int(check_output("nvidia-smi -L | wc -l", shell=True))
        if nGpus > 0:
            gpus= list(range(nGpus))
            return gpus, nGpus
        else:
            return [None], 1
      except (CalledProcessError, FileNotFoundError, OSError):
        return [None], 1
  else:
    gpus= [ int(num.strip()) for num in gpusStr.split(",") ]
    return gpus, len(gpus)

def mask_CUDA_VISIBLE_DEVICES(gpuList):
  print("updating environ to select gpus %s" % (gpuList))
  if gpuList is None:
    gpusStr="-1"
  elif isinstance(gpuList, list):
    gpusStr = ",".join([ str(elem).strip() for elem in gpuList])
  else:
    gpusStr= gpuList
  os.environ['CUDA_VISIBLE_DEVICES'] = str(gpusStr).replace(" ", "")

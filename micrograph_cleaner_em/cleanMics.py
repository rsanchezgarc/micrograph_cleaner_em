from __future__ import absolute_import, division, print_function
import os
import glob

from micrograph_cleaner_em.utils import getFilesInPaths, getMatchingFiles, selectGpus

os.environ['OPENBLAS_NUM_THREADS']="4"
os.environ['MKL_NUM_THREADS']="4"
os.environ['OMP_NUM_THREADS']="4"
from joblib import Parallel, delayed

from .cmdParser import parseArgs

def main(inputMicsPath, inputCoordsDir, outputCoordsDir, deepLearningModel, boxSize, downFactor, deepThr,
         sizeThr, predictedMaskDir, gpus="0"):
  gpus, n_jobs= selectGpus(gpus)
  micsFnames=getFilesInPaths(inputMicsPath, ["mrc", "tif"])
  inputCoordsFnames=getFilesInPaths(inputCoordsDir, ["txt", "tab", "pos"])
  coordsExtension= inputCoordsFnames[0].split(".")[-1] if inputCoordsFnames is not None else None
  matchingFnames= getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension)
  assert len(matchingFnames)>0, "Error, there are no matching coordinate-micrograph files"
  from .cleanOneBatchOfMic import cleanOneMic

  def prepareArgs(multipleNames, i):
    micFname, inputCoordsFname, outCoordsFname, predictedMaskFname= multipleNames
    args={
      'micFname': micFname,
      'inputCoordsFname':inputCoordsFname,
      'outCoordsFname': outCoordsFname,
      'predictedMaskFname': predictedMaskFname,
      'deepLearningModel' : deepLearningModel,
      'boxSize': boxSize,
      'downFactor': downFactor,
      'deepThr': deepThr,
      'sizeThr': sizeThr,
      'gpus': [gpus[i % n_jobs]]
    }
    return args

  Parallel(n_jobs= n_jobs)( delayed(cleanOneMic)( **prepareArgs(multipleNames, i))
                                            for i, multipleNames in enumerate(sorted(matchingFnames.values() ) ))



def commanLineFun():
  main( ** parseArgs() )

if __name__=="__main__":
  '''
LD_LIBRARY_PATH=/home/rsanchez/app/cuda-9.0/lib64:$LD_LIBRARY_PATH

python -m  micrograph_cleaner_em.cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/micrograph_cleaner_em/coordsCleaned/ -b 180 -s 1   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0021_2x_SumCorr.mrc

  '''
  commanLineFun()


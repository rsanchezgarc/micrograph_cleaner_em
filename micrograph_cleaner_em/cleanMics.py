from __future__ import absolute_import, division, print_function
import os


os.environ['OPENBLAS_NUM_THREADS']="4"
os.environ['MKL_NUM_THREADS']="4"
os.environ['OMP_NUM_THREADS']="4"
from joblib import Parallel, delayed


def main(inputMicsPath, inputCoordsDir, outputCoordsDir, deepLearningModel, boxSize, downFactorCoords, deepThr,
         sizeThr, predictedMaskDir, preproDownsampleMic=1, gpus="0"):
  from .utils import getFilesInPaths, getMatchingFiles, resolveDesiredGpus

  gpus, n_jobs= resolveDesiredGpus(gpus)
  micsFnames=getFilesInPaths(inputMicsPath, ["mrc", "tif"])
  inputCoordsFnames=getFilesInPaths(inputCoordsDir, ["txt", "tab", "pos", "star"], abortIfEmpty=False)
  coordsExtension= inputCoordsFnames[0].split(".")[-1] if len(inputCoordsFnames)>0 else None
  if coordsExtension=="star" and deepThr is None:
    raise Exception("When using relion star file coordinates as input, a deepThr must be provided, as relion does "+
                    "not allow for unknow metadata labels")
  matchingFnames= getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension)
  assert len(matchingFnames)>0, "Error, there are no matching coordinate-micrograph files"

  def prepareArgs(multipleNames, gpuId):
    micFname, inputCoordsFname, outCoordsFname, predictedMaskFname= multipleNames
    args={
      'micFname': micFname,
      'inputCoordsFname':inputCoordsFname,
      'outCoordsFname': outCoordsFname,
      'predictedMaskFname': predictedMaskFname,
      'deepLearningModel' : deepLearningModel,
      'boxSize': boxSize,
      'downFactorCoords': downFactorCoords,
      'deepThr': deepThr,
      'sizeThr': sizeThr,
      'preproDownsampleMic':preproDownsampleMic,
      'gpus':[gpuId]
    }
    return args

  from .cleanOneMic import cleanOneMic
  def launch_batch_cleanOneMic(batchOfArgs):
    for cleanMicsArgs in batchOfArgs:
      cleanOneMic(**cleanMicsArgs)

  with Parallel(n_jobs=n_jobs, batch_size=1) as parallel:
    args=[ [] for i in range(n_jobs)]
    for i, multipleNames in enumerate(sorted(matchingFnames.values())):
      args[i % n_jobs].append( prepareArgs(multipleNames, gpus[i % n_jobs]) )

    parallel( delayed(launch_batch_cleanOneMic)( batchOfArgs) for  batchOfArgs in args)



def commanLineFun():
  from .cmdParser import parseArgs
  main( ** parseArgs() )

if __name__=="__main__":
  '''
LD_LIBRARY_PATH=/home/rsanchez/app/cuda-9.0/lib64:$LD_LIBRARY_PATH

python -m  micrograph_cleaner_em.cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/micrograph_cleaner_em/coordsCleaned/ -b 180 -s 1   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0021_2x_SumCorr.mrc
python -m  micrograph_cleaner_em.cleanMics  --predictedMaskDir /home/rsanchez/tmp/ -b 180 -s 1   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0021_2x_SumCorr.mrc

  '''
  commanLineFun()


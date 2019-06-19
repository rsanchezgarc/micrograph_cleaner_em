import os
from threading import Lock


LOCK = Lock()
MASK_PREDICTOR_HANDLER=None

def cleanOneMic(micFname, boxSize, deepLearningModel, inputCoordsFname=None, outCoordsFname=None,
                predictedMaskFname=None, downFactor=1, deepThr=0.2, sizeThr=0.8, gpus=[0]):
  '''
  cleanOneMic computes a 0. to 1. mask given one micrograph fname. Values close to 0 are assigned to clean areas whereas
  values close to 1 correspond to carbon or other contaminated regions.

  :param micFname: a path to the micrograph. Mandatory
  :param inputCoordsFname: a path to the coordinates file associated to the micFname (.txt, .pos or .start). If None, no
                           coordinate cleanup is performed
  :param outCoordsFname: fname to store the cleaned coordinates. If None, no coordinate cleanup is performed. Required if
                         inputCoordsFname provided
  :param predictedMaskFname: fname to store the predicted mask. If None, no predicted mask is saved to disk
  :param deepLearningModel: a path where the deep learning model is saved
  :param boxSize: estimated particle boxSize in pixels (int) of the input micrograph
  :param downFactor: Downsampling factor applied to the coordinates. Set it !=1 if the coordinates where picked
                     from a different micrograph (down/up sampled) than micFname.
  :param deepThr: Threshold to rule out coordinates. Particles are ruled out if score> deepThr.
  :param sizeThr: Threshold to ignore masks. If sizeThr fraction of the micrograph is predicted as contamination, skip
                    this micrograph for coordinates cleaning.
  :param gpus: list of gpu ids (ints) or None. If None, all CUDA_VISIBLE_DEVICES gpus will be allocated although just one
               will be employed for computation (this is default tensorflow behaviour)

  :return: predictedMask as np.array of the same shape that the micrograph contained in micFname
  '''
  print(micFname, boxSize, deepLearningModel, inputCoordsFname, outCoordsFname,
                predictedMaskFname, downFactor, deepThr, sizeThr, gpus)

  from .filesManager import loadMic, loadCoords, writeMic, writeCoords
  from .predictMask import MaskPredictor
  from .filterCoords import filterCoords


  global MASK_PREDICTOR_HANDLER
  with LOCK:
    if MASK_PREDICTOR_HANDLER is None:
      MASK_PREDICTOR_HANDLER= MaskPredictor(deepLearningModel, boxSize, gpus)


  maskPredictor= MASK_PREDICTOR_HANDLER

  if predictedMaskFname is not None and os.path.isfile(predictedMaskFname):
    print("WARNING: mask already predicted for %s. Using it instead computing a new predicted mask"%(micFname))
    predictedMask= loadMic( predictedMaskFname)
  else:
    inputMic= loadMic( micFname )
    predictedMask= maskPredictor.predictMask(inputMic)
    if predictedMaskFname is not None:
      writeMic(predictedMaskFname, predictedMask)
  
  if inputCoordsFname is not None:
    inputCoords= loadCoords(inputCoordsFname, downFactor)
    if deepThr is not None:
      deepThr= None if deepThr<=0 else deepThr
    filteredCoords= filterCoords( inputCoords, predictedMask, deepThr, sizeThr)
    writeCoords(outCoordsFname, filteredCoords)

  return predictedMask

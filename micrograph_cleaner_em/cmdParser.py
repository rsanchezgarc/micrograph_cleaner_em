from __future__ import absolute_import, division, print_function
import sys, os

DOWNLOAD_MODEL_URL = 'http://campins.cnb.csic.es/micrograph_cleaner/defaultModel.keras.gz'
DEFAULT_MODEL_PATH = os.path.expanduser("~/.local/share/micrograph_cleaner_em/models/")


def parseArgs():
  import argparse

  example_text = '''examples:

  + Donwload deep learning model
cleanMics --download

  + Compute masks from imput micrographs and store them
cleanMics  -c path/to/inputCoords/ -b $BOX_SIXE  -i  /path/to/micrographs/ --predictedMaskDir path/to/store/masks

  + Rule out input bad coordinates (threshold<0.5) and store them into path/to/outputCoords
cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b $BOX_SIXE -s $DOWN_FACTOR  -i  /path/to/micrographs/ --deepThr 0.5

+ Compute goodness scores from input coordinates and store them into path/to/outputCoords
  cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b $BOX_SIXE -s $DOWN_FACTOR  -i  /path/to/micrographs/ --deepThr 0.5

'''

  parser = argparse.ArgumentParser(
    description='Compute goodness score for picked coordinates. Rule out bad coordinates',
    epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)

  def getRestricetedFloat(minVal=0, maxVal=1):
    def restricted_float(x):
      x = float(x)
      if x < minVal or x > maxVal:
        raise argparse.ArgumentTypeError("%r not in range [%f, %f]" % (x, minVal, maxVal))
      return x

    return restricted_float

  def file_choices(choices, fname):
    '''
    str
    '''
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
      parser.error("file %s extension not allowed: %s" % ((fname,) + (" ".join(choices),)))
    return os.path.abspath(os.path.expanduser(fname))

  parser.add_argument('-i', '--inputMicsPath', metavar='MIC_FNAME', type=str, nargs='+', required=True,
                      help='micrograph(s) filenames where coordinates were picked (.mrc or .tif).\n' +
                           'Linux wildcards or several files are allowed.')

  parser.add_argument('-c', '--inputCoordsDir', type=str, required=False,
                      help='input coordinates directory (.pos or tab separated x y). Filenames ' +
                           'must agree with input micrographs except for file extension.')

  parser.add_argument('-o', '--outputCoordsDir', type=str, required=False,
                      help='output coordinates directory.')

  parser.add_argument('-d', '--deepLearningModel', metavar='MODEL_PATH', type=str, nargs='?', required=False,
                      help=('(optional) deep learning model filename. If not provided, model at %s ' +
                            'will be employed') % (DEFAULT_MODEL_PATH))

  parser.add_argument('-b', '--boxSize', metavar='PXLs', type=int, required=True,
                      help='particles box size in pixels')

  parser.add_argument('-s', '--downFactor', type=float, nargs='?', required=False, default=1,
                      help='(optional) micrograph downsampling factor to scale coordinates, Default no scaling. Use it '+
                            'only if the micrographs have been down/up sampled with respect the picked coordinates')

  parser.add_argument('--deepThr', type=getRestricetedFloat(), nargs='?', default=None, required=False,
                      help='(optional) deep learning threshold to rule out coordinates (coord_score<=deepThr-->accepted). ' +
                           'The smaller the treshold ' +
                           'the more coordinates will be ruled out. Ranges 0..1. Recommended 0.2')

  parser.add_argument('--sizeThr', type=getRestricetedFloat(0, 1.), nargs='?', default=0.8, required=False,
                      help='Failure threshold. Fraction of the micrograph predicted as contamination to ignore predictions. ' +
                           'Ranges 0..1. Default 0.8')

  parser.add_argument('--predictedMaskDir', type=str, nargs='?', required=False,
                      help='directory to store the predicted masks. If a given mask already existed, it will be used instead' +
                           ' of a new prediction')

  parser.add_argument('-g', '--gpus', metavar='GPU_Ids', type=str, required=False, default="0",
                      help='GPU ids to employ. Comma separated list. E.g. "0,1". Default 0. use "-1" for CPU-only computation' +
                           'or "all" to use all devices found in CUDA_VISIBLE_DEVICES')

  class _DownloadModel(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None,
                 choices=None, required=False, help=None, metavar=None):
      super(_DownloadModel, self).__init__(option_strings=option_strings, dest=dest, default=default,
                                           nargs=nargs, const=const, required=required, help=help, metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
      import requests, gzip
      from io import BytesIO

      r = requests.get(DOWNLOAD_MODEL_URL)
      if r.status_code != 200:
        raise Exception("It was not possible to download the model")
      if len(values) == 0:
        downloadPath = DEFAULT_MODEL_PATH
      else:
        downloadPath = os.path.abspath(os.path.expanduser(values[0]))
      if not os.path.exists(downloadPath):
        os.makedirs(downloadPath)
      deepLearningModelPath = os.path.join(downloadPath, "defaultModel.keras")
      print("DOWNLAODING MODEL at %s" % (downloadPath))
      with open(deepLearningModelPath, 'wb') as f:
        content = gzip.GzipFile(fileobj=BytesIO(r.content))
        f.write(content.read())
      print("DOWNLOADED!!")
      parser.exit()

  parser.add_argument('--download', nargs='*', action=_DownloadModel,
                      help='Download default micrograph_cleaner_em model. ' +
                           'It will be saved at %s if no path provided' % (DEFAULT_MODEL_PATH))

  args = vars(parser.parse_args())
  deepLearningModelPath = args["deepLearningModel"]
  if deepLearningModelPath is None:
    if not os.path.exists(DEFAULT_MODEL_PATH):
      os.makedirs(DEFAULT_MODEL_PATH)
    deepLearningModelPath = os.path.join(DEFAULT_MODEL_PATH, "defaultModel.keras")
  args["deepLearningModel"] = deepLearningModelPath
  if not os.path.isfile(deepLearningModelPath):
    print(("Deep learning model not found at %s. Downloading default model with --download or " +
           "indicate its location with --deepLearningModel.") % DEFAULT_MODEL_PATH)
    sys.exit(1)

  if args["inputCoordsDir"] is None and args["predictedMaskDir"] is None:
    raise Exception("Either inputCoordsDir or predictedMaskDir (or both) must be provided")
    parser.print_help()
  if args["inputCoordsDir"] is not None and args["outputCoordsDir"] is None:
    raise Exception("Error, if inputCoordsDir provided, then outputCoordsDir must also be provided")
    parser.print_help()

  if args["outputCoordsDir"] is not None and args["inputCoordsDir"] is None:
    raise Exception("Error, if outputCoordsDir provided, then inputCoordsDir must also be provided")
    parser.print_help()

  if "-1" in args["gpus"]:
    args["gpus"] = None
  if "download" in args:
    del args["download"]
  return args

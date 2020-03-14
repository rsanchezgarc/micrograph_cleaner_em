import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings

warnings.filterwarnings("ignore", "Cannot provide views on a non-contiguous")
warnings.filterwarnings("ignore", "Unrecognised machine stamp")
warnings.filterwarnings("ignore", "Map ID string not found")

warnings.filterwarnings("ignore", ".*", category=ImportWarning)
warnings.filterwarnings("ignore", ".*", category=DeprecationWarning)
try:
  warnings.filterwarnings("ignore", ".*", category=ResourceWarning)
except NameError:
  pass

from .cleanOneMic import cleanOneMic
from .predictMask import MaskPredictor
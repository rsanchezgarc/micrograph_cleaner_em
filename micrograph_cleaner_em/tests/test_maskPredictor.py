from unittest import TestCase
import os

from micrograph_cleaner_em.tests.testConfig import TEST_DATA_ROOT_DIR

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_CUDNN_USE_AUTOTUNE", "0")
os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")

class TestMaskPredictor(TestCase):
  def setUp(self):
    from subprocess import check_call
    download_cmd = "python -m micrograph_cleaner_em.cleanMics --download"
    check_call(download_cmd, shell=True)


  def test_predictMask(self):
    from micrograph_cleaner_em import MaskPredictor
    from micrograph_cleaner_em.config import DEFAULT_MODEL_PATH
    import mrcfile
    import numpy as np

    micFname = os.path.join(TEST_DATA_ROOT_DIR, "mics", "Ucsf_stack_1142_DW.mrc")
    precomputedMaskFname= os.path.join(TEST_DATA_ROOT_DIR, "masks", "Ucsf_stack_1142_DW.mrc")
    boxSize = 46
    deepLearningModelFname = os.path.join(DEFAULT_MODEL_PATH, "defaultModel.h5")

    with mrcfile.open(micFname, permissive=True) as f: mic = f.data.copy()

    with MaskPredictor(boxSize, deepLearningModelFname, gpus=[0]) as mp:
      mask = mp.predictMask(mic)

    self.assertTrue(mask.shape==mic.shape, "Error, mask shape is not the same that mic shape")

    with mrcfile.open(precomputedMaskFname, permissive=True) as f: precomputedMask = f.data.copy()

    print(np.mean((mask - precomputedMask)**2))

    self.assertTrue( np.mean((mask - precomputedMask)**2)<1e-3, "Error, precomputed mask is not similar to computed mask")


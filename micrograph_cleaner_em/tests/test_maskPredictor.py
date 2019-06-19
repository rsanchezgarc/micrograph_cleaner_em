from unittest import TestCase
from .testConfig import TEST_DATA_ROOT_DIR
import os

class TestMaskPredictor(TestCase):

  def test_predictMask(self):
    from micrograph_cleaner_em import MaskPredictor
    from micrograph_cleaner_em.cmdParser import DEFAULT_MODEL_PATH
    import mrcfile
    import numpy as np

    micFname = os.path.join(TEST_DATA_ROOT_DIR, "mics", "Ucsf_stack_1142_DW.mrc")
    precomputedMaskFname= os.path.join(TEST_DATA_ROOT_DIR, "masks", "Ucsf_stack_1142_DW.mrc")
    boxSize = 46
    deepLearningModelFname = os.path.join(DEFAULT_MODEL_PATH, "defaultModel.keras")

    with mrcfile.open(micFname, permissive=True) as f: mic = f.data.copy()

    with MaskPredictor(deepLearningModelFname, boxSize, gpus=[0]) as mp:
      mask = mp.predictMask(mic)

    self.assertTrue(mask.shape==mic.shape, "Error, mask shape is not the same that mic shape")

    with mrcfile.open(precomputedMaskFname, permissive=True) as f: precomputedMask = f.data.copy()

    print(np.mean((mask - precomputedMask)**2))

    self.assertTrue( np.mean((mask - precomputedMask)**2)<1e-3, "Error, precomputed mask is not similar to computed mask")


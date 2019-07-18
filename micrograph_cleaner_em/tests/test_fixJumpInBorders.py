import os
from unittest import TestCase

from micrograph_cleaner_em.tests.testConfig import TEST_DATA_ROOT_DIR


class TestFixJumpInBorders(TestCase):

  def test_fixJumps(self):
    from micrograph_cleaner_em.predictMask import fixJumpInBorders
    from micrograph_cleaner_em.filesManager import loadMic

    micsDir=os.path.join(TEST_DATA_ROOT_DIR,"rawPreds")
    fnamesDict={
           "20190628_Her2_2mgml_nanoprobe_0003_aligned_mic_DW.mrc":False,
           "20190628_Her2_2mgml_nanoprobe_0094_aligned_mic_DW.mrc":False,
           "20190628_Her2_2mgml_nanoprobe_0225_aligned_mic_DW.mrc":False,
           "20190628_Her2_2mgml_nanoprobe_0330_aligned_mic_DW.mrc":True,
           "stack_0002_2x_SumCorr.mrc":True,
           "stack_0007_2x_SumCorr.mrc": True
           }
    for basename in fnamesDict:
      fname= os.path.join(micsDir, basename)
      micro_out=  loadMic(fname)
      axis=0
      stride=128
      micro_fix, wasFixed= fixJumpInBorders(micro_out.copy(), axis, stride)
      print("wasFixed", wasFixed)
      self.assertTrue( wasFixed == fnamesDict[basename])
      # import matplotlib.pyplot as plt
      # fig=plt.figure(); fig.suptitle(fname); fig.add_subplot(121); plt.imshow(micro_out, cmap="gray"); fig.add_subplot(122); plt.imshow(micro_fix, cmap="gray"); plt.show()
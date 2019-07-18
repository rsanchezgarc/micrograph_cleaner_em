from unittest import TestCase
import os

from micrograph_cleaner_em.tests.testConfig import TEST_DATA_ROOT_DIR

class TestGetMatchingFiles(TestCase):
  def test_relion_match(self):
    from micrograph_cleaner_em.utils import getFilesInPaths
    from micrograph_cleaner_em.utils import getMatchingFiles
    inputCoordsDir= os.path.join(TEST_DATA_ROOT_DIR,"inCoords/relion")
    micsFnames=getFilesInPaths(os.path.join(TEST_DATA_ROOT_DIR,"mics"), ["mrc"])
    inputCoordsFnames = getFilesInPaths(inputCoordsDir, ["txt", "tab", "pos", "star"])
    coordsExtension = inputCoordsFnames[0].split(".")[-1] if inputCoordsFnames is not None else None
    predictedMaskDir=None
    outputCoordsDir=os.path.join(TEST_DATA_ROOT_DIR,"/outCoords/relion")
    matchingFiles=getMatchingFiles(micsFnames, inputCoordsDir, outputCoordsDir, predictedMaskDir, coordsExtension)
    self.assertTrue(len(matchingFiles)==1 and matchingFiles["Ucsf_stack_1142_DW"][0].endswith("mrc") and
                    matchingFiles["Ucsf_stack_1142_DW"][1].endswith("_autopick.star") and
                    matchingFiles["Ucsf_stack_1142_DW"][2].endswith("_autopick.star")
                    , "Error, No matching files were found for relion")
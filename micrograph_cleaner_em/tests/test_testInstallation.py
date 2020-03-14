import os
from subprocess import CalledProcessError
from unittest import TestCase
from subprocess import check_output


class TestTestInstallation(TestCase):
  VERSIONS= ["2.7", "3.6"]
  ENV_NAME_TEST= "test_mic_cleaner_34r4341324132"
  CONDA_PATH = os.path.split(os.path.split(check_output("which conda", shell=True).strip().decode("utf-8"))[0])[0]
  CONDA_ACTIVATE_CMD = ". " + os.path.join(CONDA_PATH, "etc/profile.d/conda.sh")
  TEST_INSTALL_CMD= ("export PYTHONPATH='' && conda create -y -n  %(envName)s python=%(pyVersion)s && "+
                   CONDA_ACTIVATE_CMD+" && "+"conda activate %(envName)s && "+" ls && "
                   "%(installCmd)s && cleanMics -h")
  CLEAN_INSTALL_CMD=(CONDA_ACTIVATE_CMD+" && conda deactivate && conda env remove -y -n  %(envName)s")

  def _test_testInstallationGeneric(self, installCmd):
    from subprocess import check_call

    envName= TestTestInstallation.ENV_NAME_TEST
    for pyVersion in TestTestInstallation.VERSIONS:
      try:
        cmd= TestTestInstallation.TEST_INSTALL_CMD%locals()
        print(cmd)
        check_call(cmd , shell=True, env=os.environ )
      except CalledProcessError:
        raise
      finally:
        check_call(TestTestInstallation.CLEAN_INSTALL_CMD%locals(), shell=True, env=os.environ )

  def test_testInstallationSetupPy(self):
    self._test_testInstallationGeneric("cd ../.. && python setup.py install")

  def test_testInstallationPip(self):
    self._test_testInstallationGeneric("cd /tmp && python -m pip install micrograph-cleaner-em")

  def test_testInstallationConda(self):
    self._test_testInstallationGeneric("cd /tmp && conda install --yes micrograph-cleaner-em -c rsanchez1369 -c anaconda "
                                      "-c conda-forge")
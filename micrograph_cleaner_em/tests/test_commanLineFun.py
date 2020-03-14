import os
from subprocess import check_output
from unittest import TestCase


class TestCommanLineFun(TestCase):
  def test_commanLineFun(self):
    from subprocess import check_call
    import tempfile

    os.environ["PATH"] += ":" + os.path.expanduser("~/app/anaconda3/bin/")
    CONDA_PATH = os.path.split(os.path.split(check_output("which conda", shell=True).strip().decode("utf-8"))[0])[0]
    PYTHON_BIN= os.path.join(CONDA_PATH,"envs","env_micrograph_cleaner_em","bin","python")
    print(PYTHON_BIN)
    with tempfile.TemporaryDirectory() as dirpath:
      check_call("pwd")
      check_call(PYTHON_BIN+" -m micrograph_cleaner_em.cleanMics -i data/mics/* -b 80 -g -1 -p"+dirpath,
                 shell=True )

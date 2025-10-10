import os, sys
from subprocess import check_output
from unittest import TestCase


class TestCommanLineFun(TestCase):
  def test_commanLineFun(self):
    from subprocess import check_call
    import tempfile
    with tempfile.TemporaryDirectory() as dirpath:
      datapath = os.path.join(os.path.dirname(__file__), "data/mics")
      download_cmd = "python -m micrograph_cleaner_em.cleanMics --download"
      check_call(download_cmd, shell=True)
      cmd = f"python  -m micrograph_cleaner_em.cleanMics -i {datapath}/* -b 80 -g -1 -p {dirpath}"
      check_call(cmd, shell=True )
    with tempfile.TemporaryDirectory() as dirpath:
      cmd = f"python  -m micrograph_cleaner_em.cleanMics -i {datapath}/* -b 80 -g all -p {dirpath}"
      check_call(cmd, shell=True )

from unittest import TestCase


class TestCommanLineFun(TestCase):
  def test_commanLineFun(self):
    from subprocess import check_call
    import tempfile
    with tempfile.TemporaryDirectory() as dirpath:
      check_call("pwd")
      check_call("python -m micrograph_cleaner_em.cleanMics -i data/mics/* -b 80 -g -1 -p"+dirpath,
                 shell=True )

import sys, os
from setuptools import setup
from subprocess import Popen, PIPE

VERSION="0.35"
def readme():
  readmePath= os.path.abspath(os.path.join(__file__, "..", "README.md") )
  with open(readmePath) as f:
      return f.read()

nvccProgram = Popen(["which", "nvcc"],stdout=PIPE).stdout.read()
tensorFlowTarget = "==1.12"

if sys.version_info[0] <3:
  FileNotFoundError= OSError

if nvccProgram== "":
  print("No cuda instalation found. Installing cpu version")
else:
  try:
    nvccVersion = Popen(["nvcc", '--version'],stdout=PIPE).stdout.read().decode("utf-8")
  except FileNotFoundError:
    nvccVersion=""
  if "release 9.0" in nvccVersion:  # cuda 9
    print("CUDA 9 found")
    tensorFlowTarget = "-gpu==1.12.0"
  elif "release 10.0" in nvccVersion:  # cuda 10
    print("CUDA 10.0 found")
    tensorFlowTarget = "-gpu==1.13.0"
  elif "release 10.1" in nvccVersion:  # cuda 10
    print("CUDA 10.1 found")
    tensorFlowTarget = "-gpu==1.14.0"
  else:
    print("Unrecognized CUDA version. Installing cpu version")

install_requires=[
        'scikit-image==0.14.2',
        'scipy==1.1',
        'joblib==0.12',
        'numpy ==1.15.4',
        'tensorflow%s'%tensorFlowTarget,
        'pandas==0.24',
        'mrcfile==1.1',
        'requests==2.22',
    ]

if sys.version_info[0] < 3:
  install_requires = ['pillow==5.0', 'matplotlib==2.2.4', 'networkx==2.2', 'PyWavelets==1.0.3']+install_requires

setup(name='micrograph_cleaner_em',
  version=VERSION,
  description='Deep learning for cryo-EM micrograph cleaning',
  long_description=readme(),
  long_description_content_type="text/markdown",
  keywords='cryo-EM deep learning',
  url='https://github.com/rsanchezgarc/micrograph_cleaner_em',
  author='Ruben Sanchez-Garcia',
  author_email='rsanchez@cnb.csic.es',
  license='Apache 2.0',
  packages=[ 'micrograph_cleaner_em' ],
  install_requires= install_requires,
  entry_points={
      'console_scripts': ['cleanMics=micrograph_cleaner_em.cleanMics:commanLineFun'],
  },
  include_package_data=True,
  zip_safe=False)

import sys, os
from setuptools import setup
from subprocess import Popen, PIPE
from distutils.command.install import install as _install

def readme():
  readmePath= os.path.abspath(os.path.join(__file__, "..", "README.md") )
  with open(readmePath) as f:
      return f.read()

nvccProgram = Popen(["which", "nvcc"],stdout=PIPE).stdout.read()
if nvccProgram== "":
  tensorFlowTarget=""
  raise Exception("No cuda instalation found")
else:
  nvccVersion = Popen(["nvcc", '--version'],stdout=PIPE).stdout.read().decode("utf-8")
  if "release 8.0" in nvccVersion:  # cuda 8
    print("CUDA 8 found")
    tensorFlowTarget = "-gpu==1.4.1"
  elif "release 9.0" in nvccVersion:  # cuda 9
    print("CUDA 9 found")
    tensorFlowTarget = "-gpu==1.12.0"
  elif "release 10.0" in nvccVersion:  # cuda 10
    print("CUDA 10 found")
    tensorFlowTarget = "-gpu==1.13.0"



if sys.version_info[0] < 3:
  install_requires=[
          'scikit-image==0.14.2',
          'scipy==1.1',
          'joblib',
          'tensorflow%s'%tensorFlowTarget,
          'keras==2.2.4',
          'pandas==0.24.2',
          'mrcfile',
          'requests',
          'networkx==2.2',
      ]
else:
  install_requires=[
          'scikit-image==0.14.2',
          'scipy==1.1',
          'joblib',
          'tensorflow%s'%tensorFlowTarget,
          'keras==2.2.4',
          'pandas==0.24.2',
          'mrcfile',
          'requests'
      ]
                 
setup(name='micrograph_cleaner_em',
      version='0.2',
      description='Deep learning for cryo-EM micrograph cleaning',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='cryo-EM deep learning',
      url='https://github.com/rsanchezgarc/micrograph_cleaner_em',
      author='Ruben Sanchez-Garcia',
      author_email='rsanchez@cnb.csic.es',
      license='Apache 2.0',
      packages=['micrograph_cleaner_em'],
      install_requires= install_requires,
      entry_points={
          'console_scripts': ['cleanMics=micrograph_cleaner_em.cleanMics:commanLineFun'],
      },
      include_package_data=True,
      zip_safe=False)


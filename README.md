#Carbon Cleaner
**carbon_cleaner_em** is a python package designed to segment cryo-EM micrographs into:

  -carbon/high-contrast region 
  -good regions
  
so that incorrectly picked coordinates can be easily ruled out

To get a complete description of usage execute

`cleanMics -h`

Example

`cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b 180 -s 1.0   -i  /path/to/micrographs/ --predictedMaskDir path/to/store/masks --deepThr 0.5`


##INSTALLATION:

###anaconda (recommended)

1) Install anaconda Python 3x version from https://www.anaconda.com/distribution/

2) Create an environment for carbon_cleaner
  `conda create -n env_carbon_cleaner_em python=3.6`

3) Activate environment (each time you want to use carbon_cleaner you will need to activate it)
  `conda activate env_carbon_cleaner_em`
  
4) Install carbon_cleaner_em from repository
  `conda install ?????? -c anaconda`

5) Download deep learning model
  `cleanMics --download`

6) Ready!
  
###pip/source option:


1) install CUDA and cudnn in such a way that tensorflow (https://www.tensorflow.org/) can be executed. 
   Carbon_cleaner is compatible with CUDA-8,CUDA-9 and CUDA-10.
   Tensorflow version will be automatically selected according your CUDA version and installed later.
   CUDA is available at https://developer.nvidia.com/cuda-toolkit and cudnn is available at
   https://developer.nvidia.com/cudnn
   Easy cudnn instalation can be performed automatically at step 2 using python module cudnnenv

1.1) (optional) create virtual environment
`pip install virtualenv`
`virtualenv --system-site-packages -p python3 ./venv`
`source ./venv/bin/activate`
2) Install carbon_cleaner_em
`git clone https://github.com/rsanchezgarc/carbon_cleaner_em.git; cd carbon_cleaner_em; python setup.py install`
  or
`pip install carbon_cleaner_em`

2.1) If cudnn not installed yet, install install cudnnenv
 `pip install cudnnenv`
 
 and execute
 `cudnnenv install [VERSION]`, where recommended versions are "v6-cuda8" for CUDA-8, "v7.0.1-cuda9" for CUDA-9 and
"v7.4.1-cuda10" for CUDA-10.
 
3) Download deep learning model
  `cleanMics --download`
  
4) Ready!

###scipion option:

1) Install scipion version 2.0+ from http://scipion.i2pc.es/

2) Install xmipp either from plugin manager or from command line:
  `scipion installp -p scipion-em-xmipp`

3) Install deepLearningToolkit either from plugin manager or from command line:
  `scipion installb deepLearningToolkit`

4) Ready!

##USAGE

Carbon_cleaner employs an U-net-based deep learning model to segmentate micrographs into good regions and bad regions. Thus,
it is mainly used as a post-processing step after particle picking in which coordinates selected in high contrast artefacts
such as carbon will be ruled out. Additionally, it can be employed to generate binary masks so that particle pickers can be
prevented from considering problematic regions.
Thus, carbon_cleaner employs needs a mandatory argument micrographs and it can recive as input

1) A directory where picked coordinates in pos format or plain text (columns whith header colnames x and y) are located. There
must be one different coordinate file for each micrograph named as the micrograph. 
E.g. /path/to/mics/mics_1.mrc /path/to/coords


#TO CONTINUE

```
cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbon_cleaner_em/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbon_cleaner_em/micsPreds --deepThr 0.5
```

If cuda not found, export its path
```
export LD_LIBRARY_PATH=/path/to/cuda/cuda-9.0/lib64:$LD_LIBRARY_PATH
```
and then execute cleanMics


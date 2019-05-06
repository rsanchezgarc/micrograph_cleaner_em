#Carbon Cleaner
**carbon_cleaner_em** is a python package designed to segment cryo-EM micrographs into:

  -carbon/high-contrast region 
  -normal regions
  
so that incorrectly picked coordinates can be easily ruled out

To get a complete description of usage execute

`cleanMics -h`

Example

`cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbon_cleaner_em/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbon_cleaner_em/micsPreds --deepThr 0.5`


##INSTALLATION:


###anaconda (recommended)

1) Install anaconda Python 3x version from https://www.anaconda.com/distribution/

2) Create an environment for carbon_cleaner
  `conda create -n env_carbon_cleaner_em python=3.7`

3) Activate environment (each time you want to use carbon_cleaner you will need to activate it)
  `conda activate env_carbon_cleaner_em`
  
4) Install carbon_cleaner_em from repository
`conda install ?????? -c anaconda`

5) Download deep learning model
  `cleanMics --download`

6) Ready!
  
###pip/source option:

This option is required for python2 installation.

1) install cuda and cudnn so that tensorflow (https://www.tensorflow.org/) can be executed. This program is compatible
   with CUDA-8,CUDA-9 and CUDA-10. Please refere to tensorflow installation guide to ensure cudnn and cuda versions are
   compatible. Tensorflow version will be automatically selected according your cuda version and installed later.

2) Install carbon_cleaner_em
`git clone https://github.com/rsanchezgarc/carbon_cleaner_em.git; cd carbon_cleaner_em; python setup.py install`
  or
`pip install carbon_cleaner_em`

3) Download deep learning model
  `cleanMics --download`
  
4) Ready!

###scipion option:

1) Install scipion version 2.0+ from http://scipion.i2pc.es/

2) Install xmipp either from plugin manager or from command line:
  `scipion installp -p scipion-em-xmipp`

3) Install deepLearningToolkit either from plugin manager or from command line:
  `scipion installb deepLearningToolkit`
  
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


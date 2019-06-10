# MicrographCleaner
**MicrographCleaner** (micrograph_cleaner_em) is a python package designed to segment cryo-EM
 micrographs into:

  - carbon/high-contrast or contaminated regions 
  - good regions
  
so that incorrectly picked coordinates can be easily ruled out

To get a complete description of usage execute

`cleanMics -h`

##### Example

`cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b 180 -s 1.0   -i  /path/to/micrographs/ --predictedMaskDir path/to/store/masks --deepThr 0.5`


## INSTALLATION:

### anaconda (recommended)

1) Install anaconda Python 3x version from https://www.anaconda.com/distribution/

2) Create an environment for MicrographCleaner  
  `conda create -n env_micrograph_cleaner_em python=3.6`

3) Activate environment (each time you want to use micrograph_cleaner you will need to activate it)  
  `conda activate env_micrograph_cleaner_em`
  
4) Install micrograph_cleaner_em from repository  
  ` conda install -c rsanchez1369 micrograph-cleaner-em`

5) Download deep learning model  
  `cleanMics --download`

6) Ready!
  
### pip/source option:


1) install CUDA and cudnn in such a way that tensorflow (https://www.tensorflow.org/) can be executed. 
   micrograph_cleaner is compatible with CUDA-8,CUDA-9 and CUDA-10.
   Tensorflow version will be automatically selected according your CUDA version and installed later.
   CUDA is available at https://developer.nvidia.com/cuda-toolkit and cudnn is available at
   https://developer.nvidia.com/cudnn.  
   Easy cudnn instalation can be performed automatically at step 2 using python module cudnnenv

1.1) (optional) create virtual environment  
```
pip install virtualenv
virtualenv --system-site-packages -p python3 ./env_micrograph_cleaner_em
source ./env_micrograph_cleaner_em/bin/activate
```
2) Install micrograph_cleaner_em  
```
git clone https://github.com/rsanchezgarc/micrograph_cleaner_em.git
cd micrograph_cleaner_em
python setup.py install
```
  or  
`pip install micrograph_cleaner_em`

2.1) If cudnn not installed yet, install install cudnnenv  
`pip install cudnnenv`  
 
 and execute  
`cudnnenv install [VERSION]`, where recommended versions are "v6-cuda8" for CUDA-8, "v7.0.1-cuda9" for CUDA-9 and
"v7.4.1-cuda10" for CUDA-10.  
 
3) Download deep learning model  
  `cleanMics --download`
  
4) Ready!  

### scipion option:

1) Install scipion version 2.0+ from http://scipion.i2pc.es/  

2) Install xmipp either from plugin manager or from command line  
  `scipion installp -p scipion-em-xmipp`  

3) Install deepLearningToolkit either from plugin manager or from command line  
  `scipion installb deepLearningToolkit`  

4) Ready!

## USAGE

MicrographCleaner employs an U-net-based deep learning model to segmentate micrographs into good regions and bad regions. Thus, it is mainly used as a post-processing step after particle picking in which coordinates selected in high contrast artefacts, such as carbon, will be ruled out. Additionally, it can be employed to generate binary masks so that particle pickers can be prevented from considering problematic regions.
Thus, micrograph_cleaner employs as a mandatory argument a(some) micrograph(s) fileneame(s) and the particle size in pixels. Additionally it can recive as input:

1) A directory where picked coordinates are located and another directory where scored/cleaned coordiantes will be saved. Coordinates will be saved in pos format or plain text (columns whith header colnames x and y) are located. 
There must be one different coordinates file for each micrograph named as the micrograph and the output coordiantes will preserve the naming.  
E.g. -c path/to/inputCoordsDirectory/ -o /path/to/outputCoordsDirectory/  
Allowed formats are xmipp pos and raw text tab separated with at least two columns named as xcoor, ycoor in the header.
Raw text file example:
```
micFname1.tab:
###########################################
xcoor ycoor otherInfo1 otherInfo2
12  143  -1  0.1
431  4341  0  0.2
323  321  1  0.213
###########################################
```
2) A directory where predicted masks will be saved (mrc format).
E.g. --predictedMaskDir path/where/predictedMasksWillBeSaved/  

3) A downsampling factor (can be less than 1 if actually upsampling was performed) in case the coordinates where picked from
micrographs at different scale.  
E.g. -s 1.5 will downsample coordinates by a factor 1.5 and then it will apply the predicted mask that is as big as the imput micrographs  

4) Any combination of previous options.  

Trained MicrographCleaner model is available at http://campins.cnb.csic.es/micrograph_cleaner/ and can be automatically download executing  
`cleanMics --download`


Beware that if you installed micrograph_cleaner using pip/source, then CUDA and cudnn libraries should be
available prior execution, so if CUDA is not found, export its path prior execution  
```
export LD_LIBRARY_PATH=/path/to/cuda/cuda-9.0/lib64:$LD_LIBRARY_PATH
```
and then execute `cleanMics` program  

#### Examples

```
#Donwload deep learning model
cleanMics --download
    
#Compute masks from imput micrographs and store them
cleanMics -b $BOX_SIXE  -i  /path/to/micrographs/ --predictedMaskDir path/to/store/masks

#Rule out input bad coordinates (threshold<0.5) and store them into path/to/outputCoords
cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b $BOX_SIXE -s $DOWN_FACTOR  -i  /path/to/micrographs/ --deepThr 0.5

#Compute goodness scores from input coordinates and store them into path/to/outputCoords
cleanMics  -c path/to/inputCoords/ -o path/to/outputCoords/ -b $BOX_SIXE -s $DOWN_FACTOR  -i  /path/to/micrographs/ --deepThr 0.5     
```

```
cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/micrograph_cleaner_em/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/micrograph_cleaner_em/micsPreds --deepThr 0.5
```




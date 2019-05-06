#carbonCleaner
**carbonCleaner** is a python package designed to segment cryo-EM micrographs into:

  -carbon/high-contrast region 
  -normal regions
  
so that incorrectly picked coordinates can be easily ruled out

To get a complete description of usage execute

`cleanMics -h`

Example

`cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbonCleaner/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbonCleaner/micsPreds --deepThr 0.5`


##INSTALLATION:

###pip/setup option:

1) install cuda and cudnn so that tensorflow (https://www.tensorflow.org/) can be executed. This program is compatible
   with CUDA-8,CUDA-9 and CUDA-10. Please refere to tensorflow installation guide to ensure cudnn and cuda vesrsions are
   compatible. Tensorflow will be automatically installed later.

2) Install carbonCleaner
`git clone https://github.com/rsanchezgarc/carbonCleaner.git; cd carbonCleaner; python setup.py install`
  or
`pip install carbonCleaner`

3) Download deep learning model
  `cleanMics --download`
  
4) execute cleanMics command

```
cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbonCleaner/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbonCleaner/micsPreds --deepThr 0.5
```

If cuda not found, export its path
```
export LD_LIBRARY_PATH=/path/to/cuda/cuda-9.0/lib64:$LD_LIBRARY_PATH
```
and then execute cleanMics


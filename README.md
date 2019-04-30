#carbonCleaner
**carbonCleaner** is a python package designed to segment cryo-EM micrographs into:

  -carbon/high-contrast region 
  -normal regions
  
so that picked coordinates can be easily pruned

To get a complete description of usage execute

cleanMics -h

Example

`cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbonCleaner/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbonCleaner/micsPreds --deepThr 0.5`


INSTALLATION:

pip/setup option:

1) install cuda and cudnn so that tensorflow can run. This program is compatible
   with CUDA-8,CUDA-9 and CUDA-10

2) Install carbonCleaner
`python setup.py install`
  or
`pip install carbonCleaner`

3) execute cleanMics command. Ensure CUDA and cudnn libraries are available.

```
LD_LIBRARY_PATH=/home/rsanchez/app/cuda-9.0/lib64:$LD_LIBRARY_PATH
cleanMics  -c /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/008337_XmippParticlePickingAutomatic/extra/ -o ~/tmp/carbonCleaner/coordsCleaned/ -b 180 -s 1.0   --inputMicsPath  /home/rsanchez/ScipionUserData/projects/2dAverages_embeddings/Runs/002321_ProtImportMicrographs/extra/stack_0002_2x_SumCorr.mrc --predictedMaskDir /home/rsanchez/tmp/carbonCleaner/micsPreds --deepThr 0.5
```


#!/usr/bin/env bash
conda-build ../micrograph_cleaner_em/ -c anaconda
anaconda_path=`which python | rev | cut -f 5- -d"/" | rev`
#conda install --use-local micrograph-cleaner-em -c anaconda
echo rsanchez1369 | anaconda upload $anaconda_path/conda-bld/linux-64/micrograph-cleaner-em-*.bz2   && conda build purge
#xxxXxx


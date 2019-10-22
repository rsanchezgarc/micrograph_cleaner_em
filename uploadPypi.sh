#!/usr/bin/env bash
rm -r -f dist micrograph_cleaner_em.egg-info
python setup.py sdist
#pip install twine
echo rsanchez1369 | twine upload dist/*gz

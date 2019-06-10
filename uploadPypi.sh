#!/usr/bin/env bash
python setup.py sdist
#pip install twine
echo rsanchez1369 | twine upload dist/*

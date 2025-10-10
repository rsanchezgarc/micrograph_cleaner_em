from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent

# Prefer README for long_description
long_description = ""
readme = ROOT / "README.md"
if readme.exists():
    long_description = readme.read_text(encoding="utf-8")

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
        'scipy==1.10.0',
        'joblib==0.12',
        'numpy ==1.22.0',
        'tensorflow%s'%tensorFlowTarget,
        'h5py==2.10',
        'pandas==0.24',
        'mrcfile==1.1',
        'requests==2.22',
    ]

setup(
    name="micrograph-cleaner-em",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="Deep-learning micrograph denoising/segmentation for cryo-EM (TF2/Keras3 rescue)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsanchezgarc/micrograph_cleaner_em",
    author="Original authors + maintainers",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs", "examples")),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
           "cleanMics=micrograph_cleaner_em.cleanMics:commanLineFun"
        ]
    },
)

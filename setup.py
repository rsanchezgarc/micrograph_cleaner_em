from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent

# Prefer README for long_description
long_description = ""
readme = ROOT / "README.md"
if readme.exists():
    long_description = readme.read_text(encoding="utf-8")

# Read requirements dynamically
req_file = ROOT / "requirements.txt"   # change to "requests.txt" if that's your filename
with req_file.open(encoding="utf-8") as f:
    install_requires = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
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

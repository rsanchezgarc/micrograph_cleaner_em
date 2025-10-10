import os

MODEL_IMG_SIZE=256
DESIRED_PARTICLE_SIZE= 16
DOWNLOAD_MODEL_URL = 'https://zenodo.org/records/17093439/files/deepMicrographCleaner.tgz'
DEFAULT_MODEL_PATH = os.path.expanduser("~/.local/share/micrograph_cleaner_em/models/")
BATCH_SIZE = 16
ROTATIONS=[0, 30, 45, 90, 150, 180, 200, 270]

import os

MODEL_IMG_SIZE=256
DESIRED_PARTICLE_SIZE= 16
DOWNLOAD_MODEL_URL = 'http://campins.cnb.csic.es/micrograph_cleaner/defaultModel.keras.gz'
DEFAULT_MODEL_PATH = os.path.expanduser("~/.local/share/micrograph_cleaner_em/models/")
BATCH_SIZE = 16
ROTATIONS=[0, 30, 45, 90, 150, 180, 200, 270]

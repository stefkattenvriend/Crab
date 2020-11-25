import os
import config

def init():
    if not os.path.exists(config.IMAGE_UPLOADS):
        os.makedirs(config.IMAGE_UPLOADS)
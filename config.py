from pathlib import Path

IMAGE_UPLOADS = Path("static/img/uploads/")
ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
TESTING = True
DEBUG = True
FLASK_ENV = 'development'
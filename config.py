class Config(object):
    DEBUG = False
    TEMPLATE_FILE_PATH = "static/download_template"
    EXTRACTION_FILE_PATH = "app/static/download_extract"
    DOWNLOAD_EXTRACT = "static/download_extract"
    SECRET_KEY = "uigdsjgdsjgcgcdgjsdajg"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

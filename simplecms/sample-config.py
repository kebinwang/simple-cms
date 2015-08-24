import os


MODULE_NAME = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]


class BaseConfig(object):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


Config = DevelopmentConfig

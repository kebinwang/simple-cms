import os


MODULE_NAME = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]


class BaseConfig(object):
    pass


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = "don'ttellyou"

    MYSQLHOST = "localhost"
    MYSQLPASSWD = "xiachufang"
    MYSQLUSER = "xiachufang"
    MYSQLDB_NAME = "xiachufang"
    MYSQL_DB_URL = "mysql://%s:%s@%s/%s" \
                   % (MYSQLUSER, MYSQLPASSWD, MYSQLHOST, MYSQLDB_NAME)


class ProductionConfig(BaseConfig):
    pass


Config = DevelopmentConfig

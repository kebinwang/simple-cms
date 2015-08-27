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
    DB_CHARSET = 'utf8mb4'
    DB_URL = "mysql://%s:%s@%s/%s"\
             % (MYSQLUSER, MYSQLPASSWD, MYSQLHOST, MYSQLDB_NAME)
    DB_CONFIG = {
        'url': DB_URL,
        'charset': DB_CHARSET,
    }

    # DB_URL = 'sqlite:///default.db'
    # DB_CONFIG = {
    #     'url': DB_URL,
    # }


class ProductionConfig(BaseConfig):
    pass


Config = DevelopmentConfig

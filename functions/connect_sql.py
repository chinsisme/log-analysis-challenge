from sqlalchemy import create_engine
import pymysql
import configparser


def sqlalchemy_connect():
    config = configparser.ConfigParser()
    config.read('parameters.ini')
    address = config.get('DATABASE', 'ADDRESS')
    username = config.get('DATABASE', 'USERNAME')
    password = config.get('DATABASE', 'PASSWORD')
    database = config.get('DATABASE', 'NAME')
    return create_engine("mysql+pymysql://{}:{}@{}/{}".format(username, password, address, database))


def pymysql_connect():
    config = configparser.ConfigParser()
    config.read('parameters.ini')
    return pymysql.connect(host=config.get('DATABASE', 'ADDRESS'),
                           user=config.get('DATABASE', 'USERNAME'),
                           passwd=config.get('DATABASE', 'PASSWORD'),
                           db=config.get('DATABASE', 'NAME')
                           )

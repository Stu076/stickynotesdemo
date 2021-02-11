import os

basedir = os.path.abspath(os.path.dirname(__file__))
# postgresql://user:password@host:port/
postgres_local_base = "postgresql://postgres:admin@localhost:5432/"
database_name = "stickynotes"


class BaseConfig:
	"""Base config"""
	SECRET_KEY = os.getenv("SECRET_KEY", "12345")
	DEBUG = False
	BCRYPT_LOG_ROUNDS = 13
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
	"""Development config"""
	DEBUG = True
	BCRYPT_LOG_ROUNDS = 4
	SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
	"""Testing config"""
	DEBUG = True
	TESTING = True
	BCRYPT_LOG_ROUNDS = 4
	SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + "_test"
	PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
	"""Production config"""
	SECRET_KEY = "b'\x16\x98\xf3\xc4\x11\x06\x16\x1e\xf4IQ\x12\xc3\x81\xc7\xfe\xaf\x8c5\xcebe8\x05'"
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

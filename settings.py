"""File with settings and configs for the project"""

from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default='postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres'
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default='postgresql+asyncpg://postgres_test:postgres_test@127.0.0.1:5432/postgres_test'
)
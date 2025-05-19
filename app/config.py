import os


def get_database_url():
    """
    Returns the database URL from environment variables.
    See: https://12factor.net/config
    """
    return os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/starterdb")

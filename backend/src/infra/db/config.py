import dataclasses
from typing import ClassVar

from environs import Env
from sqlalchemy import URL


@dataclasses.dataclass(frozen=True, slots=True)
class DbConfig:
    """Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes:
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.

    """

    host: str
    password: str
    user: str
    database: str
    port: int
    naming_convention: ClassVar[dict[str, str]] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        """Creates the DbConfig object from environment variables.

        Returns:
            Database configuration populated from the environment.
        """
        host = env.str("POSTGRES_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("POSTGRES_PORT", 5432)

        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
        )

    def construct_sqlalchemy_url(
        self,
        driver: str = "asyncpg",
        host: str | None = None,
        port: int | None = None,
    ) -> str:
        """Constructs a SQLAlchemy URL for this database configuration.

        Returns:
            SQLAlchemy connection URL.
        """
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return str(uri.render_as_string(hide_password=False))

    @property
    def construct_psql_dns(self) -> str:
        uri = URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        return str(uri.render_as_string(hide_password=False))

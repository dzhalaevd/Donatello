from dataclasses import (
    dataclass,
)

from environs import (
    Env,
)
from sqlalchemy.engine import URL


@dataclass
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
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(
        self,
        driver: str = "asyncpg",
        host: str | None = None,
        port: int | None = None,
    ) -> str:
        """Construct a SQLAlchemy URL for this database configuration.

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

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        """Create the DbConfig object from environment variables.

        Returns:
            Database configuration populated from the environment.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(host=host, password=password, user=user, database=database, port=port)


@dataclass
class TgBot:
    """Creates the TgBot object from environment variables."""

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env) -> "TgBot":
        """Create the TgBot object from environment variables.

        Returns:
            Telegram bot configuration populated from the environment.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS", subcast=int)
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig:
    """Redis configuration class.

    Attributes:
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.

    """

    redis_pass: str | None
    redis_port: int | None
    redis_host: str | None

    def dsn(self) -> str:
        """Construct a Redis DSN.

        Returns:
            Redis data source name.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env) -> "RedisConfig":
        """Create the RedisConfig object from environment variables.

        Returns:
            Redis configuration populated from the environment.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host)


@dataclass
class Miscellaneous:
    """Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes:
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).

    """

    other_params: str | None = None


@dataclass
class Config:
    """The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes:
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).

    """

    tg_bot: TgBot
    misc: Miscellaneous
    db: DbConfig | None = None
    redis: RedisConfig | None = None


def load_config(path: str | None = None) -> Config:
    """Load application configuration.

    Args:
        path: Optional path to an environment file.

    Returns:
        Configuration populated from the file or process environment.
    """
    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        # db=DbConfig.from_env(env),
        # redis=RedisConfig.from_env(env),
        misc=Miscellaneous(),
    )


cfg = load_config()

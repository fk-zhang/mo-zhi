from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    env: str = "dev"

    # MySQL
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "password"
    mysql_db: str = "mo_zhi"
    mysql_charset: str = "utf8mb4"

    # MongoDB
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_username: str = ""
    mongo_password: str = ""
    mongo_db: str = "mo_zhi"
    mongo_auth_source: str = "admin"  # Default auth source
    mongo_max_pool_size: int = 100
    mongo_min_pool_size: int = 0
    mongo_max_idle_time_ms: int = 30000  # 30 seconds
    mongo_connect_timeout_ms: int = 10000  # 10 seconds
    mongo_socket_timeout_ms: int = 30000  # 30 seconds
    mongo_retry_writes: bool = True
    mongo_retry_reads: bool = True

    # MySQL Connection Pool Settings
    db_pool_size: int = 20
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600  # Recycle connections after 1 hour
    db_pool_pre_ping: bool = True
    sqlalchemy_echo: bool = False

    @computed_field  # type: ignore[misc]
    @property
    def database_url(self) -> str:
        """Get MySQL connection URL."""
        return (
            f"mysql+asyncmy://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
            f"?charset={self.mysql_charset}"
        )
    
    @computed_field  # type: ignore[misc]
    @property
    def mongo_uri(self) -> str:
        """Get MongoDB connection URI."""
        if self.mongo_username and self.mongo_password:
            return (
                f"mongodb://{self.mongo_username}:{self.mongo_password}@"
                f"{self.mongo_host}:{self.mongo_port}/"
                f"?authSource={self.mongo_auth_source}"
            )
        return f"mongodb://{self.mongo_host}:{self.mongo_port}/"
    
    @computed_field  # type: ignore[misc]
    @property
    def mongo_connection_options(self) -> dict:
        """Get MongoDB connection options."""
        return {
            "maxPoolSize": self.mongo_max_pool_size,
            "minPoolSize": self.mongo_min_pool_size,
            "maxIdleTimeMS": self.mongo_max_idle_time_ms,
            "connectTimeoutMS": self.mongo_connect_timeout_ms,
            "socketTimeoutMS": self.mongo_socket_timeout_ms,
            "retryWrites": self.mongo_retry_writes,
            "retryReads": self.mongo_retry_reads,
        }


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    API_KEY: str = ""
    GPT_MODEL: str = "gpt-3.5-turbo"
    BOT_TOKEN: str = ""

    POSTGRES_DB: str = "travel"
    POSTGRES_HOST: str = "db"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_USER: str = "travel-bot"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chat_id: str
    authorization: str

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    settings = Settings()  # type: ignore
    return settings


if __name__ == "__main__":
    settings = get_settings()
    print(f"{settings.authorization=}")
    print(f"{settings.chat_id=}")

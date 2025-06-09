from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    chat_id: str
    authorization: str

    @field_validator("chat_id")
    @classmethod
    def validate_str(cls, value: str) -> str:
        count = len(value)
        if count != 20:
            raise ValueError("str must be 20 characters long")
        if not value.isalnum():
            raise ValueError("str must be alphanumeric")
        return value

    @field_validator("authorization")
    @classmethod
    def validate_authorization(cls, value: str) -> str:
        # print(f"{value=}")
        if not value.startswith("Bearer "):
            raise ValueError("Authorization must start with 'Bearer '")
        return value

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    settings = Settings()  # type: ignore
    return settings


if __name__ == "__main__":
    try:
        settings = get_settings()
        print(settings.model_dump())
    except ValueError as e:
        print(e)

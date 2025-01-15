from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
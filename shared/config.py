from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PATH_BASE: str
    SIGN_PASSWORD: str
    SIGN_NAME: str
    POLITICA_NAME: str
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        secrets_dir = None # Desactiva cualquier caché de secretos

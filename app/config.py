from pydantic import BaseSettings, Field


class LoadSettings(BaseSettings):
    wkhtmltopdf: str = Field('/usr/bin/wkhtmltopdf', env='WKHTMLTOPDF')


settings = LoadSettings()

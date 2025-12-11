from pydantic import (
    SecretStr,
)

from app.settings.base_settings import BaseConfig


class RetailSettings(BaseConfig):
    SUBDOMAIN: str
    API_KEY: SecretStr

    @property
    def api_url(self) -> str:
        return f"https://{self.SUBDOMAIN}.retailcrm.ru/api/v5"

    @property
    def temp_api_url(self) -> str:
        return f"https://{self.SUBDOMAIN}.retailcrm.ru/api/"

    @property
    def api_key(self) -> str:
        return self.API_KEY.get_secret_value()


retail_crm_settings = RetailSettings()

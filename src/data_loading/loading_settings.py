from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataLoadingSettings(BaseSettings):
    receiver_url: Optional[str] = Field(default=None, alias="DATA_LOADER_URL")

    receiver_name: Optional[str] = Field(default=None, alias="DATA_LOADER_NAME")
    receiver_port: Optional[str | int] = Field(default=None, alias="DATA_LOADER_PORT")
    receiver_endpoint: Optional[str | int] = Field(
        default="/", alias="DATA_LOADER_ENDPOINT"
    )

    local_storage_dir: Optional[str] = Field(default="", alias="DATA_STORAGE_DIR")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def use_remote_loader(self) -> bool:
        if self.receiver_url:
            return True

        if self.receiver_name and self.receiver_port:
            return True

        return False

    @property
    def remote_receiver_url(self) -> str | None:
        if self.receiver_url:
            if not self.receiver_url.startswith(("http://", "https://")):
                return f"http://{self.receiver_url}"
            else:
                return self.receiver_url

        if self.receiver_name and self.receiver_port:
            return f"http://{self.receiver_url}:{str(self.receiver_port)}{self.receiver_endpoint}"

        return None


loading_settings = DataLoadingSettings()

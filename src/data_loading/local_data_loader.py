import os
from urllib.parse import quote

from .data_loader import DataLoader
from .loading_settings import loading_settings


class LocalLoader(DataLoader):
    def __init__(self):
        super().__init__()
        self.storage_dir = loading_settings.local_storage_dir

    def load(self, data_container, extension: str = "md"):
        filename = quote(data_container.source, safe="")

        os.makedirs(self.storage_dir, exist_ok=True)
        filepath = os.path.join(self.storage_dir, filename + f".{extension}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data_container.data)

        self.logger.info(f"Loaded data locally for {data_container.source}")

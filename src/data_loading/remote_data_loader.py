import json

import requests

from .data_loader import DataLoader
from .loading_settings import loading_settings


class RemoteDataLoader(DataLoader):
    def __init__(self):
        self.receiver_url = loading_settings.remote_receiver_url

    def load(self, data_container):
        headers = {"Content-Type": "application/json"}
        data = {"source_url": data_container.source, "content": data_container.data}
        try:
            response = requests.post(
                self.receiver_url, data=json.dumps(data), headers=headers
            )
            response.raise_for_status()
            self.logger.info(f"Loaded data remotely for {data_container.source}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Can't load data remotely with error: {e}")

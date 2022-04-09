import logging
from typing import List


class Config:

    token: str
    plugin_directories: List[str]
    log_level: str

    def __init__(self, **kwargs) -> None:
        self.token = kwargs.get('token', '')
        self.plugin_directories = kwargs.get('plugin_directories', '')
        self.log_level = kwargs.get('log_level', logging.INFO)
